# Projet Configuration auto d'un réseau sur GNS3

Le Programme principal ([gns.py](https://github.com/mortcailloux/GNS3/blob/main/gns.py)) permet de configurer automatiquement tous les routeurs suivant le fichier d'intention [normal](https://github.com/mortcailloux/GNS3/blob/main/reseau_officiel.json) ou avec [policies](https://github.com/mortcailloux/GNS3/blob/main/reseau_officiel_policies.json). 

## structure du projet:
Le projet est structuré en plusieurs modules dont la description est donnée ci-dessous:
- [BGP.py](https://github.com/CharlesBouquet1011/GNS3_MP-BGP/blob/main/BGP.py): génère les commandes relatives à BGP pour la configuration des routeurs.
- [adressage.py](https://github.com/CharlesBouquet1011/GNS3_MP-BGP/blob/main/adressage.py): génère dynamiquement les adresses ip des interfaces puis génère les commandes de configuration relatives aux IP et aux interfaces pour la configuration des routeurs.
- [gns.py](https://github.com/CharlesBouquet1011/GNS3_MP-BGP/blob/main/adressage_loopback.py): permet de configurer tous les routeurs en combinant les modules. Lance telnet et l'écriture de config sur des process indépendants afin de pouvoir continuer à générer les commandes en parallèle.
- [adressage_loopback.py](https://github.com/CharlesBouquet1011/GNS3_MP-BGP/blob/main/adressage_loopback.py): permet de configurer les interfaces de loopback en générant les commandes correspondantes.
- [ospf.py](https://github.com/CharlesBouquet1011/GNS3_MP-BGP/blob/main/adressage_loopback.py): permet de générer les commandes nécessaires pour configurer OSPF sur les routeurs concernés.
- [fichier_intention.json](https://github.com/CharlesBouquet1011/GNS3_MP-BGP/blob/main/adressage_loopback.py): fichier d'intention décrivant le réseau pour la démo avec les policies (on a rajouté des routeurs et des AS pour pouvoir montrer que cela fonctionne bien)
- [routeur_id.py](https://github.com/CharlesBouquet1011/GNS3_MP-BGP/blob/main/adressage_loopback.py): génère les router_id qui seront utilisés par BGP.py.
- [structure_config_noeud.json](https://github.com/CharlesBouquet1011/GNS3_MP-BGP/blob/main/structure_config_noeud.json): fichier qui décrit à quoi ressemble notre dictionnaire de configuration des noeuds (qui est généré au cours du programme). Pratique pour s'y retrouver dans le code.
- [telnet.py](https://github.com/CharlesBouquet1011/GNS3_MP-BGP/blob/main/telnet.py): fichier qui contient les fonctions qui permettent d'écrire les commandes dans la console du routeur.
- [write_config.py](https://github.com/CharlesBouquet1011/GNS3_MP-BGP/blob/main/write_config.py): permet d'écrire la config dans un fichier et de formatter le nom du fichier conformément à gns3.
- [vrf.py](https://github.com/CharlesBouquet1011/GNS3_MP-BGP/blob/main/vrf.py): gère la configuration des vrf
- [MP_BGP.py](https://github.com/CharlesBouquet1011/GNS3_MP-BGP/blob/main/MP_BGP.py): configure MP BGP, contient une fonction qui configure à la fois MP BGP et les vrf à l'aide de fonctions du module vrf.



## Execution du programme:
Il suffit de lancer le script [gns.py](https://github.com/mortcailloux/GNS3/blob/main/gns.py) en ayant gns3 de lancé, rentrez ensuite le nom de votre projet qui correspond au graphe décrit dans le fichier d'intention.
## librairies utilisées:
Le programme utilise telnetlib, gns3fy, multiprocessing et json. Il vous faudra installer la librairie correspondante s'il vous la manque. Attention, telnetlib n'est plus disponible à partir de python 3.13

## structure du fichier d'intention:
la première clé est le numéro de l'AS, ensuite on a le choix entre protocole (qui sert à récupérer le protocole utilisé dans l'as), routeurs (qui sert à savoir quels routeurs sont présents dans l'as) et relation qui permet d'établir les relations clients/peer/provider de cet as vers les autres as.
Dans les routeurs, on retrouve un dictionnaire à chaque routeur dans lequel on retrouve les interfaces associés aux routeurs auxquelles elles sont connectées et le coût OSPF associé (on peut le modifier)
la clé CE permet d'annoncer les CE d'un AS et la clé annonce réseau permet de mettre les routeurs qui vont annoncer tous les réseaux auxquels il sont connectés. La clé Plage IP sert à annoncer quelle plage IP va être utilisée par un AS.

# fonctionnalités prises en charge:
- génération automatique d'IPv4 et attribution des ips aux interfaces via telnet.
- déploiement d'OSPF dans un AS via telnet
- déploiement de BGP sur tous les AS via telnet
- déploiement des policies BGP pour une gestion plus approfondie du trafic via telnet.
- export des configurations des routeurs dans des fichiers.cfg
- permet d'annoncer des réseaux précis dans BGP ou tous les réseaux d'un routeur spécifique dans BGP.
- permet de configurer des vrf et MP BGP afin de faire des routes VPN.
- prend également en charge du multiprocessing pour que les configurations soient calculées et envoyées au plus vite aux différents routeurs sur GNS3.


Pour BGP, on prend en charge jusqu'à 255 routeurs (on génère les routeurs id de façon dynamique) et on génère les adresses de loopback automatiquement.

