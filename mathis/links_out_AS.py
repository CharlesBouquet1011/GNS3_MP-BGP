import json

with open('./mathis/intent_lite.json', 'r') as JSON:
    intent = json.load(JSON)

def links_out_AS(intent):
    links = []
    AS_by_router = {}
    processed = set()  # Pour éviter de traiter deux fois le même lien

    # Table de correspondance routeur <-> AS
    for AS_number, AS_data in intent.items():
        for router in AS_data["routeurs"]:
            AS_by_router[router] = AS_number

    # Parcours de chaque routeur et de ses interfaces
    for AS_number, AS_data in intent.items():
        routers = AS_data["routeurs"]

        for router, interfaces in routers.items():
            for interface, info in interfaces.items():
                neighbor_router = info[0]

                # Vérifie si le voisin est dans une autre AS
                if neighbor_router in AS_by_router and AS_by_router[neighbor_router] != AS_number:
                    neighbor_AS = AS_by_router[neighbor_router]

                    # Trouve l'interface du voisin pointant vers ce routeur
                    neighbor_interfaces = intent[neighbor_AS]["routeurs"][neighbor_router]
                    for neighbor_intf_temp, neighbor_info in neighbor_interfaces.items():
                        if neighbor_info[0] == router:
                            # Clé unique du lien pour éviter les doublons (triée par AS + routeur)
                            key = tuple(sorted([(AS_number, router), (neighbor_AS, neighbor_router)]))
                            if key not in processed:
                                links.append([AS_number, router, interface, neighbor_AS, neighbor_router, neighbor_intf_temp])
                                processed.add(key)
                            break
    return links

# Traitement de toutes les AS
print(links_out_AS(intent))

# Résultat de la fonction links_out_AS(intent) avec intent_lite.json
# [['1', R1', 'FastEthernet0/0', '2', 'R4', 'GigabitEthernet1/0'], ['1', 'R3', 'GigabitEthernet3/0', '2', 'R5', 'FastEthernet0/0']]