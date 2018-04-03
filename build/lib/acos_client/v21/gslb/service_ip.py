
import acos_client.v21.base as base

from port import Port


class Service_IP(base.BaseV21):

    def get(self, name, **kwargs):
        return self._post("gslb.service_ip.search", {'name': name}, **kwargs)

    def create(self, name, ip_address, **kwargs):
        params = {
            "service_ip": {
                "name": name,
                "ip_address": ip_address,
                "status": kwargs.get('status', 1)
            }
        }
        self._post("gslb.service_ip.create", params, **kwargs)

    def update(self, name, ip_address, **kwargs):
        params = {
            "service_ip": {
                "name": name,
                "ip_address": ip_address,
                "status": kwargs.get('status', 1)
            }
        }
        self._post("gslb.service_ip.update", params, **kwargs)

    def delete(self, name, **kwargs):
        self._post("gslb.service_ip.delete", {"name": name}, **kwargs)

    def all(self, **kwargs):
        return self._get('gslb.service_ip.getAll', **kwargs)


    @property
    def port(self):
        return Port(self.client)
