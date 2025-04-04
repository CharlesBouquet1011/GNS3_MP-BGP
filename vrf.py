from BGP import get_as_for_router


def config_vrf(router_id,voisin_id,data,nom_client):
    as_self=get_as_for_router(router_id,data)
    as_neighbour=get_as_for_router(voisin_id,data)
    commands = ["conf t"]
    '''
    vrf definition Client_1
    rd 1:1
    route-target export 1:1
    route-target import 1:1
    '''
    commands.append(f"vrf definition {nom_client}")
    commands.append(f"rd {as_self}:{as_neighbour}")
    commands.append(f"route-target export {as_self}:{nom_client[3:]}") #car nos noms de clients sont VPN1, VPN2, ...
    commands.append(f"route-target import {as_self}:{nom_client[3:]}")


