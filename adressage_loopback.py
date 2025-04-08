import json

def add_loop(id_routeur:int,AS:str):
    return f"{AS}.0.128.{id_routeur}"
# def adressage_loopback(data:dict,AS:str):
#     dic_loop = {}
#     liste_routeur = list(data[AS]["routeurs"].keys())
    
#     for r in liste_routeur:
        
#         id_routeur = r[1:]
#         add_loop = f"{AS}.0.128.{id_routeur}" 
#         dic_loop[r] = add_loop
#     return dic_loop

def map_routeurs_to_as(data):
    routeur_to_as = {}
    for AS in data:
        for routeur in data[AS]["routeurs"]:
            routeur_to_as[routeur] = AS
    return routeur_to_as


def generer_loopback_commandes(routeur:str, adresse_loopback:str):
	"""
	génère les commandes loopback à appliquer au routeur donné en entrée à l'aide du dictionnaire de config
	"""
	commandes = []
	
	commandes.extend([
                     "conf t",
					f"interface loopback0",
					
					f" ip address {adresse_loopback} 255.255.255.255",
					f"no shutdown",
					"exit","end"])
	

	return commandes


def configure_loopback_addresses(data,config_noeud):
    routeur_to_as = map_routeurs_to_as(data)
    
    for routeur in config_noeud:
        if routeur in routeur_to_as:
            AS = routeur_to_as[routeur]
            adresse_loopback = add_loop(routeur[1:], AS)
            config_noeud[routeur]["loopback"] = adresse_loopback
        


    
if __name__ == "__main__":
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
    with open('fichier_intention.json','r') as file:
        data  = json.load(file)
    print(config_noeuds)
    
    configure_loopback_addresses(data,config_noeuds)
    print(config_noeuds)
    
        