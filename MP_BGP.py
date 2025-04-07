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
        if max>=3: break #pour aller plus vite
    
    return max>=3 #si on a une liste de longueur 3 dans les voisins ex [R18,0,VPN1] alors c'est un PE

def getNomClient(routeur,numAS,data,interface):
    return data[numAS]["routeurs"][routeur][interface][2]


def getInterfacesClient(routeur,numAs,data):
    """
    Renvoie une liste d'interfaces associées au nom du client
    """
    voisins=data[numAs]["routeurs"][routeur]
    retour=[]
    for interface,liste in voisins.items():
        if len(liste)==3:
            CE=liste[0]
            retour.append([getNomClient(routeur,numAs,data,interface),CE,interface])
            


def getIpVoisin(routeur,voisin,config):
    """
    Renvoie l'IP qu'à un voisin sur l'interface à laquelle est connectée notre routeur
    config est le dictionnaire de config
    """
    return config[voisin]["ip_et_co"][routeur][1]

def configMp_BGP_routeur(routeur,AS,data,config):
    from BGP import get_as_for_router


    
    commandes=[]
    commandes.append("conf t")
        
    commandes.append(f"router bgp {AS}")
        
        #config vpnv4
    commandes.append("address-family vpnv4")
    for PEVoisin in trouve_PE_AS(AS,data):
        loopbackVoisin=getIpLoopback(PEVoisin,config)
        commandes.append(f"neighbor {loopbackVoisin} activate")
        commandes.append(f"neighbor {loopbackVoisin} send-community extended")
    commandes.append("exit-address-family")  

    #config vrf avec les clients
    for client,CE,interface in getInterfacesClient(routeur,AS,data):
        commandes.append(f"address-family ipv4 vrf {client}")
        ipvoisin=getIpVoisin(routeur,CE,config)
        asVoisin=get_as_for_router()
        commandes.append(f"neighbor {ipvoisin} remote-as {asVoisin}")
        commandes.append(f"neighbor {ipvoisin} activate")
        commandes.append('exit-adress-family')
    

    commandes.append("end")
    return commandes


def getIpLoopback(routeur,config):
    return config[routeur]["loopback"]

def trouve_PE_AS(numAs,data):
    liste=[]
    for routeur in data[numAs]["routeurs"]:
        if routeur_est_PE(routeur,numAs,data):
            liste.append(routeur)
    

def config_vrf_et_MP_BGP_routeur(routeur,AS,data,config):
    from vrf import config_vrf_routeur
    commandes=[]
    commandes+=config_vrf_routeur(routeur,AS,data)
    commandes+=configMp_BGP_routeur(routeur,AS,data,config)
    return commandes