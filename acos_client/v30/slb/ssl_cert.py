from __future__ import absolute_import
from __future__ import unicode_literals

from acos_client import errors as acos_errors
from acos_client.v30 import base


class SSLCert(base.BaseV30):
    url_prefix = '/slb/ssl-cert/'

    def oper(self, max_retries=None, timeout=None, *args, **kwargs):
        return self._get(self.url_prefix + "/oper", max_retries=max_retries, timeout=timeout,
                         axapi_args=kwargs)
