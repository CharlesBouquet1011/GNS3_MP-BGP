from mathis import links_in_AS, links_out_AS

def genere_config_noeud(intent_file):
    config_noeuds={}
    in_links = []
    for ass in intent_file.keys():
        for routeur in intent_file[ass]["routeurs"]:
            config_noeuds[routeur]={}
            config_noeuds[routeur]["ip_et_co"]={}
            config_noeuds[routeur]["protocole"]="OSPF"
            for interface,connexion in intent_file[ass]["routeurs"][routeur].items():
                connexion=connexion[0] #on n'a pas besoin d'utiliser le coût
                config_noeuds[routeur]["ip_et_co"][connexion]=[]
        in_links += links_in_AS.links_in_AS(intent_file[ass])
    out_links = links_out_AS.links_out_AS(intent_file)
    create_subnets_and_map_in(intent_file, in_links, config_noeuds)
    create_subnets_and_map_out(out_links, config_noeuds)
    return config_noeuds

def create_subnets_and_map_in(intent_file, links, config_noeuds):
    try:
        for as_nb in intent_file.keys():
            network_address = intent_file[as_nb]["plage_IP"]
            nb_of_links = len(links)
            octets = (network_address.split('/')[0]).split('.')
            octets[2] = 0
            octets[3] = 0
            plage = f"{octets[0]}.{octets[1]}"
            for link in links:
                config_noeuds[link[0]]["ip_et_co"][link[2]]=[link[1], f"{plage}.{octets[2]}.{octets[3]+1}"]
                config_noeuds[link[2]]["ip_et_co"][link[0]]=[link[3], f"{plage}.{octets[2]}.{octets[3]+2}"]
                if octets[3] < 249:
                    octets[3] += 4
                else:
                    octets[2] += 1
                    octets[3] = 0
        return config_noeuds
    except (IndexError, ValueError):
        return "Invalid format"

def create_subnets_and_map_out(out_links, config_noeuds):
    try:
        for link in out_links:
            config_noeuds[link[1]]["ip_et_co"][link[4]]=[link[2], f"{link[0]}.{link[3]}.0.1"]
            config_noeuds[link[4]]["ip_et_co"][link[1]]=[link[5], f"{link[0]}.{link[3]}.0.2"]
    except (IndexError, ValueError):
        return "Invalid format"

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
