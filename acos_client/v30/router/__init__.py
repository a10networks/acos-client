from ..base import BaseV30
from acos_client.v30.router.bgp import Bgp


class Router(BaseV30):
    def __str__(self):
        return f"Router: {vars(self)}"

    @property
    def bgp(self) -> Bgp:
        return Bgp(client=self.client)

    @property
    def isis(self):
        pass

    @property
    def log(self):
        pass

    @property
    def ospf(self):
        pass

    @property
    def rip(self):
        pass

    @property
    def ipv6(self):
        pass

    def all(self):
        return self._get("/router/")
