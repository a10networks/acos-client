# Copyright 2014,  Jeff Buttars,  A10 Networks.
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
import json


class Session(object):

    def __init__(self, client, username, password):
        self.client = client
        self.http = client.http
        self.username = username
        self.password = password
        self.session_id = None
        self.headers = {
            'Content-type': 'application/json',
        }

    @property
    def id(self):
        if self.session_id is None:
            self.authenticate(self.username, self.password)
        return self.session_id

    def authenticate(self, username, password):
        url = "/axapi/v3/auth"
        headers = {'Content-type': 'application/json'}
        payload = json.dumps(
            {'credentials': {
                "username": username,
                "password": password
                }
             }
        )

        if self.session_id is not None:
            self.close()

        r = self.http.post(url, payload, headers=headers)
        # print "RESPONSE ", r
        # print "RESPONSE ", dir(r)
        # response = json.loads(str(r))

        self.session_id = r.get('session_id', '')
        self.headers['Authorization'] = "A10 %s" % self.session_id

        return r

    def close(self):
        try:
            self.client.partition.active()
        except Exception:
            pass

        try:
            url = "/axapi/v3/logoff"
            r = self.http.post(url, "", headers=self.headers)
        finally:
            self.session_id = None

        return r
