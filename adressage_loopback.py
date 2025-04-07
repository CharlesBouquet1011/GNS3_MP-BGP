import json

# config des @ entre PE & CE avec AS1.AS2.0.0/16
#10.0.0.0/17 pour les interfaces physiques
#10.0.128.0/17 pour les interfaces loopback


#config des @ loopback avec des /32
def adressage_loopback(data:dict,AS:str):
    dic_loop = {}
    liste_routeur = list(data[AS]["routeurs"].keys())
    
    for r in liste_routeur:
        
        id_routeur = r[1:]
        add_loop = f"{AS}.0.128.{id_routeur}" 
        dic_loop[r] = add_loop
    return dic_loop

def generer_loopback_commandes(routeur:str, adresse_loopback:str):
	"""
	génère les commandes loopback à appliquer au routeur donné en entrée à l'aide du dictionnaire de config
	"""
	commandes = []
	
	commandes.extend([
                     "conf t",
					f"interface loopback0",
					
					f" ip address {adresse_loopback} 255.255.128.0",
					f"no shutdown",
					"exit","end"])
	

	return commandes

def ajout_commande_config(config_noeud: dict,loopbacks:dict):
     for routeur in config_noeud.keys():
        if routeur in loopbacks:
            config_noeud[routeur]["loopback"]=generer_loopback_commandes(routeur,loopbacks[routeur])
        
     return config_noeud
     
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
if __name__ == "__main__":
    with open('fichier_intention.json','r') as file:
        data  = json.load(file)
    print(config_noeuds)
    
    for AS in data.keys():
        loopbacks =adressage_loopback(data,AS)
        config_noeuds = ajout_commande_config(config_noeuds,loopbacks)
    print(config_noeuds)
    
        