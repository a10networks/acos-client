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

import test_base

class TestSystem(test_base.UnitTestBase):
    pass

    # def test_information(self):
    #     self.c.system.information()
    #     self.assertEqual(2, self.c.http_client._http.call_count)
    #     self.c.http_client._http.assert_called_with(
    #         'GET',
    #         '/services/rest/v2.1/?format=json&session_id=session0&'
    #         'method=system.information.get',
    #         None)
