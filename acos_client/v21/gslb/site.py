
import acos_client.v21.base as base

class Site(base.BaseV21):

    def get(self, name, **kwargs):
        return self._post("gslb.site.search", {'name': name}, **kwargs)

    def create(self, name, **kwargs):
        params = {
            "gslb_site": {
                "name": name,
            }
        }
        self._post("gslb.site.create", params, **kwargs)

    def delete(self, name, **kwargs):
        self._post("gslb.site.delete", {"name": name}, **kwargs)

    def all(self, **kwargs):
        return self._get('gslb.site.getAll', **kwargs)

    def create_ip_server(self, name, vip_server_name, **kwargs):
        params = {
            "name": name,
            "ip_server":
                {
                    "name": vip_server_name
                }
        }
        self._post("gslb.site.ip_server.create", params, **kwargs)

    def delete_ip_server(self, name, vip_server_name, **kwargs):
        params = {
            "name": name,
            "ip_server":
                {
                    "name": vip_server_name
                }
        }
        self._post("gslb.site.ip_server.delete", params, **kwargs)