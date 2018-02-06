import acos_client.v21.base as base


class Zone_Service(base.BaseV21):

    enable = 1
    disable = 0

    def _set(self, action, zone_name, service_domain_name, port_num, policy, name, static, weight, **kwargs):

        params = {
            "zone_name": zone_name,
            "service": {
                "name": service_domain_name,
                "port": port_num,
                "policy": policy,
                "dns_address_record_list":[
                    {
                        "vip_order": name,
                        "static": static,
                        "weight": weight,
                    }
                ]
            }
        }

        return self._post(action, params, **kwargs)


    def create(self, zone_name, service_domain_name, port_num, policy, name, static, weight, **kwargs):
        return self._set('gslb.zone.service.create', zone_name, service_domain_name, port_num, policy, name, static, weight,
                         **kwargs)

    def update(self, zone_name, service_domain_name, port_num, policy, name, static, weight, **kwargs):
        return self._set('gslb.zone.service.update', zone_name, service_domain_name, port_num, policy, name, static, weight,
                         **kwargs)

    def delete(self, zone_name, service_domain_name, port_num, **kwargs):
        params = {
            "zone_name": zone_name,
            "service": {
                "name": service_domain_name,
                "port": port_num,
            }
        }

        return self._post('gslb.zone.service.delete', params, **kwargs)