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
import acos_client.v21.base as base


class BasePersistence(base.BaseV21):

    def __init__(self):
        self.prefix = "slb.template.%s_persistence" % self.pers_type

    def get(self, name):
        return self.http.post(self.url("%s.search" % self.prefix),
                              {'name': name})

    def exists(self, name):
        try:
            self.get(name)
            return True
        except acos_errors.NotFound as e:
            return False

    def create(self, name):
        self.http.post(self.url("%s.create" % self.prefix),
                       self.get_params(name))

    def delete(self, name):
        self.http.post(self.url("%s.delete" % self.prefix), {'name': name})


class CookiePersistence(BasePersistence):

    def __init__(self):
        self.pers_type = 'cookie'
        super(CookiePersistence, self).__init__()

    def get_params(self, name):
        return {
            "cookie_persistence_template": {
                "name": name
            }
            # "cookie_persistence_template": {
            #     "name": name,
            #     "expire_exist": 0,
            #     "expire": 3600,
            #     "cookie_name": "",
            #     "domain": "",
            #     "path": "",
            #     "match_type": 0,
            #     "match_all": 0,
            #     "insert_always": 0,
            #     "dont_honor_conn": 0
            # }
        }


class SourceIpPersistence(base.BaseV21):

    def __init__(self):
        self.pers_type = 'src_ip'
        super(CookiePersistence, self).__init__()

    def get_params(self, name):
        return {
            "src_ip_persistence_template": {
                "name": name
            }
            # "src_ip_persistence_template": {
            #     "name": name,
            #     "match_type": 1,
            #     "match_all": 0,
            #     "timeout": 1800,
            #     "no_honor_conn": 0,
            #     "incl_sport": 0,
            #     "include_dstip": 0,
            #     "hash_persist": 0,
            #     "enforce_high_priority": 0,
            #     "netmask": "255.255.255.255",
            #     "netmask6": 96
            # }
        }
