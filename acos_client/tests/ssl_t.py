# tests slb file uploading
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

"""
Basic code for testing SSL cert upload against AXAPI c3-compliant vThunder
"""

from acos_client.client import Client

key_file = "key.pem"
cert_file = "cert.pem"
file_mode = "rb"
host_ip = "10.48.7.125"
api_ver = "2.1"
username = "admin"
password = "a10"

with open(cert_file, file_mode) as f:
    f_data = f.read()
assert(f.closed)

with open(key_file, file_mode) as f:
    k_data = f.read()

x = Client(host_ip, api_ver, username, password)
x.slb.ssl.upload("cert.pem", f_data, "certificate")
