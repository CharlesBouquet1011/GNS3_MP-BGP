import json

with open('fichier_intention.json', 'r') as JSON: # Charger le fichier JSON
    intent = json.load(JSON)

def links_in_AS(AS):
    return AS["routeurs"]

for AS in intent.items():
    print("AS", AS[0], links_in_AS(AS[1]))

# Résultat fonction
[["R1", "GigabitEthernet1/0", "R2", "GigabitEthernet2/0",0],["R1", "GigabitEthernet2/0", "R3", "GigabitEthernet1/0",0],["R2", "GigabitEthernet1/0", "R3", "GigabitEthernet2/0",0]]