
from acos_client.multipart import Multipart
import base

class Aflex(base.BaseV21):

    def _set(self, action, name, aflex, **kwargs):
        m = Multipart()
        m.file(name="upload_aflex", filename=name, value=aflex)
        ct, payload = m.get()
        kwargs.update(payload=payload, headers={'Content-Type': ct})
        return self._post(action, **kwargs)

    def upload(self,name, aflex, **kwargs):
        return self._set('slb.aflex.upload', name, aflex, **kwargs)

    def update(self, name, aflex, **kwargs):
        return self._set('slb.aflex.update', name, aflex, **kwargs)

    def all(self, **kwargs):
        return self._get('slb.aflex.getAll')

    def get(self, name, **kwargs):
        return self._post('slb.aflex.search', {'name': name},
                          **kwargs)

    def download(self, name, **kwargs):
        return self._post('slb.aflex.download', {'name': name},
                          **kwargs)

    def delete(self, name, **kwargs):
        self._post('slb.aflex.delete', {'name': name},
                          **kwargs)

    def stats(self, name, **kwargs):
        return self._post("slb.aflex.fetchStatistics", {"name": name},
                          **kwargs)

    def all_stats(self, **kwargs):
        return self._get("slb.aflex.fetchAllstatistics",**kwargs)

    def clear_stats(self, name, **kwargs):
        return self._post("slb.aflex.slb.aflex.clearStatistics", {"name": name},
                          **kwargs)

    def clear_all_stats(self, **kwargs):
        return self._post("slb.aflex.clearAllStatistics",**kwargs)

    def clear_events(self, name, event_name, **kwargs):
        params = {
                    "aflex_event": {
                        "name": name,
                        "event_name": event_name
                    }
        }

        return self._post("=slb.aflex.clearEvents", params,
                          **kwargs)

    def clear_all_events(self, **kwargs):
        return self._post("slb.aflax.clearAllEvents",**kwargs)
