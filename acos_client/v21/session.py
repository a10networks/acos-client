#! coding: utf-8
# Copyright 2014,  Doug Wiegley,  A10 Networks.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import acos_client.errors as acos_errors
from acos_client.ctrippkg.result import Result
from acos_client.ctrippkg.redisconfig import RedisConfig
import platform
import json
import requests
import socket
import time
from redlock import Redlock


from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl


class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

class Session(object):

    def __init__(self, client, username, password):
        self.client = client
        self.http = client.http
        self.username = username
        self.password = password
        self.session_id = None

    @property
    def id(self):
        deviceIP = self.client.host
        self.session_id = self.get_redis_session(deviceIP)
        if not self.check_session_invalid(self.session_id, deviceIP):
            local_ip = self.get_local_ip()
            redisobj = RedisConfig()
            redis_server = redisobj.get_redis_servers(True)
            redis_conf_ls = [{"host": s["host"], "port": s["port"], "db": s["dbno"]} for s in redis_server]
            lock_mgmt = Redlock(redis_conf_ls)
            device_lock = lock_mgmt.lock(local_ip+"_"+deviceIP+'_device_lock_calabash', 30*1000)
            tmp_count = 0
            while isinstance(device_lock, bool) and not device_lock and tmp_count < 1000:
                tmp_count += 1
                time.sleep(0.5)
                self.session_id = self.get_redis_session(deviceIP)
                if self.check_session_invalid(self.session_id, deviceIP):
                    return self.session_id

                device_lock = lock_mgmt.lock(local_ip+"_"+deviceIP+'_device_lock_calabash', 30*1000)

            self.session_id = self.get_redis_session(deviceIP)
            if self.check_session_invalid(self.session_id, deviceIP):
                return self.session_id

            self.authenticate(self.username, self.password)
            #set sessionid to redis
            self.set_session_to_redis(self.session_id, deviceIP)
            lock_mgmt.unlock(device_lock)
        return self.session_id

    def authenticate(self, username, password):
        url = "/services/rest/v2.1/?format=json&method=authenticate"
        params = {
            "username": username,
            "password": password
        }

        if self.session_id is not None:
            self.close()

        r = self.http.post(url, params)
        self.session_id = r['session_id']
        return r

    def close(self):
        try:
            self.client.partition.active()
        except Exception:
            pass
        try:
            url = ("/services/rest/v2.1/?format=json&method=session"
                   ".close&session_id=%s" % self.session_id)

            r = self.http.post(url, {"session_id": self.session_id})
        except acos_errors.InvalidPartitionParameter:
            pass
        finally:
            self.session_id = None

        return r

    def get_local_ip(self,):
        systype = platform.system()
        if systype.upper() == "WINDOWS":
            return socket.gethostbyname(socket.gethostname())
        elif systype.upper() == "LINUX":
            #linux环境下特有的包
            import fcntl
            import struct
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', 'eth0'[:15]))[20:24])
        return None

    def get_redis_session(self, deviceIP):
        redisobj = RedisConfig()
        local_ip = self.get_local_ip()
        redis_conn_ls = redisobj.get_redis_connection(isMaster=False)
        redis_conn_ls = redis_conn_ls["message"]
        deviceIP_sessions = redis_conn_ls[0]["redis_conn"].hget('acos_sessions', deviceIP)
        if not deviceIP_sessions:#外层key不存在的情况
            return "123"
        all_serverip_session_dict = json.loads(deviceIP_sessions)

        if local_ip not in all_serverip_session_dict.keys():#clientip首次调用
            return "123"
        redis_session_dict = all_serverip_session_dict[local_ip]
        return redis_session_dict['session_id']


    def set_session_to_redis(self, sessionid, deviceIP):
        redisobj = RedisConfig()
        local_ip = self.get_local_ip()
        redis_conn_ls = redisobj.get_redis_connection()
        redis_conn_ls = redis_conn_ls["message"]

        r_redis_conn_ls = []
        w_redis_conn_ls = []
        for redis_conn in redis_conn_ls:
            if redis_conn["isMaster"]:
                w_redis_conn_ls.append(redis_conn)
            else:
                r_redis_conn_ls.append(redis_conn)

        all_deviceIP_sessions = r_redis_conn_ls[0]['redis_conn'].hget('acos_sessions', deviceIP)
        all_deviceIP_sessions_dict = {}
        if all_deviceIP_sessions is None:
            all_deviceIP_sessions_dict.setdefault(local_ip, {'session_id': sessionid})
        else:
            all_deviceIP_sessions_dict = json.loads(all_deviceIP_sessions)
            if all_deviceIP_sessions is None or local_ip not in all_deviceIP_sessions_dict.keys():
                all_deviceIP_sessions_dict.setdefault(local_ip, {'session_id': sessionid})
            else:
                all_deviceIP_sessions_dict[local_ip] = {'session_id': sessionid}
        for w_redis_conn in w_redis_conn_ls:
                w_redis_conn["redis_conn"].hset('acos_sessions', deviceIP, json.dumps(all_deviceIP_sessions_dict))

    def check_session_invalid(self, sessionID, deviceIP):
        if sessionID is None:
            return False

        url = "https://" + deviceIP + "/services/rest/V2/?session_id=" + sessionID +\
              "&method=slb.virtual_server.getAll&format=json"
        tmp_result = self.request_get(url)
        if int(tmp_result["code"]) == 0 and "Invalid session ID" not in str(tmp_result["message"]):
            return True
        return False

    def request_get(self, url):
        result = Result(0).get_result()
        try:
            #https请求,禁用https ssl警告
            if url.startswith("https://"):
                session = requests.Session()
                session.mount("https://", MyAdapter())
                requests.packages.urllib3.disable_warnings()
                req = session.get(url, verify=False)
                result["message"] = req.json()
                if "response" in result["message"].keys():
                    result["code"] = 199
                    result["status"] = False
            else:
                req = requests.get(url)
                result["message"] = req.json()
        except Exception as e:
            print e
            return Result(199).get_result("make request error! error info : " + str(e))
        return result