# Copyright (C) 2016, A10 Networks Inc. All rights reserved.

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
from __future__ import absolute_import
from __future__ import unicode_literals

from acos_client.v21 import base


class LicenseManager(base.BaseV21):
    """v2.1 LicenseManager is not yet supported"""
    def create(self, host_list=[], serial=None, instance_name=None, use_mgmt_port=False,
               interval=None, bandwidth_base=None, bandwidth_unrestricted=None):
        raise NotImplementedError("LicenseManager is not yet supported using AXAPI v2.1")

    def get(self):
        raise NotImplementedError("LicenseManager is not yet supported using AXAPI v2.1")

    def connect(self, connect=False):
        raise NotImplementedError("LicenseManager is not yet supported using AXAPI v2.1")

    def update(self, host_list=[], serial=None, instance_name=None, use_mgmt_port=False,
               interval=None, bandwidth_base=None, bandwidth_unrestricted=None):
        raise NotImplementedError("LicenseManager is not yet supported using AXAPI v2.1")
