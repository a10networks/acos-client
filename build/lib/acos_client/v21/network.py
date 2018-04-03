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


class Network(base.BaseV21):

    @property
    def interface(self):
        return self.Interface(self.client)

    class Interface(base.BaseV21):

        def all(self):
            return self._get('network.interface.getAll')

        def get(self, port_num):
            return self._get('network.interface.get', {"port_num": port_num})

        def set(self, port_num, **kwargs):

            params = {
                "interface": {
                    "port_num": port_num
                }
            }
            return self._post('network.interface.set', params, **kwargs)

        @property
        def ipv4(self):
            return self.IPV4(self.client)

        class IPV4(base.BaseV21):

            def _set(self, action, port_num, ipv4_address, ipv4_mask,
                     **kwargs):

                params = {
                    "interface": {
                        "ipv4": {
                            "ipv4_address": ipv4_address,
                            "ipv4_mask": ipv4_mask
                        },
                        "port_num": port_num
                    }
                }

                return self._post(action, params, **kwargs)

            def all_delete(self, port_num, **kwargs):
                return self._post('network.interface.ipv4.deleteAll',
                                  {"port_num": port_num}, **kwargs)

            def add(self, port_num, ipv4_address, ipv4_mask, **kwargs):
                return self._set('network.interface.ipv4.add', port_num,
                                 ipv4_address, ipv4_mask, **kwargs)

            def delete(self, port_num, ipv4_address, ipv4_mask, **kwargs):
                return self._set('network.interface.ipv4.delete', port_num,
                                 ipv4_address, ipv4_mask, **kwargs)

    @property
    def acl(self):
        return self.ACL(self.client)

    class ACL(base.BaseV21):

        @property
        def ext(self):
            return self.Ext(self.client)

        class Ext(base.BaseV21):

            # Protocols
            ICMP = 0
            IP = 1
            TCP = 2
            UDP = 3

            def _set(self, action, id, acl_item_list, **kwargs):

                params = {
                    "ext_acl": {
                        "id": id,
                        'acl_item_list': acl_item_list
                    }
                }

                # silently fails if 'acl_item_list' is empty
                return self._post(action, params, **kwargs)

            def all(self):
                return self._get('network.acl.ext.getAll')

            def search(self, id):
                # FIXME not working
                return self._get('network.acl.ext.search', {"id": id})

            def create(self, id, acl_item_list, **kwargs):
                return self._set('network.acl.ext.create', id, acl_item_list,
                                 **kwargs)

            def update(self, id, acl_item_list, **kwargs):
                return self._set('network.acl.ext.update', id, acl_item_list,
                                 **kwargs)  # FIXME NOT WORKING

            def delete(self, id):
                # FIXME NOT WORKING
                return self._post('network.acl.ext.delete', {"id": id})

            def all_delete(self, **kwargs):
                return self._get('network.acl.ext.deleteAll', **kwargs)

    @property
    def route(self):
        return self.Route(self.client)

    class Route(base.BaseV21):

        def _set(self, action, address, mask, gateway, distance, **kwargs):
            params = {
                'address': address,
                'mask': mask,
                'gateway': gateway,
                'distance': distance
            }
            return self._post(action, params, **kwargs)

        def ipv4_all(self, **kwargs):
            return self._get('network.route.ipv4static.getAll', **kwargs)

        def ipv4_create(self, address, mask, gateway, distance, **kwargs):
            return self._set('network.route.ipv4static.create', address, mask,
                             gateway, distance, **kwargs)

        def ipv4_update(self, address, mask, gateway, distance, **kwargs):
            return self._set('network.route.ipv4static.update', address, mask,
                             gateway, distance, **kwargs)  # FIXME NOT WORKING

        def ipv4_delete(self, address, mask, gateway, distance, **kwargs):
            return self._set('network.route.ipv4static.delete', address, mask,
                             gateway, distance, **kwargs)  # FIXME NOT WORKING

    @property
    def arp(self):
        return self.Arp(self.client)
    class Arp(base.BaseV21):
        def _set(self, action, ip_version, **kwargs):
            params = {
                    'ip_version': ip_version
                    }
            return self._post(action, params, **kwargs)
        def arp_all(self, ip_version, **kwargs):
            return self._set('network.arp.fetchAllStatistics', ip_version, **kwargs)
