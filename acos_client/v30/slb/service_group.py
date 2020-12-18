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
from __future__ import absolute_import
from __future__ import unicode_literals

from acos_client.v30 import base
from acos_client.v30.slb.member import Member


class ServiceGroup(base.BaseV30):
    url_prefix = '/slb/service-group/'

    @property
    def member(self):
        return Member(self.client)

    # Valid LB methods
    ROUND_ROBIN = 'round-robin'
    WEIGHTED_ROUND_ROBIN = 'weighted-rr'
    LEAST_CONNECTION = 'least-connection'
    WEIGHTED_LEAST_CONNECTION = 'weighted-least-connection'
    LEAST_CONNECTION_ON_SERVICE_PORT = 'service-least-connection'
    WEIGHTED_LEAST_CONNECTION_ON_SERVICE_PORT = \
        'service-weighted-least-connection'
    FAST_RESPONSE_TIME = 'fastest-response'
    LEAST_REQUEST = 'least-request'
    STRICT_ROUND_ROBIN = 'round-robin-strict'
    STATELESS_SOURCE_IP_HASH = 'stateless-src-ip-hash'
    STATELESS_SOURCE_IP_HASH_ONLY = 'stateless-src-ip-only-hash'
    STATELESS_DESTINATION_IP_HASH = 'stateless-dst-ip-hash'
    STATELESS_SOURCE_DESTINATION_IP_HASH = 'stateless-src-dst-ip-hash'
    STATELESS_PER_PACKET_ROUND_ROBIN = 'stateless-per-pkt-round-robin'
    SOURCE_IP_HASH_ONLY = 'src-ip-only-hash'
    SOURCE_IP_HASH = 'src-ip-hash'
    DESTINATION_IP_HASH_ONLY = 'dst-ip-only-hash'
    DESTINATION_IP_HASH = 'dst-ip-hash'

    # Valid protocols
    TCP = 'tcp'
    UDP = 'udp'

    def _set(self, name, protocol=None, lb_method=None, service_group_templates=None,
             hm_name=None, mem_list=None, health_check_disable=False, health_check=None,
             hm_delete=False, **kwargs):

        # Normalize "" -> None for json
        hm_name = hm_name or None

        # v30 needs unit tests badly...

        params = {
            "service-group": self.minimal_dict({
                "name": name,
                "protocol": protocol,
                "member-list": mem_list
            })
        }

        # If we explicitly disable health checks, ensure it happens
        # Else, we implicitly disable health checks if not specified.
        health_check_disable = 1 if health_check_disable else 0

        # When enabling/disabling a health monitor, you can't specify
        # health-check-disable and health-check at the same time.
        if hm_name is None:
            params["service-group"]["health-check-disable"] = health_check_disable
            # Have to explicitly detach health monitor from the service group,
            # by setting hm_delete flag
            if hm_delete:
                params["service-group"]["health-check"] = health_check
        else:
            params["service-group"]["health-check"] = hm_name

        if lb_method is None:
            pass
        elif lb_method[-16:] == 'least-connection':
            params['service-group']['lc-method'] = lb_method
            params['service-group']['stateless-auto-switch'] = 0
        elif lb_method[:9] == 'stateless':
            params['service-group']['stateless-lb-method'] = lb_method
        else:
            params['service-group']['lb-method'] = lb_method
            params['service-group']['stateless-auto-switch'] = 0

        if service_group_templates:
            service_group_templates = {k: v for k, v in service_group_templates.items() if v}

            if service_group_templates.get('template-policy'):
                params['service-group']['template-policy'] = service_group_templates['template-policy']
            elif service_group_templates.get('template-policy-shared'):
                params['service-group']['template-policy-shared'] = service_group_templates['template-policy-shared']
                params['service-group']['shared-partition-policy-template'] = True

            params['service-group']['template-server'] = service_group_templates.get('template-server', None)
            params['service-group']['template-port'] = service_group_templates.get('template-port', None)

        return params

    def all(self, max_retries=None, timeout=None, *args, **kwargs):
        return self._get(self.url_prefix, max_retries=max_retries, timeout=timeout, axapi_args=kwargs)

    def all_stats(self, max_retries=None, timeout=None, *args, **kwargs):
        return self._get(self.url_prefix + "stats", max_retries=max_retries, timeout=timeout, axapi_args=kwargs)

    def all_oper(self, max_retries=None, timeout=None, *args, **kwargs):
        return self._get(self.url_prefix + "oper", max_retries=max_retries, timeout=timeout, axapi_args=kwargs)

    def create(self, name, protocol=TCP, lb_method=ROUND_ROBIN, service_group_templates=None,
               mem_list=None, hm_name=None, max_retries=None, timeout=None, health_check_disable=False,
               health_check=None, **kwargs):
        params = self._set(name, protocol=protocol, lb_method=lb_method,
                           service_group_templates=service_group_templates,
                           mem_list=mem_list, hm_name=hm_name, health_check_disable=health_check_disable,
                           health_check=health_check, **kwargs)
        return self._post(self.url_prefix, params, max_retries=max_retries, timeout=timeout, axapi_args=kwargs)

    def delete(self, name):
        return self._delete(self.url_prefix + name)

    def get(self, name, max_retries=None, timeout=None, **kwargs):
        return self._get(self.url_prefix + name, max_retries=max_retries, timeout=timeout, axapi_args=kwargs)

    def oper(self, name, max_retries=None, timeout=None, *args, **kwargs):
        return self._get(self.url_prefix + name + "/oper", max_retries=max_retries, timeout=timeout,
                         axapi_args=kwargs)

    def stats(self, name, max_retries=None, timeout=None, *args, **kwargs):
        return self._get(self.url_prefix + name + "/stats", max_retries=max_retries, timeout=timeout,
                         axapi_args=kwargs)

    def update(self, name, protocol=None, lb_method=None, health_monitor=None,
               service_group_templates=None, mem_list=None, hm_name=None,
               max_retries=None, timeout=None, health_check_disable=False, health_check=None,
               hm_delete=False, **kwargs):
        params = self._set(name, protocol=None, lb_method=lb_method, hm_name=hm_name,
                           service_group_templates=service_group_templates,
                           mem_list=mem_list, health_check_disable=health_check_disable,
                           health_check=health_check, hm_delete=hm_delete, **kwargs)
        return self._post(self.url_prefix + name, params, max_retries=max_retries, timeout=timeout,
                          axapi_args=kwargs)

    def replace(self, name, protocol=None, lb_method=None, health_monitor=None,
                service_group_templates=None, mem_list=None, hm_name=None,
                max_retries=None, timeout=None, health_check_disable=False, health_check=None,
                **kwargs):
        params = self._set(name, protocol=protocol, lb_method=lb_method, hm_name=hm_name,
                           service_group_templates=service_group_templates,
                           mem_list=mem_list, health_check_disable=health_check_disable,
                           health_check=health_check, **kwargs)
        return self._put(self.url_prefix + name, params, max_retries=max_retries, timeout=timeout,
                         axapi_args=kwargs)
