
from acos_client.multipart import Multipart
import base

class ClassList(base.BaseV21):


    def _fix_json(self, data):
        import re,json
        p = re.compile(r'(?<=[^:{\[,])"(?![:,}\]])')
        return json.loads(re.sub(p, '\\"', data))

    def all(self, **kwargs):
        return self._fix_json(self._get("slb.class_list.getAll", **kwargs))

    def get(self, name, **kwargs):
        return self._fix_json(self._post("slb.class_list.search", {'name': name},
                          **kwargs))

    def download(self, name, **kwargs):
        return self._post('slb.class_list.download', params={'file_name': name}, **kwargs)

    def upload(self, name, class_list, **kwargs):
        m = Multipart()
        m.file(name=name, filename=name, value=class_list)
        ct, payload = m.get()
        kwargs.update(payload=payload, headers={'Content-Type': ct})
        return self._post('slb.class_list.upload', **kwargs)

    def _set(self, action, class_list, **kwargs):
        return self._post(action, class_list, **kwargs)

    def create(self, class_list, **kwargs):
        return self._set("slb.class_list.create", class_list, **kwargs)

    def update(self, class_list, **kwargs):
        return self._set("slb.class_list.update", class_list, **kwargs)

    def delete(self, name, **kwargs):
        self._post("slb.class_list.delete", {"name": name}, **kwargs)

