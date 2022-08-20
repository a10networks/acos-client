from __future__ import absolute_import
from __future__ import unicode_literals

from acos_client import errors as acos_errors
from acos_client.v30 import base


class Inside(base.BaseV30):
    @property
    def source(self):
        return self.Source(self.client)

    class Source(base.BaseV30):
        url_prefix = "/ip/nat/inside/source/list"

        def all(self):
            return self._get(self.url_prefix)

        def get_id_list(self, acl_id):
            return self._get("%s/acl-id-list/%s" % (
                self.url_prefix,
                acl_id
            ))

        def create_id_list(self, acl_id, pool):
            return self._post("%s/acl-id-list" % self.url_prefix, {
                'acl-id-list': {
                    'acl-id': acl_id,
                    'pool': pool,
                }
            })

        def delete_id_list(self, acl_id):
            return self._delete("%s/acl-id-list/%s" % (
                self.url_prefix,
                acl_id
            ))
