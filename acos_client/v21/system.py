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


class System(object):

    def __init__(self, http_client, session):
        self.http_client = http_client
        self.session = session

    def information(self):
        url = ("/services/rest/v2.1/?format=json&session_id=%s"
               "&method=system.information.get" % self.session.id)
        return self.http_client.request("GET", url)


    def write_memory(self, tenant_id=""):
        return self.send(tenant_id=tenant_id,
                         method="GET",
                         url=(
                             "/services/rest/v2.1/?format=json&method=system"
                             ".action"
                             ".write_memory&session_id=%s" % self.session_id),
                         partition_ax=False,
                         close_session_after_request=False)

