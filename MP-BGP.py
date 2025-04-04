"""
Configure MP-BGP Sur les routeurs PE seulement !!

"""

def routeur_est_PE(routeur,numAs,data):
    """
    data:fichier d'intention
    routeur: le routeur pour lequel on veut savoir si c'est un PE
    retourne un booleen, true si le routeur est dedans, false sinon
    """
    voisins=data[numAs]["routeurs"][routeur]
    max=0
    for liste in voisins.values():
        longueur=len(liste)
        if longueur>max:
            max=longueur
    
    return max>=3 #si on a une liste de longueur 3 dans les voisins ex [R18,0,VPN1] alors c'est un PE

def getNomClient(routeur,numAS,data,interface):
    return data[numAS]["routeurs"][routeur][interface][2]
    
