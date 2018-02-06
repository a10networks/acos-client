
import acos_client.v21.base as base

class Zone(base.BaseV21):

    def get(self, name, **kwargs):
        return self._post("gslb.zone.search", {'name': name}, **kwargs)

    def create(self, name, ttl, **kwargs):
        params = {
            "zone": {
                "name": name,
                "ttl": ttl,
            }
        }
        self._post("gslb.zone.create", params, **kwargs)

    def delete(self, name, **kwargs):
        self._post("gslb.zone.delete", {"name": name}, **kwargs)

    def all(self, **kwargs):
        return self._get('gslb.zone.getAll', **kwargs)

    def update(self, name, ttl, **kwargs):
        params = {
            "zone": {
                "name": name,
                "ttl": ttl,
            }
        }
        self._post("gslb.zone.update", params, **kwargs)