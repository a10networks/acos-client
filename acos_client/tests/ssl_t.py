# tests slb file uploading

from acos_client.client import Client

cert_file = "server_cert.pem"
file_mode = "rb"
host_ip = "10.48.7.125"
api_ver = "2.1"
username = "admin"
password = "a10"

with open(cert_file, file_mode) as f:
    f_data = f.read()
assert(f.closed)


x = Client(host_ip, api_ver, username, password)
x.slb.ssl.upload("server_key.pem", f_data, "certificate")
