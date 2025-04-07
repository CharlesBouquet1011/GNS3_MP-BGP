import json

with open('./mathis/intent_lite.json', 'r') as JSON:
    intent = json.load(JSON)

def links_out_AS(intent):
    links = []

    for AS_number, AS_data in intent.items():
        routers = AS_data["routeurs"]

    return links

# Traitement de toutes les AS
print(links_out_AS(intent))


# Résultat fonction
# [['1', R1', 'FastEthernet0/0', '2', 'R4', 'GigabitEthernet1/0'], ['1', 'R3', 'GigabitEthernet3/0', '2', 'R5', 'FastEthernet0/0']]