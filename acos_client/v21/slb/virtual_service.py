
import acos_client.v21.base as base

class VirtualService(base.BaseV21):

    def all(self, **kwargs):
        return self._get("slb.virtual_service.getAll", **kwargs)

    def get(self, name, **kwargs):
        return self._post("slb.virtual_service.search", {'name': name},
                          **kwargs)

    def _set(self, action, name, protocol, port, **kwargs):
        params = {
            "virtual_service": {
                "port": port,
                "protocol": protocol,
                "name": name
            }
        }

        return self._post(action, params, **kwargs)

    def create(self, name, protocol, port, **kwargs):
        return self._set("slb.virtual_service.create", name, protocol, port, **kwargs)

    def update(self, name, protocol, port, **kwargs):
        return self._set("slb.virtual_service.update", name, protocol, port, **kwargs)

    def delete(self, name, **kwargs):
        return self._post("slb.virtual_service.delete", {"name": name}, **kwargs)

    def all_delete(self, **kwargs):
        return self._get("slb.virtual_service.deleteAll", **kwargs)

    def stats(self, name, **kwargs):
        return self._post("slb.virtual_service.fetchStatistics", {"name": name},
                          **kwargs)

    def all_stats(self, **kwargs):
        return self._get("slb.virtual_service.fetchAllStatistics",**kwargs)
