import acos_client.v21.base as base

from service_ip import Service_IP
from site import Site
from zone import Zone
from zone_service import Zone_Service


class GSLB(base.BaseV21):

    @property
    def service_ip(self):
        return Service_IP(self.client)

    @property
    def site(self):
        return Site(self.client)

    @property
    def zone(self):
        return Zone(self.client)

    @property
    def zone_service(self):
        return Zone_Service(self.client)
