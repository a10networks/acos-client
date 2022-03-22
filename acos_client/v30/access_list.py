from __future__ import absolute_import
from __future__ import unicode_literals

from acos_client import errors as acos_errors
from acos_client.v30 import base


class AccessList(base.BaseV30):
    url_prefix = "/access-list"

    def list(self, **kwargs):
        return self._get(self.url_prefix, axapi_args=kwargs)

    def get(self, id, **kwargs):
        return self._get("%s/standard/%s" % (self.url_prefix, id), axapi_args=kwargs)

    def create(self, std, stdrules, **kwargs):
        request_params = {
            "standard-list": [{
                "std": std,
                "stdrules": stdrules
            }]
        }
        return self._post("%s/standard" % self.url_prefix, request_params, axapi_args=kwargs)
