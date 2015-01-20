import base

class Admin(base.BaseV21):

    @property
    def administrator(self):
        return self.Administrator(self.client)

    class Administrator(base.BaseV21):

        def all(self, **kwargs):
            return self._get('system.admin.administrator.getAll', **kwargs)

        def get(self, name, **kwargs):
            params = {"admin_name": name}
            return self._post('system.admin.administrator.search', params, **kwargs)

        def create(self, name, **kwargs):
            params = {
                "administrator": {
                    "admin_name": name
                }
            }

            return self._post('system.admin.administrator.create', params, **kwargs)

        def update(self, name, **kwargs):
            params = {
                "administrator": {
                    "admin_name": name
                }
            }

            return self._post('system.admin.administrator.update', params, **kwargs)


        def delete(self, name, **kwargs):
            params = {"admin_name": name }
            return self._post('system.admin.administrator.delete', params, **kwargs)

        def all_delete(self, **kwargs):
            return self._post('system.admin.administrator.deleteAll', **kwargs)

