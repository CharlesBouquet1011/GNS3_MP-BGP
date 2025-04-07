import json
with open('fichier_intention.json', 'r') as file:
    intent_data = json.load(file)

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

def mapping(links, subnet_addresses, config_noeuds):
    for i in range (len(links)):
        config_noeuds[links[i][0]]["ip_et_co"][links[i][2]]=[links[i][1], subnet_addresses[i][0]]
        config_noeuds[links[i][2]]["ip_et_co"][links[i][0]]=[links[i][3], subnet_addresses[i][1]]
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

ip = "10.0.0.0/16"
links = [["R1", "GigabitEthernet1/0", "R2", "GigabitEthernet2/0",0],["R1", "GigabitEthernet2/0", "R3", "GigabitEthernet1/0",0],["R2", "GigabitEthernet1/0", "R3", "GigabitEthernet2/0",0]]
config_noeuds = {
    "R1": {
        "ip_et_co": {
            "R2": [],
            "R3": []
        },
    },
    "R2": {
        "ip_et_co": {
        "R1": [],
        "R3": []
        },
    },
    "R3": {
        "ip_et_co": {
        "R1": [],
        "R2": []
        },
    }
}
subnet = create_subnets(intent_data, 1)
print(genere_commandes_ip(mapping(links, subnet, config_noeuds), "R1"))