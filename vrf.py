"""
configure les vrf
"""

def config_vrf(router_id,voisin_id,data,nom_client): #router id est le nom du routeur
    """
    configure les paramètres généraux de vrf pour un routeur donnée:
    router_id: nom du routeur
    voisin_id: nom du routeur voisin
    data: fichier d'intention
    nom_client: nom du client
    """
    from BGP import get_as_for_router

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
    commands.append("address-family ipv4")
    commands.append("exit-address-family")
    commands.append("end")
    return(commands)

def config_vrf_interface(interface,nom_client,config,routeur):
    """
    configure la vrf pour une interface donnée:
    interface: l'interface qu'on configure
    nom_client: nom du client
    config: dictionnaire qui contient toutes les configurations
    routeur: routeur de l'interface qu'on configure
    """
    from adressage import genere_ip_interface
    commands = ["conf t"]
    commands.append(f"interface {interface}")
    commands.append(f"vrf forwarding {nom_client}")
    commands+=genere_ip_interface(config,routeur,interface) #quand on a configuré la vrf sur une interface, ça a supprimé son IP
    commands.append("end")
    return(commands)


def config_vrf_routeur(routeur,AS,data,config):
    """
    configure intégralement la vrf d'un routeur (paramètres généraux + interfaces)
    routeur: routeur à configurer
    AS: numéro d'AS
    data: fichier d'intention
    config: dictionnaire de configuration
    """
    from MP_BGP import routeur_est_PE,getInterfacesClient
    commandes=[]
    if routeur_est_PE(routeur,AS,data):
    

        for client,CE,interface in getInterfacesClient(routeur,AS,data):
            commandes+=config_vrf(routeur,CE,data,client)
            commandes+=config_vrf_interface(interface,client,config,routeur)
    return commandes


def test():
    import json
    with open("fichier_intention.json") as fichier:
        data=json.load(fichier)
    print(config_vrf("R1","R2",data,"VPN1"))
    print(config_vrf_interface("GigabitEthernet 1/0","VPN1"))

if __name__=="__main__":
	test()