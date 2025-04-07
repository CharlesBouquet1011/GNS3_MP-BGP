from mathis import links_in_AS, links_out_AS

import json

def genere_config_noeud(intent_file):
    config_noeuds={}
    for ass in intent_file.keys():
        for routeur in intent_file[ass]["routeurs"]:
            config_noeuds[routeur]={}
            config_noeuds[routeur]["ip_et_co"]={}
            config_noeuds[routeur]["protocole"]="OSPF"
            for interface,connexion in intent_file[ass]["routeurs"][routeur].items():
                connexion=connexion[0] #on n'a pas besoin d'utiliser le coût
                config_noeuds[routeur]["ip_et_co"][connexion]=[]
    return config_noeuds

def create_subnets(intent_file, as_nb):
    try:
        network_address = intent_file[as_nb]["plage_IP"]
        nb_of_links = 0
        for router in intent_file[as_nb]["routeurs"].values():
            nb_of_links += len(router)
        octets = (network_address.split('/')[0]).split('.')
        octets[2] = 0
        octets[3] = 0
        plage = f"{octets[0]}.{octets[1]}"
        subnet_addresses = []
        for i in range (nb_of_links):
            subnet_addresses.append((f"{plage}.{octets[2]}.{octets[3]+1}", f"{plage}.{octets[2]}.{octets[3]+2}"))
            if octets[3] < 249:
                octets[3] += 4
            else:
                octets[2] += 1
                octets[3] = 0
        return subnet_addresses

    
    except (IndexError, ValueError):
        return "Invalid format"

def mapping_in(links, subnet_addresses, config_noeuds):
    for i in range (len(links)):
        config_noeuds[links[i][0]]["ip_et_co"][links[i][2]]=[links[i][1], subnet_addresses[i][0]]
        config_noeuds[links[i][2]]["ip_et_co"][links[i][0]]=[links[i][3], subnet_addresses[i][1]]
    return config_noeuds

def mapping_out(links, subnet_addresses, config_noeuds):
    for i in range (len(links)):
        config_noeuds[links[i][1]]["ip_et_co"][links[i][4]]=[links[i][2], subnet_addresses[i][0]]
        config_noeuds[links[i][4]]["ip_et_co"][links[i][1]]=[links[i][5], subnet_addresses[i][1]]
    return config_noeuds

def genere_commandes_ip(config_noeuds,noeud):
    """génère les commandes pour configurer les addresses ip"""
    commande=["configure terminal"]
    for interface,ip in config_noeuds[noeud]["ip_et_co"].values():
        commande.append(f"interface {interface}")
        commande.append(f"ip address {ip} 255.255.255.252")
        commande.append("no shutdown")
        commande.append("exit")

    commande.append("end")
    return commande

if __name__=="__main__":
    with open('fichier_intention.json', 'r') as file:
        intent_data = json.load(file)

    in_links = links_in_AS.links_in_AS(intent_data["1"]) #Pour l'AS 1
    out_links = links_out_AS.links_out_AS(intent_data)
    config_noeuds = genere_config_noeud(intent_data)
    subnet = create_subnets(intent_data, "1")
    min = mapping_in(in_links, subnet, config_noeuds)
    mout = mapping_out(out_links, subnet, config_noeuds)
    commande = []

    for router in intent_data["1"]["routeurs"]:
        commande.append(genere_commandes_ip(config_noeuds, router))
    print(commande)