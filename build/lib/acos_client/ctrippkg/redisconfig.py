#!/usr/bin/env python
#! -*- coding: utf-8 -*-

__author__ = 'wenjiexu'

from result import Result

#设置运行环境和redis 配置url
SYSTEMCONFIG = {
    "host": "http://ws.fx.uat.qa.nt.ctripcorp.com/credis/configapi/getcluster/OPS_VS_LB",
    "dbno": 0
}

DJANGO_ENV = "UAT"

import json
import copy
import time

from django.core.mail import send_mail
import redis
import requests

class RedisConfig():
    redis_server_option = {
        "host": "",
        "port": "",
        "dbno": "",
        "isMaster": "" #master True只可写不可读, False只可读不可写
    }
    redis_conn_option = {
        "isMaster": "",
        "redis_conn": ""
    }

    def __init__(self,):
        pass

    def get_redis_servers(self, isMaster_type="BOTH"):
        #isMaster_type 可能的值True, False, BOTH
        result = []
        conf_url = SYSTEMCONFIG["host"]
        try:
            r = requests.get(conf_url)
            redis_json = r.json()
        except Exception as e:
            return Result(150).get_result(conf_url+" message: "+e.__unicode__().encode('utf-8'))

        if "Servers" not in redis_json.keys():
            return Result(151).get_result()

        if DJANGO_ENV.upper() != "PRODUCT":
            # uat env
            for server in redis_json["Servers"]:
                tmp_redis_w = copy.deepcopy(self.redis_server_option)
                tmp_redis_w["host"] = server["IPAddress"]
                tmp_redis_w["port"] = server["Port"]
                tmp_redis_w["dbno"] = SYSTEMCONFIG["dbno"]
                tmp_redis_w["isMaster"] = True
                tmp_redis_r = copy.deepcopy(tmp_redis_w)
                tmp_redis_r["isMaster"] = False

                if isMaster_type == "BOTH":
                    result.append(tmp_redis_r)
                    result.append(tmp_redis_w)
                elif (isinstance(isMaster_type, bool) and not isMaster_type):
                    result.append(tmp_redis_r)
                else:
                    result.append(tmp_redis_w)
                return result
        else:
            # pro env
            redis_w_ls = []
            redis_r_ls = []
            for server in redis_json["Servers"]:
                tmp_redis_pro = copy.deepcopy(self.redis_server_option)
                tmp_redis_pro["host"] = server["IPAddress"]
                tmp_redis_pro["port"] = server["Port"]
                tmp_redis_pro["dbno"] = server["DBNumber"]
                tmp_redis_pro["isMaster"] = True if server["ParentID"] == 0 else False
                if (isinstance(isMaster_type, bool)):
                    if server["ParentID"] != 0:
                        redis_r_ls.append(tmp_redis_pro)
                    else:
                        redis_w_ls.append(tmp_redis_pro)
                else:
                    result.append(tmp_redis_pro)
            if isinstance(isMaster_type, bool):
                result = redis_w_ls if isMaster_type else redis_r_ls
        return result

    def get_redis_connection(self, isMaster="BOTH"):
        redis_server_ls = self.get_redis_servers(isMaster)
        if isinstance(redis_server_ls, dict) and redis_server_ls["code"] != 0:
            return redis_server_ls
        result = Result(0).get_result()
        redis_conn_ls = []
        if redis_server_ls == []:
            return Result(153).get_result()
        for redis_server in redis_server_ls:
            try:
                tmp_redis_conn = copy.deepcopy(self.redis_conn_option)
                redis_conn = redis.StrictRedis(host=redis_server["host"], port=redis_server["port"], db=redis_server['dbno'])
                # 没什么用，只是为了验证redis_conn是否有效
                redis_conn.dbsize()
                tmp_redis_conn["isMaster"] = redis_server["isMaster"]
                tmp_redis_conn["redis_conn"] = redis_conn
                redis_conn_ls.append(tmp_redis_conn)
            except Exception as e:
                msg = Result(199).get_result("connection redis server {0} error! info: {1}".format(str(redis_server), e.__unicode__().encode('utf-8')))
                send_mail(subject="Connection redis server error!",
                          message=json.dumps(msg),
                          from_email='Calabash API',
                          recipient_list=['wenjiexu@ctrip.com', ],
                          fail_silently=False,
                          connection=None)
                return msg
        result["message"] = redis_conn_ls
        return result

    def read_redis_by_key(self, _key1=None, _key2="data"):
        redis_conn_ls = self.get_redis_connection(False)
        if redis_conn_ls["code"] != 0 or (redis_conn_ls["code"] == 0 and not isinstance(redis_conn_ls["message"], list)):
            return redis_conn_ls
        data = None
        result = {}
        for redis_conn in redis_conn_ls:
            data = redis_conn["redis_conn"].hget(_key1, _key2)
            update_time = redis_conn["redis_conn"].hget(_key1, "update_time")
            break
        if data is None:
            data = ["redis server doesn\'t exist the key: "+_key1]
            update_time = ""
        result.setdefault("data", data)
        result.setdefault("update_time", update_time)
        return result

    def write_redis(self, _key1=None, _key2="data", data=None):
        if _key1 is None:
            return Result(155).get_result()
        if data is None:
            return Result(156).get_response()
        else:
            redis_conn_ls = self.get_redis_connection(True)
            if redis_conn_ls["code"] != 0 or (redis_conn_ls["code"] == 0 and not isinstance(redis_conn_ls["message"], list)):
                return redis_conn_ls
            for redis_conn in redis_conn_ls:
                redis_conn["redis_conn"].hset(_key1, _key2, json.dumps(data))
                redis_conn["redis_conn"].hset(_key1, 'update_time', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            return Result(0).get_result()