import fltk
import os
import random
import time


hauteur_fenetre = 800 
largeur_fenetre = 800
decalage_fenetre = 200
nbr_carreau = 10

print(hauteur_fenetre)
hauteur_fenetre=hauteur_fenetre//nbr_carreau*nbr_carreau
print(hauteur_fenetre)
largeur_fenetre=largeur_fenetre//nbr_carreau*nbr_carreau
fltk.cree_fenetre(largeur_fenetre, hauteur_fenetre)


# On récupère les dimensions de la fenêtre après sa création
hauteur_fenetre = fltk.hauteur_fenetre()  # Récupère la hauteur de la fenêtre dynamique
largeur_fenetre = fltk.largeur_fenetre()  # Récupère la largeur de la fenêtre dynamique

# Calculer la taille des tuiles (en fonction de la taille de la fenêtre et du nombre de carreaux)
hauteur_carreau = hauteur_fenetre // nbr_carreau
largeur_carreau = largeur_fenetre // nbr_carreau

# Calculer les décals pour laisser de l'espace entre les tuiles
decalage_haut = hauteur_carreau - decalage_fenetre//nbr_carreau
decalage_larg = largeur_carreau - decalage_fenetre//nbr_carreau

# Charger la liste des tuiles
liste_tuiles = os.listdir('tuiles_v2/')
liste_tuiles = [nom[:-4] for nom in liste_tuiles if nom.endswith('.png') and len(nom[:-4]) == 4]

def afficher_tuiles(liste_num, liste_tuiles, nbr_car):
    """Affiche les tuiles possibles pour la case cliquée.
    
    Paramètres :
    list_num                -Permet de savoir quel tuiles afficher (si le joueur scroll parmis les tuiles)
    liste_tuiles            -Liste contenant le nom de toutes les tuiles possibles pour la case cliquée
    nbr_car                 -Nombre de carreaux de la map pour l'affichage

    Ne renvoie rien.
    """
    fltk.efface_tout()
    fltk.rectangle(100, 100, hauteur_fenetre-100, largeur_fenetre-100, "pink", "pink")
    for x in range(len(liste_num)):
        for y in range(len(liste_num[x])):
            num_ligne = liste_num[x][y][1]
            num_colon = liste_num[x][y][0]
            if nbr_car * num_colon + num_ligne < len(liste_tuiles):
                fltk.image(y * decalage_larg + 105, x * decalage_haut + 105, "tuiles_v2/" + liste_tuiles[nbr_car * num_colon + num_ligne]+".png", decalage_haut - 10, decalage_larg - 10, ancrage='nw', tag='image' + str(num_ligne) + str(num_colon))
    
    quad(nbr_carreau, hauteur_fenetre - decalage_fenetre, largeur_fenetre - decalage_fenetre, decalage_haut, decalage_larg, "pink", 100)



def quad(nbr_carreaux, haut_fenetre, larg_fenetre, haut_car, larg_car, couleur="black", decal=0):
    """Fait un quadrillage.

    Paramètres :
    haut_fenetre            -Hauteur de la fenêtre
    larg_fenetre            -Largeur de la fenêtre
    nbr_carreaux            -Nombre de carreaux de la map pour l'affichage
    haut_car                -Hauteur d'un carreau
    larg_car                -Largeur d'un carreau
    couleur                 -Couleur du quadrillage
    decal                   -Décalage si nécessaire du quadrillage

    Ne renvoie rien.
    """
    for x in range(1, nbr_carreaux):
        fltk.ligne((x) * larg_car + decal, haut_fenetre + decal, x * larg_car + decal, decal, couleur)
        fltk.ligne(larg_fenetre + decal, (x) * haut_car + decal, decal, x * haut_car + decal, couleur)

def afficher_carte(nbr_car, haut_fenetre, larg_fenetre, haut_car, larg_car, coos=(0,0)):
    """Affiche la carte actuelle.
    
    Paramètres :
    haut_fenetre            -Hauteur de la fenêtre
    larg_fenetre            -Largeur de la fenêtre
    nbr_car                 -Nombre de carreaux de la map pour l'affichage
    haut_car                -Hauteur d'un carreau
    larg_car                -Largeur d'un carreau
    coos                    -Tuple représentant les coordonées (latéraux, verticaux) de décalage lors du défilement

    Ne renvoie rien.
    """
    fltk.efface_tout()
    
    quad(nbr_car, haut_fenetre, larg_fenetre, haut_car, larg_car)
    for x in range(coos[0],coos[0]+nbr_car):
        for y in range(coos[1],coos[1]+nbr_car):
            if list_image[x][y] != None:
                fltk.image((y-coos[1]) * larg_car, (x-coos[0]) * haut_car, "tuiles_v2/" + list_image[x][y] + ".png", haut_car, larg_car, ancrage='nw', tag='image' + str(y) + str(x))


def afficher_decors(nbr_car, haut_car, larg_car, coos=(0,0)):
    """Affiche les décors.
    
    Paramètres :
    nbr_car                 -Nombre de carreaux de la map pour l'affichage
    haut_car                -Hauteur d'un carreau
    larg_car                -Largeur d'un carreau
    coos                    -Tuple représentant les coordonées (latéraux, verticaux) de décalage lors du défilement

    Ne renvoie rien.
    """
    
    for x in range(coos[0],coos[0]+nbr_car):
        for y in range(coos[1],coos[1]+nbr_car):
            if grille_dec[x][y] != None and grille_dec[x][y] != 'vu':
                fltk.image((y-coos[1]+grille_dec[x][y][0][0]) * larg_car, (x-coos[0]+grille_dec[x][y][0][1]) * haut_car, grille_dec[x][y][1], int(haut_car/grille_dec[x][y][2]), int(larg_car/grille_dec[x][y][2]), ancrage=grille_dec[x][y][3], tag='image' + str(y) + str(x))
            #if grille_dec_milieu[x][y] != None and grille_dec_milieu[x][y] != 'vu':
                #fltk.image((y-coos[1]+grille_dec_milieu[x][y][0][0]) * larg_car, (x-coos[0]+grille_dec_milieu[x][y][0][1]) * long_car, grille_dec_milieu[x][y][1], int(long_car/grille_dec_milieu[x][y][2]), int(larg_car/grille_dec_milieu[x][y][2]), ancrage=grille_dec_milieu[x][y][3], tag='image' + str(y) + str(x))


# Liste des images de tuiles
list_image = [[None for x in range(nbr_carreau)] for y in range(nbr_carreau)]

# Mode de sélection
mode = 'choisir_case'

quad(nbr_carreau, hauteur_fenetre, largeur_fenetre, hauteur_carreau, largeur_carreau)

def case_vide(grille):
    """Renvoie la liste des cases vides (None) dans la liste grille.
    
    Paramètres:
    grille                  -Grille à analyser

    Return: Renvoie une liste de liste
    """
    
    lst = []
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if grille[i][j] is None :
                lst.append((i,j))
    return lst

def emplacement_valide(grille, i, j, tuile):
   
    haut, droite, bas, gauche = tuile
    #dessus
    if i > 0 and grille[i-1][j] is not None:
        tuile_voisine = grille[i-1][j]
        if tuile_voisine[2] != haut:
            return False

    #dessous
    if i < len(grille) - 1 and grille[i+1][j] is not None:
        tuile_voisine = grille[i+1][j]
        if tuile_voisine[0] != bas:
            return False
    
    #gauche
    if j > 0 and grille[i][j-1] is not None:
        tuile_voisine = grille[i][j-1]
        if tuile_voisine[1] != gauche:
            return False
    
    #droite
    if j < len(grille[0])-1 and grille[i][j+1] is not None:
        tuile_voisine = grille[i][j+1]
        print("ui")
        if tuile_voisine[3] != droite:
            return False
    return True

def tuiles_possibles(grille,i,j): # i -> colonne; j -> ligne;
    """Recherche l'ensemble des tuiles possibles pour la case de coordonées i j
    
    Paramètres:
    grille                  -La grille à analyser
    i                       -Représente la colonne de la case
    j                       -Représente la ligne de la case

    Return: Renvoie la liste de toutes les tuiles possibles à cette position.
    """
    
    #Vérifie si il y a une case sur les côtés, si oui elle retient le raccord nécessaire
    if j-1 >=0:
        gauche = grille[i][j-1][1] if grille[i][j-1]!=None else '0' 
    else :
        gauche = '0'
    if j+1 <len(grille[0]):
        droite = grille[i][j+1][3] if grille[i][j+1]!=None else '0' 
    else :
        droite = '0'
    if i-1 >=0:
        haut = grille[i-1][j][2] if grille[i-1][j]!=None else '0' 
    else :
        haut = '0'
    if i+1 <len(grille):
        bas = grille[i+1][j][0] if grille[i+1][j]!=None else '0' 
    else :
        bas = '0'

    #Recherche l'ensemble des cases qui correspondent aux critères demandés
    list_intermediaire=[]
    for tuile in liste_tuiles:
        if (tuile[3]==gauche or gauche=='0') and (tuile[1]==droite or droite=='0') and (tuile[0]==haut or haut=='0') and (tuile[2]==bas or bas=='0'):
            list_intermediaire.append(tuile)

    #Récupère la listes des rivières liées à un océan
    if gauche=='R' or droite=='R' or haut=='R' or bas=='R':
        list_valide=[]
        for z in range(len(list_intermediaire)):
            if 'R' in list_intermediaire[z] and ('D' in list_intermediaire[z] or 'G'  in list_intermediaire[z] or 'B'  in list_intermediaire[z] or 'H'  in list_intermediaire[z]):
                pass
            else:
                list_valide.append(list_intermediaire[z])
    else:
        list_valide=[]
        for z in range(len(list_intermediaire)):
            if 'R' in list_intermediaire[z] and 'D' not in list_intermediaire[z] and 'G' not in list_intermediaire[z] and 'B' not in list_intermediaire[z] and 'H' not in list_intermediaire[z]:
                pass
            else:
                list_valide.append(list_intermediaire[z])
   
   #Gestion des rivières liées à l'océan
    lst_finale=[]
    for tuile in list_valide:
        ajout=True
        if (tuile[3]=='R' and gauche=='0') :
            if i-1>0 and j-1>0  and grille_riv[i-1][j-1]=='end':
                ajout=False
            if j-1>0 and len(grille_riv)>i+1 and grille_riv[i+1][j-1]=='end':
                ajout=False
            if j-2>0 and  grille_riv[i][j-2]=='end':
                ajout=False
            
        if (tuile[1]=='R' and droite=='0') :
            if len(grille_riv)>i+1 and len(grille_riv[i+1])>j+1  and grille_riv[i+1][j+1]=='end':
                ajout=False
            if i-1>0 and len(grille_riv[i-1])>j+1 and grille_riv[i-1][j+1]=='end':
                ajout=False
            if len(grille_riv[i])>j+2 and  grille_riv[i][j+2]=='end':
                ajout=False

        if (tuile[0]=='R' and haut=='0') :
            if i-1>0 and j-1>0  and grille_riv[i-1][j-1]=='end':
                ajout=False
            if i-1>0 and len(grille_riv[i-1])>j+1 and grille_riv[i-1][j+1]=='end':
                ajout=False
            if i-2>0 and  grille_riv[i-2][j]=='end':
                ajout=False

        if (tuile[2]=='R' and bas=='0') :
            if len(grille_riv)>i+1 and j-1>0  and grille_riv[i+1][j-1]=='end':
                ajout=False
            if len(grille_riv)>i+1 and len(grille_riv[i-1])>j+1 and grille_riv[i+1][j+1]=='end':
                ajout=False
            if len(grille_riv)>i+2 and  grille_riv[i+2][j]=='end':
                ajout=False
        
        if ajout==True:
            lst_finale.append(tuile)
    #Fin de la gestion des rivières
   

    return lst_finale


def solveur(grille):
    vide = case_vide(grille)
    if not vide:
        return True
    i, j = vide[0]
    tuiles = tuiles_possibles(grille,i,j)
    for tuile in tuiles:
        grille[i][j] = tuile
        if solveur(grille):
            return True
        grille[i][j] = None
    
    return False

def case_plus_contrainte(grille):
    """Recherche la case avec le plus de contraintes.
    
    Paramètres :
    grille                  -Grille à analyser

    Return: Renvoie un triplet avec les coordonnées i et j de la case et les possibilites pour cette case.
    """
    
    minimum = None
    meilleure_case = None

    for i in range (len(grille)):
        for j in range(len(grille[0])):
            if grille[i][j] == None:
                possibilites  = tuiles_possibles(grille,i,j)
                nombre = len(possibilites)
                if nombre == 0:
                    return(i,j,[])
                if minimum == None or nombre < minimum:
                    minimum = nombre
                    meilleure_case =(i,j,possibilites)
    return meilleure_case


def effacer_autour(i,j):
    """Efface les tuiles autour d'une case déterminée
    
    Paramètres:
    i                       -Représente la colonne de la case ciblée
    j                       -Représente la ligne de la case ciblée


    Ne renvoie rien.
    """
    
    for x in range(i-3,i+3):
        for y in range(j-3,j+3):
            if y>=0 and x>=0 and y<len(list_image) and x<len(list_image[0]):
                list_image[y][x]=None
                fltk.efface('image'+str(x)+str(y))
    fltk.mise_a_jour()
    



def solveur2(grille, dico, coos):
    """Solveur récurcif cherchant la case avec le plus de contraintes.
    
    Paramètres:
    grille                  -Grille à solver
    dico                    -Dictionnaire vérifiant combien de tentatives ont été effectuées sur chaque case
    coos                    -Coordonnées du décalage en cas de défilement


    Renvoie True ou False.
    """
    
    case = case_plus_contrainte(grille)

    if case == None:
        return True
    i, j, tuiles = case
    if i== 0 and j ==0 :
        print(tuiles,len(tuiles))
    n=0
    random.shuffle(tuiles)
    if tuiles != []:
        if 'SSSS' not in tuiles:
            while n < 10 and 'S' not in tuiles[0]:
                random.shuffle(tuiles)
                n+=1
        elif 'SSSS' in tuiles :
            a = [1,2,3,4,5]
            random.shuffle(a)
            if a[0]!=2:
                for x in range(len(tuiles)):
                    if tuiles[x]=='SSSS':
                        tuiles[x]=tuiles[0]
                        tuiles[0]='SSSS'
    for tuile in tuiles:
        grille[i][j] = tuile

        # Ajoute à la liste
        list_image[i][j] = tuile    

        # Gestion des rivières
        if 'R' in tuile:
            grille_riv[i][j] = 'end'
        else :
            grille_riv[i][j] = '0'

        if solveur2(grille,dico, coos):
            
            return True
        grille[i][j] = None


        dico=dico.copy()
        dico[str(j)+','+str(i)]+=1
        if dico[str(j)+','+str(i)]>=50:
            effacer_autour(j,i)
            grille=list_image
            dico[str(j)+','+str(i)]=0
            
    
    return False



grille_riv = [[None for x in range(nbr_carreau)] for y in range(nbr_carreau)]
grille_dec = [[None for x in range(nbr_carreau)] for y in range(nbr_carreau)]
grille_dec_milieu = [[None for x in range(nbr_carreau)] for y in range(nbr_carreau)]

def decor(nbr_carreau, hauteur_carreau, largeur_carreau, list_image):
    """Détermine les décors dans la mer et sur la terre.
    
    Paramètres:
    nbr_carreau             -Nombre de carreau de la map pour afficher les décors
    hauteur_carreau         -Hauteur d'un carreau
    largeur_carreau         -Largeur d'un carreau

    Ne renvoie rien.
    """
    
    #Gestion des décors maritimes
    for x in range(0,len(list_image)):
        for y in range(0,len(list_image[x])):
            if grille_dec[x][y]==None:
                a = [x for x in range(15)]
                b = random.choice(a)
                if list_image [x][y] == 'SSSS':
                    if b == 2 or b == 3:
                        c=random.choice(['sieren/siren_e.png','serpent_v2.png','sieren/siren_n.png','sieren/siren_l.png'])
                        if c != 'serpent_v2.png':
                            grille_dec[x][y] = [(0.33,0.33),"decors/mer/"+c,3,'nw']
                        else :
                            grille_dec[x][y] = [(0.25,0.25),"decors/mer/"+c,2,'nw']
                    elif b == 1:    
                            grille_dec[x][y] = [(0,0),"decors/mer/ship_v2.png",1.3,'nw']
                    else:
                            grille_dec[x][y] = 'vu'

    #Gestion des décors terrestres 
    for x in range(0,len(list_image)):
        for y in range(0,len(list_image[x])):
            if grille_dec[x][y]==None:
                #Charger la liste des décors terrestres
                decorsa = os.listdir('decors/terre/')
                decors = []
                for dec in decorsa :
                    if 'grass' not in dec and 'field' not in dec:
                        decors.append(dec)
                a = [x for x in range(15)]
                b = random.choice(a)

                #Décors sur 1 seule case
                if b in [x for x in range(5)]:
                    #bordures
                    if list_image [x][y][3] == 'H' and list_image[x][y][2] == 'P'and list_image[x][y][1] == 'H':
                        zzzz = random.choice(decors)
                        grille_dec[x][y] = [(0.25,0.5),"decors/terre/"+zzzz,2,'nw']
                    
                    if list_image [x][y][0] == 'G' and list_image[x][y][1] == 'P'and list_image[x][y][2] == 'G':
                        zzzz = random.choice(decors)
                        grille_dec[x][y] = [(0.5,0.25),"decors/terre/"+zzzz,2,'nw']
                    
                    if list_image [x][y][3] == 'B' and list_image[x][y][0] == 'P'and list_image[x][y][1] == 'B':
                        zzzz = random.choice(decors)
                        grille_dec[x][y] = [(0.25,0),"decors/terre/"+zzzz,2,'nw']
                    
                    if list_image [x][y][0] == 'D' and list_image[x][y][3] == 'P'and list_image[x][y][2] == 'D':
                        zzzz = random.choice(decors)
                        grille_dec[x][y] = [(0,0.5),"decors/terre/"+zzzz,2,'nw']
            
                    #angles
                    if list_image [x][y]=='GBSS':
                        zzzz = random.choice(decors)
                        grille_dec[x][y] = [(0.5,0.6),"decors/terre/"+zzzz,2.5,'sw']
            
                    if list_image [x][y]=='SHGS':
                        zzzz = random.choice(decors)
                        grille_dec[x][y] = [(0.5,0.4),"decors/terre/"+zzzz,2.5,'nw']
            
                    if list_image [x][y]=='SSDH':
                        zzzz = random.choice(decors)
                        grille_dec[x][y] = [(0.5,0.4),"decors/terre/"+zzzz,2.5,'ne']
            
                    if list_image [x][y]=='DSSB':
                        zzzz = random.choice(decors)
                        grille_dec[x][y] = [(0.5,0.6),"decors/terre/"+zzzz,2.5,'se']
            
                   
                else:
                    grille_dec[x][y] = 'vu'
    
                #Décors entre plusieurs case
                if x > len(list_image)-1 and y > len(list_image)-1:
                    if b in [6,7,8]:
                        un = (list_image [x][y][1] == 'P' or list_image [x][y][1] == 'R' or list_image [x][y][1] == 'H') and (list_image [x][y][2] == 'P' or list_image [x][y][2] == 'R' or list_image [x][y][2] == 'G')

                        deux = (list_image [x+1][y][0] == 'P' or list_image [x+1][y][0] == 'R' or list_image [x+1][y][0] == 'G') and (list_image [x+1][y][1] == 'P' or list_image [x+1][y][1] == 'R' or list_image [x+1][y][1] == 'B')
                        
                        trois = (list_image [x][y+1][2] == 'P' or list_image [x][y+1][2] == 'R' or list_image [x][y+1][2] == 'D') and (list_image [x][y+1][3] == 'P' or list_image [x][y+1][3] == 'R' or list_image [x][y+1][3] == 'H')
                        
                        quatre = (list_image [x+1][y+1][0] == 'P' or list_image [x+1][y+1][0] == 'R' or list_image [x+1][y+1][0] == 'D') and (list_image [x+1][y+1][3] == 'P' or list_image [x+1][y+1][3] == 'R' or list_image [x+1][y+1][3] == 'B')


                        if un and deux and trois and quatre :
                            zzzz=random.choice(decors)
                            grille_dec_milieu[x][y]=[(0.85,0.85),"decors/terre/"+zzzz,3,'nw']
                    else:
                        grille_dec_milieu[x][y]='vu'

    #Appelle la fonction afficher_decors qui affiche les décors à partir des listes globales grille_dec et grille_dec_milieu
    afficher_decors(nbr_carreau, hauteur_carreau, largeur_carreau, coord)


def menu():
    """Menu principal de jeu.

    Renvoie le mode de jeu choisit.
    """
    
    fltk.efface_tout()
    fltk.mise_a_jour()
    fltk.image(0, 0, "menu1.png", 800, 800, "nw")
    fltk.mise_a_jour()
    while True:
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        if tev == "ClicGauche":
            break
        
        elif tev == "Quitte":
            fltk.ferme_fenetre()
            exit()
        fltk.texte(250, 500, "cliquez sur une touche", "#c86598")
        fltk.mise_a_jour()
        time.sleep(0.5)
        fltk.texte(250, 500, "cliquez sur une touche", "#32683f")
        fltk.mise_a_jour()
        time.sleep(0.5)
        fltk.mise_a_jour()
    #time.sleep(2)
    fltk.image(0, 0, "menu2.png", 800, 800, "nw")
    fltk.mise_a_jour()
    fltk.texte(308, 340, "MAP MAKER", "#32683f")
    fltk.texte(312, 470, "MAP GAME", "#32683f")
    fltk.texte(330, 594, "QUITTER", "#32683f")
"""
def menu_jeu():
    fltk.efface_tout()
    fltk.mise_a_jour()
    fltk.image(0, 0, "menu3.png", 800, 800, "nw")
    fltk.mise_a_jour()
    while True:
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        if tev == "ClicGauche":
            break
        
        elif tev == "Quitte":
            fltk.ferme_fenetre()
            exit()
        fltk.texte(250, 500, "cliquez sur une touche", "#c86598")
        fltk.mise_a_jour()
        time.sleep(0.5)
        fltk.texte(250, 500, "cliquez sur une touche", "#32683f")
        fltk.mise_a_jour()
        time.sleep(0.5)
        fltk.mise_a_jour()
    #time.sleep(2)
    fltk.image(0, 0, "menu2.png", 800, 800, "nw")
    fltk.mise_a_jour()
    fltk.texte(308, 340, "MAP MAKER", "#32683f")
    fltk.texte(312, 470, "MAP GAME", "#32683f")
    fltk.texte(330, 594, "QUITTER", "#32683f")



    # Coordonnées pour les zones cliquables
    while True:
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        if tev == "ClicGauche":
            x = fltk.abscisse(ev)
            y = fltk.ordonnee(ev)
            # MAP MAKER (autour de 308, 340)
            if 290 <= x <= 510 and 320 <= y <= 400:
                return "map maker"
            # MAP GAME (autour de 312, 470)
            elif 290 <= x <= 510 and 450 <= y <= 530:
                print('b')
                return "map game"
            # QUITTER (autour de 330, 594)
            elif 290 <= x <= 510 and 570 <= y <= 610:
                print('c')
                return "quitter"
        elif tev == "Quitte":
            fltk.ferme_fenetre()
            exit()

        fltk.mise_a_jour()
"""
coord=(0,0)
completion='auto'





menu=menu()

#une fois le menu fermé et le mode choisit, lance le jeu.
if menu == "map game":
    print('s')
    fltk.efface_tout()
    fltk.texte(312,400,"CREEPER ?")
    fltk.texte(312,500,"BOATS")
    while True:
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev) 
    
        fltk.mise_a_jour()
        if tev == "ClicGauche":
            pass
        elif tev == "Quitte":
            fltk.ferme_fenetre()
            exit()


elif menu == "map maker":
    afficher_carte(nbr_carreau, hauteur_fenetre, largeur_fenetre, hauteur_carreau, largeur_carreau)
    while True:
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev) 

        if tev == "Scroll" or tev == "Up" or tev == "Down":
            if mode == 'choisir_tuile':
                if tev == "Scroll":
                    direction = int(fltk.attribut(ev, "delta") / 120)
                elif tev == "Up":
                    direction = 1
                elif tev == "Down":
                    direction = -1
                # Scroll vers le haut en décalant les images
                if liste_num_affichage[0][0][0] != 0 and direction == 1:
                    for x in range(len(liste_num_affichage)):
                        for y in range(len(liste_num_affichage[x])):
                            lig = liste_num_affichage[x][y][1]
                            col = liste_num_affichage[x][y][0]
                            liste_num_affichage[x][y] = (col - direction, lig)
                # Scroll vers le bas en décalant les images            
                if liste_num_affichage[-1][-1][0] < (len(list_valide) // nbr_carreau) and direction == -1:
                    for x in range(len(liste_num_affichage)):
                        for y in range(len(liste_num_affichage[x])):
                            lig = liste_num_affichage[x][y][1]
                            col = liste_num_affichage[x][y][0]
                            liste_num_affichage[x][y] = (col - direction, lig)

                # Affiche la nouvelle liste d'image (avec décalage du scroll)
                afficher_tuiles(liste_num_affichage, list_valide, nbr_carreau)

        if tev == "ClicGauche":
            if mode == 'choisir_case':
                # Récupère les coordonnées de la case cliquée
                num_col = fltk.ordonnee_souris() // hauteur_carreau + coord[0]
                num_lig = fltk.abscisse_souris() // largeur_carreau + coord[1]

                list_valide = tuiles_possibles(list_image,num_col,num_lig)

                # Si il y a au moins une case valide, affiche tous les tuiles possibles
                if list_valide != []:
                    liste_num_affichage = [[(y, x) for x in range(nbr_carreau)] for y in range(nbr_carreau)]
                    afficher_tuiles(liste_num_affichage, list_valide, nbr_carreau)
                    mode = 'choisir_tuile'

            elif mode == 'choisir_tuile':
                # Récupère les coordonnées de la tuile cliquée
                x = fltk.ordonnee_souris() 
                y = fltk.abscisse_souris() 
                
                #Les 3 lignes suivantes résolvent le problème de clics décalés sur la fenêtre de choix
                if x> decalage_fenetre//2 and y > decalage_fenetre//2 and x<hauteur_fenetre-decalage_fenetre//2 and y<largeur_fenetre-decalage_fenetre//2:
                    x = int((x-decalage_fenetre//2)/(hauteur_fenetre-decalage_fenetre)*hauteur_fenetre//hauteur_carreau)
                    y = int((y-decalage_fenetre//2)/(largeur_fenetre-decalage_fenetre)*largeur_fenetre//largeur_carreau) 
                    
                    if liste_num_affichage[x][y][1] + nbr_carreau * liste_num_affichage[x][y][0] < len(list_valide):
                        # Définit la nouvelle case
                        case = list_valide[liste_num_affichage[x][y][1] + nbr_carreau * liste_num_affichage[x][y][0]]

                        # Ajoute à la liste
                        list_image[num_col][num_lig] = case    

                        #rivière
                        if 'R' in case:
                            grille_riv[num_col][num_lig] = 'end'
                        else :
                            grille_riv[num_col][num_lig] = '0'

                        

                        # Réaffiche la carte
                        afficher_carte(nbr_carreau, hauteur_fenetre, largeur_fenetre, hauteur_carreau, largeur_carreau)

                        # Change le mode pour choisir une nouvelle case
                        mode = 'choisir_case'

        if tev == "ClicDroit":
            if mode == 'choisir_case':
                # Récupère les coordonnées de la case à supprimer
                y_sup = fltk.ordonnee_souris() // hauteur_carreau + coord[1]
                x_sup = fltk.abscisse_souris() // largeur_carreau + coord[0]
                fltk.efface('image' + str(x_sup) + str(y_sup))
                list_image[y_sup][x_sup] = None

        if tev == "Touche":
            touche_ev = fltk.touche(ev)
            
            if mode == 'choisir_case':

                if touche_ev == "Up":
                    if coord[0]==0:
                        grille_dec.insert(0,[None for x in range(len(list_image[-1]))])
                        grille_dec_milieu.insert(0,[None for x in range(len(list_image[-1]))])
                        grille_riv.insert(0,[None for x in range(len(list_image[-1]))])
                        list_image.insert(0,[None for x in range(len(list_image[-1]))])
                        
                    else:
                        coord=(coord[0]-1,coord[1])
                        

                if touche_ev == "Down":
                    if coord[0]+nbr_carreau==len(list_image):
                        grille_dec.append([None for x in range(len(list_image[0]))])
                        grille_dec_milieu.append([None for x in range(len(list_image[0]))])
                        grille_riv.append([None for x in range(len(list_image[0]))])
                        list_image.append([None for x in range(len(list_image[0]))])
                    coord=(coord[0]+1,coord[1])
                        


                if touche_ev == "Left":
                    if coord[1]==0:
                        for x in range(len(list_image)):
                            grille_dec[x].insert(0,None)
                            grille_dec_milieu[x].insert(0,None)
                            grille_riv[x].insert(0,None)
                            list_image[x].insert(0,None)
                    else:
                        coord=(coord[0],coord[1]-1)

                if touche_ev == "Right":
                    if coord[1]+nbr_carreau==len(list_image[0]):
                        for x in range(len(list_image)):
                            grille_dec[x].append(None)
                            grille_dec_milieu[x].append(None)
                            grille_riv[x].append(None)
                            list_image[x].append(None)
                    coord=(coord[0],coord[1]+1)
                        
                    

                if touche_ev in ['Up','Down','Left','Right']:
                    if completion=='auto':
                            dictionr = {}
                            for n in range(len(list_image)):
                                for m in range(len(list_image[n])):
                                    dictionr[str(m)+','+str(n)]=0
                            if solveur2(list_image,dictionr, coord):
                                afficher_carte(nbr_carreau, hauteur_fenetre, largeur_fenetre, hauteur_carreau, largeur_carreau,coord)
                                decor(nbr_carreau, hauteur_carreau, largeur_carreau,list_image)
                            else:
                                print("impossible de compléter la carte")
                                fltk.texte(largeur_fenetre // 2, hauteur_fenetre - 20, "carte impossible à compléter", taille=16, couleur='red', ancrage='center')
                    else:
                        afficher_carte(nbr_carreau, hauteur_fenetre, largeur_fenetre, hauteur_carreau, largeur_carreau,coord)
                        decor(nbr_carreau, hauteur_carreau, largeur_carreau,list_image)


                if touche_ev == "l":
                    num_col = fltk.ordonnee_souris() // hauteur_carreau
                    num_lig = fltk.abscisse_souris() // largeur_carreau
                    print(list_image[num_col+coord[1]][num_lig+coord[0]])

                elif touche_ev == "s":
                    print("solveur lancé")
                    dictionr = {}
                    for n in range(len(list_image)):
                        for m in range(len(list_image[n])):
                            dictionr[str(m)+','+str(n)]=0
                    if solveur2(list_image,dictionr, coord):
                        print("carte complétée")
                        afficher_carte(nbr_carreau, hauteur_fenetre, largeur_fenetre, hauteur_carreau, largeur_carreau,coord)
                        decor(nbr_carreau, hauteur_carreau, largeur_carreau,list_image)
                    else:
                        print("impossible de compléter la carte")
                        fltk.texte(largeur_fenetre // 2, hauteur_fenetre - 20, "carte impossible à compléter", taille=16, couleur='red', ancrage='center')

                elif touche_ev=='r':
                    for tab in grille_riv:
                        print(tab)

                elif touche_ev=='m':
                    #Efface Tout
                    coord=(0,0)
                    list_image = [[None for x in range(nbr_carreau)] for y in range(nbr_carreau)]
                    grille_dec = [[None for x in range(nbr_carreau)] for y in range(nbr_carreau)]
                    grille_dec_milieu = [[None for x in range(nbr_carreau)] for y in range(nbr_carreau)]
                    grille_riv = [[None for x in range(nbr_carreau)] for y in range(nbr_carreau)]
                    afficher_carte(nbr_carreau, hauteur_fenetre, largeur_fenetre, hauteur_carreau, largeur_carreau)
                    afficher_decors(nbr_carreau, hauteur_carreau, largeur_carreau,coord)

                elif touche_ev=="d":
                    decor(nbr_carreau, hauteur_fenetre, largeur_fenetre, hauteur_carreau, largeur_carreau,list_image)
                #elif touche_ev=="k":
                    
                    
            

        if tev == "Quitte":
            print("Fin de partie")
            fltk.ferme_fenetre()
            break

        fltk.mise_a_jour()

