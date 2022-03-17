from __future__ import absolute_import
from __future__ import unicode_literals

from acos_client import errors as acos_errors
from acos_client.v30 import base


class AccessList(base.BaseV30):
    url_prefix = "/access-list"

    def list(self, **kwargs):
        return self._get(self.url_prefix, axapi_args=kwargs)
