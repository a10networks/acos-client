
import acos_client.v21.base as base

class Port(base.BaseV21):

    # Protocols
    TCP = 2
    UDP = 3

    def _set(self, action, name, port_num, protocol, **kwargs):

        params = {
            "name": name,
            "port": { "port_num": port_num,
                      "protocol": protocol,
                      }
        }

        return self._post(action, params, **kwargs)

    def create(self, name, port_num, protocol, **kwargs):
        return self._set("slb.server.port.create", name, port_num, protocol, **kwargs)

    def update(self, name, port_num, protocol, **kwargs):
        return self._set("slb.server.port.update", name, port_num, protocol, **kwargs)

    def all_update(self, name, port_num, protocol, **kwargs):
        return self._set("slb.server.port.updateAll", name, port_num, protocol, **kwargs)

    def delete(self, name, port_num, protocol, **kwargs):
        self._set("slb.server.port.delete", name, port_num, protocol, **kwargs)

    def all_delete(self, name, **kwargs):
        self._get("slb.server.port.deleteAll",  {"name": name}, **kwargs)
