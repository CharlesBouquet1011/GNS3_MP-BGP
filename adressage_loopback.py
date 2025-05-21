"""
Génère les adresses loopback
"""

def add_loop(id_routeur:int,AS:str):
    """
    Fonction générant des adresses loopbacks à partir de l'AS du routeur et de son id

    Input: id_routeur = integer
    AS = string 

    Output: f-string
    """
    return f"{AS}.0.128.{id_routeur}"

def map_routeurs_to_as(data:dict):
    """
    Fonction associant à partir de la topologie du réseau de retrouver l'AS du routeur

    Input: data = dictionnaire

    Output: routeur_to_as = dictionnaire
    """
    routeur_to_as = {}
    for AS in data:
        for routeur in data[AS]["routeurs"]:
            routeur_to_as[routeur] = AS
    return routeur_to_as


def generer_loopback_commandes(routeur:str, adresse_loopback:str):
	"""
	Fonction génèrant les commandes des adresses de loopback à appliquer au routeur donné en entrée à l'aide du dictionnaire de configuration
	Input : routeur = string
    adresse_loopback = string

    Output : commandes = liste de f-string
    """
	commandes = []
	
	commandes.extend([
                     "conf t",
					f"interface loopback0",
					
					f" ip address {adresse_loopback} 255.255.255.255",
					f"no shutdown",
					"exit","end"])
	

	return commandes


def configure_loopback_addresses(data:dict,config_noeud:dict):
    """
    mets les adresses loopback dans le dictionnaire de configuration

    Input: data = dictionnaire
    configh_noeud = dictionnaire
    """
    routeur_to_as = map_routeurs_to_as(data)
    
    for routeur in config_noeud:
        if routeur in routeur_to_as:
            AS = routeur_to_as[routeur]
            adresse_loopback = add_loop(routeur[1:], AS)
            config_noeud[routeur]["loopback"] = adresse_loopback
        


    
# if __name__ == "__main__":
#     import json

#     config_noeuds = {
#     "R1": {
#         "ip_et_co": {
#             "R2": [],
#             "R3": []
#         },

#     },
#     "R2": {
#         "ip_et_co": {
#         "R1": [],
#         "R3": []
#         },
#     },
#     "R3": {
#         "ip_et_co": {
#         "R1": [],
#         "R2": []
#         },
#     }
# }
#     with open('fichier_intention.json','r') as file:
#         data  = json.load(file)
#     print(config_noeuds)
    
#     configure_loopback_addresses(data,config_noeuds)
#     print(config_noeuds)
    
        