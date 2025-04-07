import json

with open('intent_lite.json', 'r') as JSON:
    intent = json.load(JSON)

def links_in_AS(AS):
    routers = AS["routeurs"]
    links = []
    processed = set()  # Pour éviter de traiter deux fois le même lien

    for router_src, interfaces in routers.items(): # Parcours de chaque routeur source et de ses interfaces
        for intf_src, info_src in interfaces.items():
            router_dest, metric_src = info_src[0], info_src[1]
            if router_dest in routers: # Liens internes (destination dans la même AS)
                key = tuple(sorted([router_src, router_dest])) # Clé unique pour la paire (sans tenir compte de l'ordre)
                if key not in processed:
                    # Recherche de l'interface sur le routeur destination qui pointe vers src
                    intf_dest, metric_dest = None, None
                    for intf_dest_temp, info_dest in routers[router_dest].items():
                        if info_dest[0] == router_src:
                            intf_dest, metric_dest = intf_dest_temp, info_dest[1]
                            break
                    if intf_dest is not None:
                        if metric_src != metric_dest:
                            print(f"Info : Les métriques sont différentes pour le lien {router_src} <-> {router_dest} : {metric_src} vs {metric_dest}")
                        if router_src < router_dest: # Routeur avec le nom "le plus petit" en premier
                            links.append([router_src, intf_src, router_dest, intf_dest, metric_src])
                        else:
                            links.append([router_dest, intf_dest, router_src, intf_src, metric_src])
                        processed.add(key)
    return links

# Traitement de chaque AS (ici, l'exemple n'en contient qu'un)
for AS_number, AS_data in intent.items():
    print("AS", AS_number, links_in_AS(AS_data))


# Résultat fonction
# [["R1", "GigabitEthernet1/0", "R2", "GigabitEthernet2/0",0],["R1", "GigabitEthernet2/0", "R3", "GigabitEthernet1/0",0],["R2", "GigabitEthernet1/0", "R3", "GigabitEthernet2/0",0]]