print('Hello World !')
import fltk
import os
import random
import time

hauteur=800 
largeur=800
decalage_fenetre=200
fltk.cree_fenetre(largeur,hauteur)
nbr_carreau=10
haut_carreau=int(hauteur/nbr_carreau)
larg_carreau=int(largeur/nbr_carreau)                                                                
decalage_haut=haut_carreau -20
decalage_larg=larg_carreau -20



liste_tuiles = os.listdir( 'tuiles/' )
liste_tuiles = [nom[:-4] for nom in liste_tuiles if nom.endswith('.png') and len(nom[:-4]) == 4]



def afficher_tuiles(liste_num,liste_tuiles,larg_car,haut_car,nbr_car):
    """Affiche les tuiles possibles pour la case cliquée.
    

    """
    
    fltk.efface_tout()
    #print(liste_tuiles,len(liste_tuiles))
    fltk.rectangle(100,100,700,700,"pink","pink")
    fltk.texte(400,70,"choisissez une tuile",'pink','black','center',18)
    for x in range(len(liste_num)):
        for y in range(len(liste_num[x])):
            num_ligne = liste_num[x][y][1]
            num_colon = liste_num[x][y][0]
            
            if 10*num_colon+num_ligne < len(liste_tuiles):
                fltk.image(y*decalage_larg+105 , x*decalage_haut+105, "tuiles/"+liste_tuiles[nbr_car*num_colon+num_ligne],decalage_haut-10, decalage_larg-10, ancrage='nw', tag='image'+str(num_ligne)+str(num_colon))   

    quad(nbr_carreau,hauteur-decalage_fenetre,largeur-decalage_fenetre,decalage_haut,decalage_larg,"pink",100)


def quad(nbr_carreaux,long_fenetre,larg_fenetre,long_car,larg_car,couleur="black",decal=0):
    """Fait un quadrillage.fltk.rectangle(100,100,700,700,"pink","white",epaisseur="5")

    
    """
    
    for x in range(1,nbr_carreaux):
        fltk.ligne((x)*larg_car+decal,long_fenetre+decal,x*larg_car+decal,decal,couleur)
        fltk.ligne(larg_fenetre+decal,(x)*long_car+decal,decal,x*long_car+decal,couleur)



def afficher_carte(nbr_car,long,larg,long_car,larg_car):
    """Affiche la carte actuelle.
    
    
    """
    
    fltk.efface_tout()
    quad(nbr_car,long,larg,long_car,larg_car)
    for x in range(len(list_image)):
        for y in range(len(list_image[x])):
            if list_image[x][y]!=None:
                fltk.image(y*larg_car , x*long_car , "tuiles/"+list_image[x][y] + ".png", long_car, larg_car, ancrage='nw', tag='image'+str(y)+str(x))   




#liste dans laquelle sera retenue l'occupation de chaque case
list_image=[[None for x in range(nbr_carreau)] for y in range(nbr_carreau)]


#création d'un mode permettant d'alterner entre le choix de la case et le choix de la tuile pour la case
mode='choisir_case'

quad(nbr_carreau,hauteur,largeur,haut_carreau,larg_carreau)

"""partie de nesma A PAS TOUCHER"""
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
    list_valide=[]
    for tuile in liste_tuiles:
        if (tuile[3]==gauche or gauche=='0') and (tuile[1]==droite or droite=='0') and (tuile[0]==haut or haut=='0') and (tuile[2]==bas or bas=='0'):
            list_valide.append(tuile)

    return list_valide


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


def solveur2(grille):
    case = case_plus_contrainte(grille)
    if case is None:
        return True  # Tout est rempli

    i, j, tuiles = case
    random.shuffle(tuiles)  # Mélange les tuiles pour que la sélection soit aléatoire

    for tuile in tuiles:
        grille[i][j] = tuile
        fltk.image(j * larg_carreau, i * haut_carreau, "tuiles/" + tuile + ".png", haut_carreau, larg_carreau, ancrage='nw', tag='image'+str(j)+str(i))
        fltk.mise_a_jour()
        time.sleep(0.01)  # Ajoute une petite pause pour visualiser les changements

        if solveur2(grille):
            return True
        grille[i][j] = None
        fltk.efface('image'+str(j)+str(i))
        fltk.mise_a_jour()

    return False


"""fin partie Nesma bisous"""

while True:
    ev = fltk.donne_ev()
    tev = fltk.type_ev(ev)

    if tev== "Scroll" or tev=="Up" or tev=="Down":
        if mode == 'choisir_tuile':
            if tev=="Scroll":
                direction = int(fltk.attribut(ev,"delta")/120)
            elif tev=="Up":
                direction=1
            elif tev=="Down":
                direction=-1
            #scroll vers le haut en déalant les images
            if liste_num_affichage[0][0][0]!=0 and direction == 1:
                for x in range(len(liste_num_affichage)):
                    for y in range(len(liste_num_affichage[x])):
                        lig = liste_num_affichage[x][y][1]
                        col = liste_num_affichage[x][y][0]
                        liste_num_affichage[x][y]=(col-direction,lig)
                        
            #scroll vers le bas en décalant les images            
            if liste_num_affichage[-1][-1][0]<(len(list_valide)//nbr_carreau) and direction == -1:
                for x in range(len(liste_num_affichage)):
                    for y in range(len(liste_num_affichage[x])):
                        lig = liste_num_affichage[x][y][1]
                        col = liste_num_affichage[x][y][0]
                        liste_num_affichage[x][y]=(col-direction,lig)

            #affiche la nouvelle liste d'image (avec décalage du scroll)
            afficher_tuiles(liste_num_affichage,list_valide,larg_carreau,haut_carreau,nbr_carreau)

    
    if tev == "ClicGauche":
        if mode == 'choisir_case':
            #Récupère les coordonnées de la case cliquée
            num_col=fltk.ordonnee_souris()//haut_carreau
            num_lig=fltk.abscisse_souris()//larg_carreau

            #vérifie si il y a une case sur les côtés, si oui elle retiens le raccord nécessaire
            if num_lig-1 >=0:
                gauche = list_image[num_col][num_lig-1][1] if list_image[num_col][num_lig-1]!=None else '0' 
            else :
                gauche = '0'
            if num_lig+1 <len(list_image[0]):
                droite = list_image[num_col][num_lig+1][3] if list_image[num_col][num_lig+1]!=None else '0' 
            else :
                droite = '0'
            if num_col-1 >=0:
                haut = list_image[num_col-1][num_lig][2] if list_image[num_col-1][num_lig]!=None else '0' 
            else :
                haut = '0'
            if num_col+1 <len(list_image):
                bas = list_image[num_col+1][num_lig][0] if list_image[num_col+1][num_lig]!=None else '0' 
            else :
                bas = '0'

            #Recherche l'ensemble des cases qui correspondent aux critères demandés
            list_valide=[]
            for tuile in liste_tuiles:
                if (tuile[3]==gauche or gauche=='0') and (tuile[1]==droite or droite=='0') and (tuile[0]==haut or haut=='0') and (tuile[2]==bas or bas=='0'):
                    list_valide.append(tuile)

            
            #Si il y a au moins une case valide, affiche tous les tuiles possibles à l'aide de la fonction afficher_tuiles
            if list_valide!=[]:
                liste_num_affichage=[[(y,x) for x in range(nbr_carreau)] for y in range(nbr_carreau)]
                afficher_tuiles(liste_num_affichage,list_valide,larg_carreau,haut_carreau,nbr_carreau)
                #Puis modifie le mode pour passer en choix de la tuile
                mode='choisir_tuile'


        elif mode=='choisir_tuile':
            
            #Récupère les coordonées de la tuile cliquée
            x=fltk.ordonnee_souris()//haut_carreau
            y=fltk.abscisse_souris()//larg_carreau

            #Si le clique est bien sur une tuile (et pas une image vide):
            if liste_num_affichage[x][y][1]+nbr_carreau*liste_num_affichage[x][y][0]<len(list_valide):

                #Alors on définit la nouvelle case
                #Ici on utilise x et y qui correspondent à l'emplacement de la tuile choisie
                case=list_valide[liste_num_affichage[x][y][1]+nbr_carreau*liste_num_affichage[x][y][0]]


                #On l'ajoute à la liste                                
                #ici on utilise num_col et num_lig et pas x et y car on a besoin des coordonées de la case cliquée avant et non ceux de la tuile choisie
                list_image[num_col][num_lig]=case    

                #Et on réaffiche toutes les cases avec la liste modifiée juste avant
                afficher_carte(nbr_carreau,hauteur,largeur,haut_carreau,larg_carreau)

                #On rechange le mode pour choisir une nouvelle case
                mode = 'choisir_case'




    if tev == "ClicDroit":
        if mode == 'choisir_case':
            #Récupère les coordonées de la case à supprimer
            y_sup=fltk.ordonnee_souris()//haut_carreau
            x_sup=fltk.abscisse_souris()//larg_carreau
            #Efface l'image graphiquement
            fltk.efface('image'+str(x_sup)+str(y_sup))
            #Efface la tuile dans la liste
            list_image[y_sup][x_sup]=None


    if tev == "Touche":
        touche_ev = fltk.touche(ev)
        
        if touche_ev == "l":
            num_col = fltk.ordonnee_souris() // haut_carreau
            num_lig = fltk.abscisse_souris() // larg_carreau
            print(list_image[num_col][num_lig])

        elif touche_ev == "s":
            print("solveur lancé")
            if solveur2(list_image):
                print("carte complétée")
                afficher_carte(nbr_carreau, hauteur, largeur, haut_carreau, larg_carreau)
            else:
                print("impossible de compléter la carte")
                fltk.texte(largeur//2, hauteur - 20, "carte impossible à compléter", taille=16, couleur='red', ancrage='center')


    if tev == "Quitte":

        print("Fin de partie")
        fltk.ferme_fenetre()
        break
    


    fltk.mise_a_jour()