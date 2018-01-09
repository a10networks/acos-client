# -*- coding: utf-8 -*-

__author__ = 'wenjiexu'
import random
import time
import acos_client.errors as acos_errors
import base


class DeviceContext(base.BaseV30):
    def __init__(self, client):
        super(DeviceContext, self).__init__(client)
        self.url_prefix = "/device-context/"

    def switch_context(self, device_id='1'):
        params = {
            "device-context":
                {
                    "device-id": device_id
                }
        }
        self._post(self.url_prefix, params)