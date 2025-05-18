print('Hello World !')
import fltk
import os
import random
import time

hauteur_fenetre = 900 
largeur_fenetre = 900
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

def afficher_tuiles(liste_num, liste_tuiles, larg_car, haut_car, nbr_car):
    """Affiche les tuiles possibles pour la case cliquée."""
    fltk.efface_tout()
    fltk.rectangle(100, 100, hauteur_fenetre-100, largeur_fenetre-100, "pink", "pink")
    for x in range(len(liste_num)):
        for y in range(len(liste_num[x])):
            num_ligne = liste_num[x][y][1]
            num_colon = liste_num[x][y][0]
            if nbr_car * num_colon + num_ligne < len(liste_tuiles):
                fltk.image(y * decalage_larg + 105, x * decalage_haut + 105, "tuiles_v2/" + liste_tuiles[nbr_car * num_colon + num_ligne]+".png", decalage_haut - 10, decalage_larg - 10, ancrage='nw', tag='image' + str(num_ligne) + str(num_colon))
    
    quad(nbr_carreau, hauteur_fenetre - decalage_fenetre, largeur_fenetre - decalage_fenetre, decalage_haut, decalage_larg, "pink", 100)

def quad(nbr_carreaux, long_fenetre, larg_fenetre, long_car, larg_car, couleur="black", decal=0):
    """Fait un quadrillage."""
    for x in range(1, nbr_carreaux):
        fltk.ligne((x) * larg_car + decal, long_fenetre + decal, x * larg_car + decal, decal, couleur)
        fltk.ligne(larg_fenetre + decal, (x) * long_car + decal, decal, x * long_car + decal, couleur)

def afficher_carte(nbr_car, long, larg, long_car, larg_car, coos=(0,0)):
    """Affiche la carte actuelle."""
    fltk.efface_tout()
    
    quad(nbr_car, long, larg, long_car, larg_car)
    for x in range(coos[0],coos[0]+nbr_car):
        for y in range(coos[1],coos[1]+nbr_car):
            if list_image[x][y] != None:
                fltk.image((y-coos[1]) * larg_car, (x-coos[0]) * long_car, "tuiles_v2/" + list_image[x][y] + ".png", long_car, larg_car, ancrage='nw', tag='image' + str(y) + str(x))

# Liste des images de tuiles
list_image = [[None for x in range(nbr_carreau)] for y in range(nbr_carreau)]

# Mode de sélection
mode = 'choisir_case'

quad(nbr_carreau, hauteur_fenetre, largeur_fenetre, hauteur_carreau, largeur_carreau)

""" Partie de Nesma (A NE PAS TOUCHER) """
def case_vide(grille):
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
    #vérifie si il y a une case sur les côtés, si oui elle retiens le raccord nécessaire
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

    #recherche l'ensemble des cases qui correspondent aux critères demandés
    list_intermediaire=[]
    for tuile in liste_tuiles:
        if (tuile[3]==gauche or gauche=='0') and (tuile[1]==droite or droite=='0') and (tuile[0]==haut or haut=='0') and (tuile[2]==bas or bas=='0'):
            list_intermediaire.append(tuile)

    #RRRIIIIVVVIIIEEERRREEE GESTION
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
        #FIN RIVIERE GESTION
   

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


def effacer_autour(j,i):
    for x in range(j-3,j+3):
        for y in range(i-3,i+3):
            if y>=0 and x>=0 and y<len(list_image) and x<len(list_image[0]):
                list_image[y][x]=None
                fltk.efface('image'+str(x)+str(y))
    fltk.mise_a_jour()
    



def solveur2(grille, dico, coos):
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

        # gestion rivière
        if 'R' in tuile:
            grille_riv[i][j] = 'end'
        else :
            grille_riv[i][j] = '0'

        #affichage FLTK
        #fltk.image((j+coos[1])*largeur_carreau,(i+coos[0])*hauteur_carreau,"tuiles_v2/" + tuile + ".png", hauteur_carreau, largeur_carreau, ancrage = 'nw', tag = 'image'+str(j)+str(i))
        
        #time.sleep(0.01)
        #fin affichage FLTK
        if solveur2(grille,dico, coos):
            
            return True
        grille[i][j] = None


        #fltk.efface('image'+str(j)+str(i))
        dico=dico.copy()
        dico[str(j)+','+str(i)]+=1
        if dico[str(j)+','+str(i)]>=50:
            effacer_autour(j,i)
            grille=list_image
            dico[str(j)+','+str(i)]=0
            
        #fltk.mise_a_jour()
    
    return False

""" Fin partie Nesma bisous """


grille_riv = [[None for x in range(nbr_carreau)] for y in range(nbr_carreau)]
grille_dec = [[None for x in range(nbr_carreau)] for y in range(nbr_carreau)]

def decor(nbr_carreau, hauteur_fenetre, largeur_fenetre, hauteur_carreau, largeur_carreau, list_image):
    grille_dec = [[None for x in range(nbr_carreau)] for y in range(nbr_carreau)]
    for x in range(0,len(list_image)):
        for y in range(0,len(list_image[x])):
            fltk.efface('siren' + str(x) + str(y))

    for x in range(0,len(list_image)):
        for y in range(0,len(list_image[x])):
            a = [x for x in range(15)]
            b = random.choice(a)
            if list_image [x][y] == 'SSSS':
                if b == 2 or b == 3:
                    c=random.choice(['sieren/siren_e.png','serpent_v2.png','sieren/siren_n.png'])
                    if c == 'siren.png':
                        fltk.image((y+0.3)*largeur_carreau,(x+0.33)*hauteur_carreau,"decors/mer/"+c, hauteur_carreau//3, largeur_carreau//3, ancrage = 'nw', tag = 'siren'+str(x)+str(y))
                    else :
                        fltk.image((y+0.25)*largeur_carreau,(x+0.25)*hauteur_carreau,"decors/mer/"+c, hauteur_carreau//2, largeur_carreau//2, ancrage = 'nw', tag = 'siren'+str(x)+str(y))
                    grille_dec[x][y] = 'poiscay'
                if b == 1:    
                        fltk.image((y)*largeur_carreau,(x)*hauteur_carreau,"decors/mer/ship_v2.png", int(hauteur_carreau/1.3), int(largeur_carreau/1.3), ancrage = 'nw', tag = 'siren'+str(x)+str(y))
    
    for x in range(0,len(list_image)):
        for y in range(0,len(list_image[x])):
            #Charger la liste des décors terrestres
            decorsa = os.listdir('decors/terre/')
            decors = []
            for dec in decorsa :
                if 'grass' not in dec and 'field' not in dec:
                    decors.append(dec)
            
            #bordures
            if list_image [x][y][3] == 'H' and list_image[x][y][2] == 'P'and list_image[x][y][1] == 'H':
                print('terre',x,y)
                fltk.image((y+0.25)*largeur_carreau,(x+0.5)*hauteur_carreau,"decors/terre/"+random.choice(decors), int(hauteur_carreau/2), int(largeur_carreau/2), ancrage = 'nw', tag = 'siren'+str(x)+str(y))
            
            if list_image [x][y][0] == 'G' and list_image[x][y][1] == 'P'and list_image[x][y][2] == 'G':
                print('terre',x,y)
                fltk.image((y+0.5)*largeur_carreau,(x+0.25)*hauteur_carreau,"decors/terre/"+random.choice(decors), int(hauteur_carreau/2), int(largeur_carreau/2), ancrage = 'nw', tag = 'siren'+str(x)+str(y))
            
            if list_image [x][y][3] == 'B' and list_image[x][y][0] == 'P'and list_image[x][y][1] == 'B':
                print('terre',x,y)
                fltk.image((y+0.25)*largeur_carreau,(x)*hauteur_carreau,"decors/terre/"+random.choice(decors), int(hauteur_carreau/2), int(largeur_carreau/2), ancrage = 'nw', tag = 'siren'+str(x)+str(y))
            
            if list_image [x][y][0] == 'D' and list_image[x][y][3] == 'P'and list_image[x][y][2] == 'D':
                print('terre',x,y)
                fltk.image((y)*largeur_carreau,(x+0.25)*hauteur_carreau,"decors/terre/"+random.choice(decors), int(hauteur_carreau/2), int(largeur_carreau/2), ancrage = 'nw', tag = 'siren'+str(x)+str(y))
    
            #angles

            if list_image [x][y]=='GBSS':
                print('terre',x,y)
                fltk.image((y+0.5)*largeur_carreau,(x+0.6)*hauteur_carreau,"decors/terre/"+random.choice(decors), int(hauteur_carreau/2.5), int(largeur_carreau/2.5), ancrage = 'sw', tag = 'siren'+str(x)+str(y))
    
            if list_image [x][y]=='SHGS':
                print('terre',x,y)
                fltk.image((y+0.5)*largeur_carreau,(x+0.4)*hauteur_carreau,"decors/terre/"+random.choice(decors), int(hauteur_carreau/2.5), int(largeur_carreau/2.5), ancrage = 'nw', tag = 'siren'+str(x)+str(y))
    
            if list_image [x][y]=='SSDH':
                print('terre',x,y)
                fltk.image((y+0.5)*largeur_carreau,(x+0.4)*hauteur_carreau,"decors/terre/"+random.choice(decors), int(hauteur_carreau/2.5), int(largeur_carreau/2.5), ancrage = 'ne', tag = 'siren'+str(x)+str(y))
    
            if list_image [x][y]=='DSSB':
                print('terre',x,y)
                fltk.image((y+0.5)*largeur_carreau,(x+0.6)*hauteur_carreau,"decors/terre/"+random.choice(decors), int(hauteur_carreau/2.5), int(largeur_carreau/2.5), ancrage = 'se', tag = 'siren'+str(x)+str(y))
    
            #milieux

    for x in range(0,len(list_image)-1):
        for y in range(0,len(list_image[x])-1):
            #print(x,y)
            un = (list_image [x][y][1] == 'P' or list_image [x][y][1] == 'R' or list_image [x][y][1] == 'H') and (list_image [x][y][2] == 'P' or list_image [x][y][2] == 'R' or list_image [x][y][2] == 'G')
            #print('un',list_image[x][y])

            deux = (list_image [x+1][y][0] == 'P' or list_image [x+1][y][0] == 'R' or list_image [x+1][y][0] == 'G') and (list_image [x+1][y][1] == 'P' or list_image [x+1][y][1] == 'R' or list_image [x+1][y][1] == 'B')
            #print('de',list_image[x+1][y])
            
            trois = (list_image [x][y+1][2] == 'P' or list_image [x][y+1][2] == 'R' or list_image [x][y+1][2] == 'D') and (list_image [x][y+1][3] == 'P' or list_image [x][y+1][3] == 'R' or list_image [x][y+1][3] == 'H')
            #print('tr',list_image[x][y+1])
            
            quatre = (list_image [x+1][y+1][0] == 'P' or list_image [x+1][y+1][0] == 'R' or list_image [x+1][y+1][0] == 'D') and (list_image [x+1][y+1][3] == 'P' or list_image [x+1][y+1][3] == 'R' or list_image [x+1][y+1][3] == 'B')
            #print('qu',list_image[x+1][y+1])


            if un and deux and trois and quatre :
                print(x,y,x+1,y+1)
                fltk.image((y+0.85)*largeur_carreau,(x+0.85)*hauteur_carreau,"decors/terre/"+random.choice(decors), int(hauteur_carreau/3), int(largeur_carreau/3), ancrage = 'nw', tag = 'siren'+str(x)+str(y))




    fltk.mise_a_jour()


coord=(0,0)
completion='auto'

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
            afficher_tuiles(liste_num_affichage, list_valide, largeur_carreau, hauteur_carreau, nbr_carreau)

    if tev == "ClicGauche":
        if mode == 'choisir_case':
            # Récupère les coordonnées de la case cliquée
            num_col = fltk.ordonnee_souris() // hauteur_carreau
            num_lig = fltk.abscisse_souris() // largeur_carreau

            list_valide = tuiles_possibles(list_image,num_col,num_lig)

            # Si il y a au moins une case valide, affiche tous les tuiles possibles
            if list_valide != []:
                liste_num_affichage = [[(y, x) for x in range(nbr_carreau)] for y in range(nbr_carreau)]
                afficher_tuiles(liste_num_affichage, list_valide, largeur_carreau, hauteur_carreau, nbr_carreau)
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
            y_sup = fltk.ordonnee_souris() // hauteur_carreau
            x_sup = fltk.abscisse_souris() // largeur_carreau
            fltk.efface('image' + str(x_sup) + str(y_sup))
            list_image[y_sup][x_sup] = None

    if tev == "Touche":
        touche_ev = fltk.touche(ev)
        print(touche_ev)


        if touche_ev == "Up":
            if coord[0]==0:
                grille_dec.insert(0,[None for x in range(len(list_image[-1]))])
                grille_riv.insert(0,[None for x in range(len(list_image[-1]))])
                list_image.insert(0,[None for x in range(len(list_image[-1]))])
                
            else:
                coord=(coord[0]-1,coord[1])
                

        if touche_ev == "Down":
            if coord[0]+nbr_carreau==len(list_image):
                grille_dec.append([None for x in range(len(list_image[-1]))])
                grille_riv.append([None for x in range(len(list_image[-1]))])
                list_image.append([None for x in range(len(list_image[0]))])
            coord=(coord[0]+1,coord[1])
                


        if touche_ev == "Left":
            if coord[1]==0:
                for x in range(len(list_image)):
                    grille_dec[x].insert(0,None)
                    grille_riv[x].insert(0,None)
                    list_image[x].insert(0,None)
            else:
                coord=(coord[0],coord[1]-1)

        if touche_ev == "Right":
            if coord[1]+nbr_carreau==len(list_image[0]):
                for x in range(len(list_image)):
                    grille_dec[x].append(None)
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
                        print("carte complétée")
                        afficher_carte(nbr_carreau, hauteur_fenetre, largeur_fenetre, hauteur_carreau, largeur_carreau,coord)
                    else:
                        print("impossible de compléter la carte")
                        fltk.texte(largeur_fenetre // 2, hauteur_fenetre - 20, "carte impossible à compléter", taille=16, couleur='red', ancrage='center')
            else:
                afficher_carte(nbr_carreau, hauteur_fenetre, largeur_fenetre, hauteur_carreau, largeur_carreau,coord)


        if touche_ev == "l":
            num_col = fltk.ordonnee_souris() // hauteur_carreau
            num_lig = fltk.abscisse_souris() // largeur_carreau
            print(list_image[num_col][num_lig])

        elif touche_ev == "s":
            print("solveur lancé")
            dictionr = {}
            for n in range(len(list_image)):
                for m in range(len(list_image[n])):
                    dictionr[str(m)+','+str(n)]=0
            if solveur2(list_image,dictionr, coord):
                print("carte complétée")
                afficher_carte(nbr_carreau, hauteur_fenetre, largeur_fenetre, hauteur_carreau, largeur_carreau,coord)
            else:
                print("impossible de compléter la carte")
                fltk.texte(largeur_fenetre // 2, hauteur_fenetre - 20, "carte impossible à compléter", taille=16, couleur='red', ancrage='center')

        elif touche_ev=='r':
            for tab in grille_riv:
                print(tab)

        elif touche_ev=='m':
            #Efface Tout
            list_image = [[None for x in range(nbr_carreau)] for y in range(nbr_carreau)]
            afficher_carte(nbr_carreau, hauteur_fenetre, largeur_fenetre, hauteur_carreau, largeur_carreau)

        elif touche_ev=="d":
            decor(nbr_carreau, hauteur_fenetre, largeur_fenetre, hauteur_carreau, largeur_carreau,list_image)

    if tev == "Quitte":
        print("Fin de partie")
        fltk.ferme_fenetre()
        break

    fltk.mise_a_jour()
