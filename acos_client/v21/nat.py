
import base

class Nat(base.BaseV21):
    @property
    def pool(self):
        return self.Pool(self.client)

    class Pool(base.BaseV21):
        def _set(self, action, name, start_ip, end_ip, mask, **kwargs):
            params = {
                'name': name,
                'start_ip_addr': start_ip,
                'end_ip_addr': end_ip,
                'netmask': mask,
            }
            return self._post(action, params, **kwargs)

        def all(self):
            return self._get('nat.pool.getAll')

        def create(self, name, start_ip, end_ip, mask, **kwargs):
            return self._set('nat.pool.create', name, start_ip, end_ip, mask, **kwargs)

        def update(self, name, start_ip, end_ip, mask, **kwargs):
            return self._set('nat.pool.create', name, start_ip, end_ip, mask, **kwargs)

        def delete(self, name, **kwargs):
            return self._post('nat.pool.delete', {"name": name}, **kwargs)

        def stats(self, name, **kwargs):
            return self._post('nat.pool.fetchStatistics', {"name": name}, **kwargs)

        def all_stats(self, **kwargs):
            return self._get('nat.pool.fetchALLStatistics',**kwargs)
