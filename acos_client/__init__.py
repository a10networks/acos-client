# Copyright 2014,  Doug Wiegley,  A10 Networks.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
# flake8: noqa

from acos_client.version import VERSION
from acos_client.client import Client
from acos_client.hash import Hash

AXAPI_21 = '21'
AXAPI_30 = '30'
#AXAPI_SSH = 'ssh'
AXAPI_VERSIONS = (AXAPI_21, AXAPI_30)
