from typing import List, Optional


def create_route_map_structure(rm_in: Optional[str] = None, rm_out: Optional[str] = None) -> List:
    """
    Helper function for creating the Route-Map structure that can be applied
    in multiple locations, like IPv4 Neighbour, Ipv6 Neighbour, etc
    :param rm_in: Name of the inbound Route-Map
    :param rm_out: Name of the outbound Route-Map
    :returns: List
    """
    rm_list = list()
    if rm_out is not None:
        rm_list.append({"nbr-rmap-direction": "out", "nbr-route-map": rm_out})
    if rm_in is not None:
        rm_list.append({"nbr-rmap-direction": "in", "nbr-route-map": rm_in})
    return rm_list
