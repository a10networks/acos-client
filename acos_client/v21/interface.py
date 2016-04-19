# Copyright 2016, A10 Networks
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

import base


class Interface(base.BaseV21):
    def get_list(self):
        raise NotImplementedError("Not implemented in AXAPI v2.1")

    def get(self, ifnum=None):
        raise NotImplementedError("Not implemented in AXAPI v2.1")

    def delete(self, ifnum):
        raise NotImplementedError("Not implemented in AXAPI v2.1")

    def create(self, ifnum, ip_address=None, ip_netmask=None, dhcp=False, enable=None,
               speed="auto"):
        raise NotImplementedError("Not implemented in AXAPI v2.1")

    def update(self, ifnum, ip_address=None, ip_netmask=None, dhcp=False, enable=None,
               speed="auto"):
        raise NotImplementedError("Not implemented in AXAPI v2.1")

    @property
    def ethernet(self):
        return EthernetInterface(self.client)

    @property
    def management(self):
        return ManagementInterface(self.client)


class EthernetInterface(Interface):
    pass


class ManagementInterface(Interface):
    pass
