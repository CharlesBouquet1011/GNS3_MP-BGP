import json
# config des @ entre PE & CE avec AS1.AS2.0.0/16
#10.0.0.0/17 pour les interfaces physiques
#10.0.128.0/17 pour les interfaces loopback


#config des @ loopback avec des /32
def adressage_loopback(data:dict,AS:str):
    liste_loop = []
    liste_routeur = list(data[AS]["routeurs"].keys())
    
    for index_routeur in range(len(liste_routeur)):
        
        id_routeur = liste_routeur[index_routeur][1:]
        add_loop = f"10.0.128.{id_routeur}" #ou f"10.0.128.{indice}"
        liste_loop.append((id_routeur,add_loop))
    return liste_loop

# if __name__ == "__main__":
#     with open('fichier_intention.json','r') as file:
#         data  = json.load(file)
#     for AS in data.keys():
#         print(adressage_loopback(data,AS))
        