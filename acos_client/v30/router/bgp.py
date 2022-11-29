from ..base import BaseV30
from .utils import create_route_map_structure

from pprint import pprint


class BgpBase(BaseV30):

    def __init__(self, client):
        super(BgpBase, self).__init__(client=client)
        self.url_prefix = "/router/bgp/"
        self.url_suffix = ""

    def get_list(self, asn):
        _url = self._build_url(middle=asn, suffix=self.url_suffix, ends_with_separator=True)
        print(f"GET List URL: {_url}")
        return self._get(_url)

    def get(self, asn, key=None):
        key = key if key is not None else ""
        _url = self._build_url(middle=asn, suffix=self.url_suffix, ends_with_separator=True)
        _url = f"{_url}{key}"
        print(f"GET URL: {_url}")
        return self._get(_url)

    def delete(self, asn, key):
        _url = self._build_url(middle=asn, suffix=self.url_suffix, ends_with_separator=True)
        _url = f"{_url}{key}"
        print(f"DELETE URL: {_url}")
        return self._delete(_url)


class NeighborIPv4(BgpBase):

    def __init__(self, client):
        super(NeighborIPv4, self).__init__(client=client)
        self.url_suffix = "neighbor/ipv4-neighbor/"

    def create(
        self,
        ip, asn,
        bfd=None, description=None,
        activate=None, multihop=None,
        rm_in=None, rm_out=None,
        peer_group_name=None, remote_as=None,
        send_community=None, shutdown=None
    ):
        """
        Create IPv4 BGP neighbor
        :param ip: Neighbor IP Address
        :param asn: Local BGP ASN
        :param bfd: Enable BFP
        :param description: Description for the neighbor
        :param activate: Activate/DeActivate neighbor
        :param multihop: Enable BGP multi-hp
        :param rm_in: Specify inbound RouteMap
        :param rm_out: Specify outbound RouteMap
        :param peer_group_name: Assign the neighbor to a peer
            group
        :param send_community: Secify where to send commnunity
            Allowed values: "both", "none", "standard", "extended"
        :param remote_as: Specify neighbor remote AS number
        :param shutdown: Shutdown BGP neighbour
        :return Dict:
        """
        payload = self._build_payload(
            ip=ip, bfd=bfd, description=description,
            activate=activate, multihop=multihop,
            rm_in=rm_in, rm_out=rm_out,
            peer_group_name=peer_group_name,
            send_community=send_community,
            remote_as=remote_as,
            shutdown=shutdown
        )
        _url = self._build_url(middle=asn, suffix=self.url_suffix, ends_with_separator=True)
        print(f"URL NeighborIPv4 Create: {_url}")
        return self._post(_url, payload)

    def update(
        self,
        ip, asn,
        bfd=None, description=None,
        activate=None, multihop=None,
        rm_in=None, rm_out=None,
        peer_group_name=None, remote_as=None,
        send_community=None, shutdown=None
    ):
        """
        Update IPv4 neighbor
        :param ip: Neighbor IP Address
        :param asn: Local BGP ASN
        :param bfd: Enable BFP
        :param description: Description for the neighbor
        :param activate: Activate/DeActivate neighbor
        :param multihop: Enable BGP multi-hp
        :param rm_in: Specify inbound RouteMap
        :param rm_out: Specify outbound RouteMap
        :param remote_as: Specify neighbor remote AS number
        :param peer_group_name: Assign the neighbor to a peer
            group
        :param send_community: Secify where to send commnunity
            Allowed values: "both", "none", "standard", "extended"
        :param shutdown: Shutdown BGP neighbour
        :return Dict:
        """
        payload = self._build_payload(
            ip=ip, bfd=bfd, description=description,
            activate=activate, multihop=multihop,
            rm_in=rm_in, rm_out=rm_out,
            peer_group_name=peer_group_name,
            remote_as=remote_as,
            send_community=send_community,
            shutdown=shutdown
        )
        _url = self._build_url(middle=asn, suffix=self.url_suffix, ends_with_separator=True)
        pprint(f"Url NeighborIPv4 Update: {_url}")
        return self._post(f"{_url}{ip}", payload)

    @staticmethod
    def _build_payload(
        ip,
        bfd=None, description=None,
        activate=None, multihop=None,
        rm_in=None, rm_out=None,
        peer_group_name=None, remote_as=None,
        send_community=None, shutdown=None
    ):
        rv = dict()
        rv['neighbor-ipv4'] = ip
        if bfd is not None:
            rv['bfd'] = 1 if bfd is True else 0
        if description is not None:
            rv['description'] = description
        if activate is not None:
            rv['activate'] = 1 if activate is True else 0
        if peer_group_name is not None:
            rv['peer-group-name'] = peer_group_name
        if shutdown is not None:
            rv['shutdown'] = 1 if shutdown is True else 0
        if multihop is not None:
            rv['ebgp-multihop'] = 1 if multihop is True else 0
        if remote_as is not None:
            rv['nbr-remote-as'] = remote_as
        if send_community is not None:
            if send_community not in ["both", "none", "standard", "extended"]:
                raise ValueError(
                    f"send_community val {send_community} not in accepted values: both, none, standard, extended"
                )
            rv['send-community-val'] = send_community
        if rm_in is not None or rm_out is not None:
            rv['neighbor-route-map-lists'] = create_route_map_structure(rm_in=rm_in, rm_out=rm_out)
        return {
            "ipv4-neighbor": rv
        }


class NeighborIPv6(BgpBase):

    def __init__(self, client):
        super(NeighborIPv6, self).__init__(client=client)
        self.url_suffix = "neighbor/ipv6-neighbor/"

    def create(
        self,
        ip, asn,
        bfd=None, description=None,
        activate=None, multihop=None,
        rm_in=None, rm_out=None,
        peer_group_name=None, remote_as=None,
        send_community=None, shutdown=None
    ):
        """
        Create IPv4 BGP neighbor
        :param ip: Neighbor IP Address
        :param asn: Local BGP ASN
        :param bfd: Enable BFP
        :param description: Description for the neighbor
        :param activate: Activate/DeActivate neighbor
        :param multihop: Enable BGP multi-hp
        :param rm_in: Specify inbound RouteMap
        :param rm_out: Specify outbound RouteMap
        :param peer_group_name: Assign the neighbor to a peer
            group
        :param send_community: Secify where to send commnunity
            Allowed values: "both", "none", "standard", "extended"
        :param remote_as: Specify neighbor remote AS number
        :param shutdown: Shutdown BGP neighbour
        :return Dict:
        """
        payload = self._build_payload(
            ip=ip, bfd=bfd, description=description,
            activate=activate, multihop=multihop,
            rm_in=rm_in, rm_out=rm_out,
            peer_group_name=peer_group_name,
            send_community=send_community,
            remote_as=remote_as,
            shutdown=shutdown
        )
        _url = self._build_url(middle=asn, suffix=self.url_suffix, ends_with_separator=True)
        print(f"URL NeighborIPv4 Create: {_url}")
        return self._post(_url, payload)

    def update(
        self,
        ip, asn,
        bfd=None, description=None,
        activate=None, multihop=None,
        rm_in=None, rm_out=None,
        peer_group_name=None, remote_as=None,
        send_community=None, shutdown=None
    ):
        """
        Update IPv4 neighbor
        :param ip: Neighbor IP Address
        :param asn: Local BGP ASN
        :param bfd: Enable BFP
        :param description: Description for the neighbor
        :param activate: Activate/DeActivate neighbor
        :param multihop: Enable BGP multi-hp
        :param rm_in: Specify inbound RouteMap
        :param rm_out: Specify outbound RouteMap
        :param remote_as: Specify neighbor remote AS number
        :param peer_group_name: Assign the neighbor to a peer
            group
        :param send_community: Secify where to send commnunity
            Allowed values: "both", "none", "standard", "extended"
        :param shutdown: Shutdown BGP neighbour
        :return Dict:
        """
        payload = self._build_payload(
            ip=ip, bfd=bfd, description=description,
            activate=activate, multihop=multihop,
            rm_in=rm_in, rm_out=rm_out,
            peer_group_name=peer_group_name,
            remote_as=remote_as,
            send_community=send_community,
            shutdown=shutdown
        )
        _url = self._build_url(middle=asn, suffix=self.url_suffix, ends_with_separator=True)
        pprint(f"Url NeighborIPv4 Update: {_url}")
        return self._post(f"{_url}{ip}", payload)

    @staticmethod
    def _build_payload(
        ip,
        bfd=None, description=None,
        activate=None, multihop=None,
        rm_in=None, rm_out=None,
        peer_group_name=None, remote_as=None,
        send_community=None, shutdown=None
    ):
        rv = dict()
        rv['neighbor-ipv6'] = ip
        if bfd is not None:
            rv['bfd'] = 1 if bfd is True else 0
        if description is not None:
            rv['description'] = description
        if activate is not None:
            rv['activate'] = 1 if activate is True else 0
        if peer_group_name is not None:
            rv['peer-group-name'] = peer_group_name
        if shutdown is not None:
            rv['shutdown'] = 1 if shutdown is True else 0
        if multihop is not None:
            rv['ebgp-multihop'] = 1 if multihop is True else 0
        if remote_as is not None:
            rv['nbr-remote-as'] = remote_as
        if send_community is not None:
            if send_community not in ["both", "none", "standard", "extended"]:
                raise ValueError(
                    f"send_community val {send_community} not in accepted values: both, none, standard, extended"
                )
            rv['send-community-val'] = send_community
        if rm_in is not None or rm_out is not None:
            rv['neighbor-route-map-lists'] = create_route_map_structure(rm_in=rm_in, rm_out=rm_out)
        return {
            "ipv6-neighbor": rv
        }


class PeerGroupIPv4Neighbor(BgpBase):

    def __init__(self, client):
        super(PeerGroupIPv4Neighbor, self).__init__(client=client)
        self.url_suffix = f"neighbor/peer-group-neighbor/"

    def create(
        self,
        asn,
        name=None, remote_as=None,
        bfd=None, route_refresh=None,
        activate=None, multihop=None,
        shutdown=None, next_hop_self=None,
        rm_in=None, rm_out=None,
        send_community=None,
        inbound=None
    ):
        """
        Create IPv4 neighbor peer-group

        :param name: Peer-group name
        :param asn: Local BGP ASN
        :param bfd: Enable BFP
        :param remote_as: Specify remote AS number
        :param activate: Activate/DeActivate neighbor
        :param route_refresh: Enable route-refresh
        :param shutdown: Shutdown peer-group
        :param multihop: Enable BGP multi-hp
        :param rm_in: Specify inbound RouteMap
        :param rm_out: Specify outbound RouteMap
        :param next_hop_self: Enable next-hop-self
        :param send_community: Specify where to send community
            Allowed values: "both", "none", "standard", "extended"
        :param inbound: Allow inbound soft reconfiguration for this neighbor
        :return Dict:
        """
        payload = self._build_payload(
            name=name, remote_as=remote_as, bfd=bfd,
            route_refresh=route_refresh, activate=activate, multihop=multihop,
            shutdown=shutdown, next_hop_self=next_hop_self,
            rm_in=rm_in, rm_out=rm_out, send_community=send_community,
            inbound=inbound
        )
        _url = self._build_url(middle=asn, suffix=self.url_suffix, ends_with_separator=True)
        return self._post(_url, payload)

    def update(
        self,
        asn,
        name=None, remote_as=None,
        bfd=None, route_refresh=None,
        activate=None, multihop=None,
        shutdown=None, next_hop_self=None,
        rm_in=None, rm_out=None,
        send_community=None,
        inbound=None
    ):
        """
        Update IPv4 neighbor peer-group

        :param name: Peer-group name
        :param asn: Local BGP ASN
        :param bfd: Enable BFP
        :param remote_as: Specify remote AS number
        :param activate: Activate/DeActivate neighbor
        :param route_refresh: Enable route-refresh
        :param shutdown: Shutdown peer-group
        :param multihop: Enable BGP multi-hp
        :param rm_in: Specify inbound RouteMap
        :param rm_out: Specify outbound RouteMap
        :param next_hop_self: Enable next-hop-self
        :param send_community: Specify where to send community
            Allowed values: "both", "none", "standard", "extended"
        :param inbound: Allow inbound soft reconfiguration for this neighbor
        :return Dict:
        """
        payload = self._build_payload(
            name=name, remote_as=remote_as, bfd=bfd,
            route_refresh=route_refresh, activate=activate, multihop=multihop,
            shutdown=shutdown, next_hop_self=next_hop_self,
            rm_in=rm_in, rm_out=rm_out, send_community=send_community,
            inbound=inbound
        )
        _url = self._build_url(middle=asn, suffix=self.url_suffix, ends_with_separator=True)
        return self._post(f"{_url}{name}", payload)

    @staticmethod
    def _build_payload(
        name=None, remote_as=None,
        bfd=None, route_refresh=None,
        activate=None, multihop=None,
        shutdown=None, next_hop_self=None,
        rm_in=None, rm_out=None,
        send_community=None,
        inbound=None
    ):
        rv = {
            'peer-group-key': 1,
            'activate': 1,
            'allowas-in': 0,
            'dynamic': 0,
            'route-refresh': 1,
            'extended-nexthop': 0,
            'collide-established': 0,
            'default-originate': 0,
            'disallow-infinite-holdtime': 0,
            'dont-capability-negotiate': 0,
            'ebgp-multihop': 0,
            'enforce-multihop': 0,
            'bfd': 0,
            'maximum-prefix': 128,
            'next-hop-self': 0,
            'override-capability': 0,
            'passive': 0,
            'remove-private-as': 0,
            'send-community-val': 'both',
            'inbound': 0,
            'shutdown': 0,
            'strict-capability-match': 0,
            'timers-keepalive': 30,
            'timers-holdtime': 90,
            'weight': 0,
        }
        if name is not None:
            rv['peer-group'] = name
        if remote_as is not None:
            rv['peer-group-remote-as'] = remote_as
        if bfd is not None:
            rv['bfd'] = 1 if bfd is True else 0
        if send_community is not None:
            if send_community not in ["both", "none", "standard", "extended"]:
                raise ValueError(
                    f"send_community val {send_community} not in accepted values: both, none, standard, extended"
                )
            rv['send-community-val'] = send_community
        if activate is not None:
            rv['activate'] = 1 if activate is True else 0
        if shutdown is not None:
            rv['shutdown'] = 1 if shutdown is True else 0
        if multihop is not None:
            rv['ebgp-multihop'] = 1 if multihop is True else 0
        if route_refresh is not None:
            rv['route-refresh'] = 1 if route_refresh is True else 0
        if next_hop_self is not None:
            rv['next-hop-self'] = 1 if next_hop_self is True else 0
        if inbound is not None:
            rv['inbound'] = 1 if next_hop_self is True else 0
        if rm_in is not None or rm_out is not None:
            rv['neighbor-route-map-lists'] = create_route_map_structure(rm_in=rm_in, rm_out=rm_out)
        # return rv
        return {
            "peer-group-neighbor": rv
        }


class NeighborIpv6(BgpBase):

    def __init__(self, client):
        super(NeighborIpv6, self).__init__(client=client)
        self.url_suffix = f"address-family/ipv6/neighbor/ipv6-neighbor/"

    def create(
        self,
        ipv6, asn,
        send_community=None,
        next_hop_self=None,
        activate=None,
        rm_in=None, rm_out=None,
        peer_group_name=None,
    ):
        """
        Create IPv6 neighbor

        :param ipv6: Neighbor IP Address
        :param asn: Local BGP ASN
        :param activate: Activate/DeActivate neighbor
        :param rm_in: Specify inbound RouteMap
        :param rm_out: Specify outbound RouteMap
        :param next_hop_self: Enable next-hop-self
        :param peer_group_name: Assign the neighbor to a peer
            group
        :param send_community: Specify where to send community
            Allowed values: "both", "none", "standard", "extended"
        :return Dict:
        """
        payload = self._build_payload(
            ipv6=ipv6, send_community=send_community,
            next_hop_self=next_hop_self, activate=activate,
            rm_out=rm_out, rm_in=rm_in, peer_group_name=peer_group_name
        )
        _url = self._build_url(middle=asn, suffix=self.url_suffix, ends_with_separator=True)
        print(f"URL NeighborIpv6 Create: {_url}")
        return self._post(_url, payload)

    def update(
        self,
        ipv6, asn,
        send_community=None,
        next_hop_self=None,
        activate=None,
        rm_in=None, rm_out=None,
        peer_group_name=None,
    ):
        """
        Update IPv6 neighbor

        :param ipv6: Neighbor IP Address
        :param asn: Local BGP ASN
        :param activate: Activate/DeActivate neighbor
        :param rm_in: Specify inbound RouteMap
        :param rm_out: Specify outbound RouteMap
        :param next_hop_self: Enable next-hop-self
        :param peer_group_name: Assign the neighbor to a peer
            group
        :param send_community: Specify where to send community
            Allowed values: "both", "none", "standard", "extended"
        :return Dict:
        """
        payload = self._build_payload(
            ipv6=ipv6, send_community=send_community,
            next_hop_self=next_hop_self, activate=activate,
            rm_out=rm_out, rm_in=rm_in, peer_group_name=peer_group_name
        )
        _url = self._build_url(middle=asn, suffix=self.url_suffix, ends_with_separator=True)
        print(f"URL NeighborIpv6 Update: {_url}{ipv6}")
        return self._post(f"{_url}{ipv6}", payload)

    @staticmethod
    def _build_payload(
        ipv6,
        send_community=None,
        next_hop_self=None,
        activate=None,
        rm_in=None, rm_out=None,
        peer_group_name=None,
    ):
        rv = dict()
        rv['neighbor-ipv6'] = ipv6
        if send_community is not None:
            if send_community not in ["both", "none", "standard", "extended"]:
                raise ValueError(
                    f"send_community val {send_community} not in accepted values: both, none, standard, extended"
                )
            rv['send-community-val'] = send_community
        if next_hop_self is not None:
            rv['next-hop-self'] = 1 if next_hop_self is True else 0
        if activate is not None:
            rv['activate'] = 1 if activate is True else 0
        if rm_in is not None or rm_out is not None:
            rv['neighbor-route-map-lists'] = create_route_map_structure(rm_in=rm_in, rm_out=rm_out)
        if peer_group_name is not None:
            rv['peer-group-name'] = peer_group_name
        return {
            "ipv6-neighbor": rv
        }


class PeerGroupIpv6(BgpBase):

    def __init__(self, client):
        super(PeerGroupIpv6, self).__init__(client)
        self.url_suffix = f"address-family/ipv6/neighbor/peer-group-neighbor/"

    def create(
        self,
        name, asn, activate=None,
        send_community=None,
        next_hop_self=None,
        max_prefix=None,
        inbound=None
    ):
        """
        For IPv6, in order to use a peergroup that you created before,
        you need to activate first that peer-group into IPv6 AF container

        :param name: Peer-group name
        :param asn: Local BGP AS Number
        :param activate: Activate/DeActivate neighbor
        :param max_prefix: Maximum number of prefix accept from this pee
        :param next_hop_self: Enable next-hop-self
        :param send_community: Specify where to send community
            Allowed values: "both", "none", "standard", "extended"
        :param inbound: Allow inbound soft reconfiguration for this neighbor
        :return Dict:
        """
        payload = self._build_payload(
            name=name, activate=activate,
            send_community=send_community, next_hop_self=next_hop_self,
            max_prefix=max_prefix, inbound=inbound
        )
        _url = self._build_url(middle=asn, suffix=self.url_suffix, ends_with_separator=True)
        return self._post(_url, payload)

    def update(
        self,
        name, asn, activate=None,
        send_community=None,
        next_hop_self=None,
        max_prefix=None,
        inbound=None
    ):
        """
        Update IPv6 peer-group values

        :param name: Peer-group name
        :param asn: Local BGP AS Number
        :param activate: Activate/DeActivate neighbor
        :param max_prefix: Maximum number of prefix accept from this pee
        :param next_hop_self: Enable next-hop-self
        :param send_community: Specify where to send community
            Allowed values: "both", "none", "standard", "extended"
        :param inbound: Allow inbound soft reconfiguration for this neighbor
        :return Dict:
        """
        payload = self._build_payload(
            name=name, activate=activate,
            send_community=send_community, next_hop_self=next_hop_self,
            max_prefix=max_prefix, inbound=inbound
        )
        _url = self._build_url(middle=asn, suffix=self.url_suffix, ends_with_separator=True)
        return self._post(f"{_url}{name}", payload)

    @staticmethod
    def _build_payload(
        name, activate=None,
        send_community=None,
        next_hop_self=None,
        max_prefix=None,
        inbound=None
    ):
        rv = {'allowas-in': 0, 'default-originate': 0, 'inbound': 0, 'maximum-prefix': 128, 'next-hop-self': 0,
              'peer-group': name, 'remove-private-as': 0, 'send-community-val': 'both'}
        if activate is not None:
            rv['activate'] = 1 if activate is True else 0
        if send_community is not None:
            if send_community not in ["both", "none", "standard", "extended"]:
                raise ValueError(
                    f"send_community val {send_community} not in accepted values: both, none, standard, extended"
                )
            rv['send-community-val'] = send_community
        if next_hop_self is not None:
            rv['next-hop-self'] = 1 if next_hop_self is True else 0
        if max_prefix is not None:
            rv['maximum-prefix'] = max_prefix
        if inbound is not None:
            rv['inbound'] = 1 if next_hop_self is True else 0
        return {
            "peer-group-neighbor": rv
        }


class Neighbor(BgpBase):

    def __init__(self, client):
        super(Neighbor, self).__init__(client=client)
        self.url_suffix = "neighbor/"

    @property
    def ipv4_neighbor(self):
        return NeighborIPv4(self.client)

    @property
    def ipv6_neighbor(self):
        return NeighborIPv6(self.client)

    @property
    def peer_group(self):
        return PeerGroupIPv4Neighbor(self.client)


class AddressFamilyIPv6(BgpBase):
    def __init__(self, client):
        super(AddressFamilyIPv6, self).__init__(client=client)
        self.url_suffix = "address-family/"

    @property
    def ipv6_neighbor(self):
        return NeighborIpv6(self.client)

    @property
    def peer_group(self):
        return PeerGroupIpv6(self.client)


class Bgp(BgpBase):

    def __init__(self, client):
        super(Bgp, self).__init__(client=client)

    @property
    def neighbor(self):
        return Neighbor(self.client)

    @property
    def address_family(self):
        return AddressFamilyIPv6(self.client)
