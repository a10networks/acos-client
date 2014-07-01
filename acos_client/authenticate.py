# vim: tabstop=4 shiftwidth=4 softtabstop=4

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

class Authenticate(object):

    def __init__(self, client):
        self.client = client
        #self.session_id = self.authenticate(username, password)['session_id']

    def authenticate(self, username, password):
        url = "/services/rest/v2.1/?format=json&method=authenticate"
        params = {
            "username": username,
            "password": password
        }

        r = self.client.http.axapi_http("POST", auth_url, params) #yikes
        return r
