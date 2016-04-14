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

import time

import acos_client.errors as acos_errors

import base

INTERVAL_MONTHLY = 1
INTERVAL_DAILY = 2
INTERVAL_HOURLY = 3

DEFAULT_LICENSE_PORT = 443


class LicenseManager(base.BaseV30):

    url_base = "/license-manager"

    def create(self, host_list=[], serial=None, instance_name=None,  use_mgmt_port=False,
               interval=None, bandwidth_base=None, bandwidth_unrestricted=None):
        """Creates a license manager entry

        Keyword arguments:
        instance_name -- license manager instance name
        host_list -- list(dict) a list of dictionaries of the format:
            {'ip': '127.0.0.1', 'port': 443}
        serial - (str) appliance serial number
        use_mgmt_port - (bool) use management for license interactions
        interval - (int) 1=Monthly, 2=Daily, 3=Hourly
        bandwidth_base - (int) Configure feature bandwidth base (Mb)
            Valid range - 10-102400
        bandwidth_unrestricted - (bool) Set the bandwidth to maximum
        """
        payload = self._build_payload(host_list=host_list, serial=serial,
                                      instance_name=instance_name,
                                      use_mgmt_port=use_mgmt_port,
                                      interval=interval, bandwidth_base=bandwidth_base,
                                      bandwidth_unrestricted=bandwidth_unrestricted)
        return self._post(self.url_base, payload)

    def update(self, host_list=[], serial=None, instance_name=None, use_mgmt_port=False,
               interval=None, bandwidth_base=None, bandwidth_unrestricted=None):
        """Update a license manager entry

        Keyword arguments:
        instance_name -- license manager instance name
        host_list -- list(dict) a list of dictionaries of the format:
            {'ip': '127.0.0.1', 'port': 443}
        serial - (str) appliance serial number
        use_mgmt_port - (bool) use management for license interactions
        interval - (int) 1=Monthly, 2=Daily, 3=Hourly
        bandwidth_base - (int) Configure feature bandwidth base (Mb)
            Valid range - 10-102400
        bandwidth_unrestricted - (bool) Set the bandwidth to maximum
        """

        return self.create(host_list=host_list, serial=serial, instance_name=instance_name,
                           use_mgmt_port=use_mgmt_port,
                           interval=interval, bandwidth_base=bandwidth_base,
                           bandwidth_unrestricted=bandwidth_unrestricted)

    def get(self):
        return self._get(self.url_base)

    def connect(self, connect=False):
        url = self.url_base + "/connect"
        payload = {
            "connect": {
                "connect": 1 if connect else 0,
            }
        }
        return self._post(url, payload)

    def _build_payload(self, host_list=[], serial=None, instance_name=None, use_mgmt_port=False,
                       interval=None, bandwidth_base=None, bandwidth_unrestricted=None):
        rv = {"license-manager": {}}
        if host_list:
            for x in host_list:
                hosts = []
                hosts.append(self._build_host_entry(x["ip"], x.get("port")))

            rv["license-manager"]["host-list"] = hosts

        self._set_if_set(instance_name, rv["license-manager"], "instance-name")
        self._set_if_set(serial, rv["license-manager"], "sn")
        self._set_if_set(use_mgmt_port, rv["license-manager"], "use-mgmt-port")
        self._set_if_set(interval, rv["license-manager"], "interval")
        self._set_if_set(bandwidth_base, rv["license-manager"], "bandwidth-base")
        self._set_if_set(bandwidth_unrestricted, rv["license-manager"], "bandwidth-unrestricted")

        return rv

    def _build_host_entry(self, ip, port=DEFAULT_LICENSE_PORT):
        return {"host-ipv4": ip, "port": port or DEFAULT_LICENSE_PORT}

    def _set_if_set(self, src, dest, dest_key):
        if src is not None:
            dest[dest_key] = src

    #
    # The method below, 'paygo', works more reliably than the axapi above.
    # But be forewarned, looking further might cause blindness.
    #

    def _paygo_setup(self, llp_hosts=[], sn=None, instance_name=None,
                     use_mgmt_port=False, interval=None, bandwidth_base=None):
        url = "/clideploy/"
        commands = []
        if use_mgmt_port:
            commands += ["license-manager use-mgmt-port"]
        for host in llp_hosts:
            commands += ["license-manager host %s" % host]
        commands += [
            "license-manager sn %s" % sn,
            "license-manager interval %s" % interval,
            "license-manager instance-name %s" % instance_name,
            "license-manager bandwidth-base %s" % bandwidth_base,
        ]
        payload = {
            "commandlist": commands
        }
        self._post(url, payload)

    def _paygo_connect(self):
        url = "/clideploy/"
        payload = {
            "commandlist": [
                "license-manager connect"
            ]
        }

        # There is some lag between the setup call above and being able
        # to successfully retrieve a license.

        for i in range(0, 60):
            try:
                return self._post(url, payload)
            except acos_errors.ACOSException as e:
                if 'Invalid message' in str(e):
                    time.sleep(5)
                    continue
                raise e

    def paygo(self, llp_hosts=[], sn=None, instance_name=None,
              use_mgmt_port=False, interval=None, bandwidth_base=None):

        for i in range(0, 4):
            self._paygo_setup(llp_hosts, sn, instance_name, use_mgmt_port,
                              interval, bandwidth_base)
            try:
                self._paygo_connect()
            except acos_errors.ACOSException as e:
                if 'Communication error' in str(e):
                    self.client.session.close()
                    time.sleep(5)
                    continue
                raise e
