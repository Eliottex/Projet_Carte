print('Hello World !')
import fltk
import os
import random

longueur=800
largeur=800
fltk.cree_fenetre(largeur,longueur)
nbr_carreau=10
long_carreau=int(longueur/nbr_carreau)
larg_carreau=int(largeur/nbr_carreau)


liste_tuiles = os.listdir( 'tuiles/' )

def prepare_lst_tuiles(liste_tuiles_possibles):
     
    longueur=800
    largeur=800
    nbr_carreau=10
    long_carreau=int(longueur/nbr_carreau)
    larg_carreau=int(largeur/nbr_carreau)
    #print('salut')




    fltk.efface_tout()

    num_lig=1
    num_col=0
    tableau_possibles= [[[] for x in range(nbr_carreau+1)] for x in range(len(liste_tuiles_possibles)//nbr_carreau+1)]
    #print(tableau_possibles)
    for x in range(len(liste_tuiles_possibles)):
        #print( num_lig,num_col,len(liste_tuiles_possibles)//nbr_carreau+1,tableau_possibles)
        #fltk.image(num_lig*larg_carreau , num_col*long_carreau , "tuiles/"+liste_tuiles_possibles[x], long_carreau, larg_carreau, ancrage='nw', tag='image'+str(num_lig)+str(num_col))   
        tableau_possibles[num_col][num_lig-1] = liste_tuiles_possibles[x]
        if num_lig%(nbr_carreau+1)==0 and x!=0:
            num_col+=1
            num_lig=1
        else:
            num_lig +=1
    liste_num_affichage=[[(y,x) for x in range(nbr_carreau)] for y in range(nbr_carreau)]
    #print(liste_num_affichage)
    return liste_num_affichage

    #print(tableau_possibles)
    
def afficher_tuiles(liste_num,liste_tuiles,larg_car,long_car,nbr_car):
    fltk.efface_tout()
    #print(liste_tuiles,len(liste_tuiles))
    for x in range(len(liste_num)):
        for y in range(len(liste_num[x])):
            num_ligne = liste_num[x][y][1]
            num_colon = liste_num[x][y][0]
            if 10*num_colon+num_ligne < len(liste_tuiles):
                fltk.image(y*larg_car , x*long_car , "tuiles/"+liste_tuiles[nbr_car*num_colon+num_ligne], long_car, larg_car, ancrage='nw', tag='image'+str(num_ligne)+str(num_colon))   

    quad(nbr_carreau,longueur,largeur,long_carreau,larg_carreau)

def quad(nbr_carreaux,long_fenetre,larg_fenetre,long_car,larg_car):
    for x in range(1,nbr_carreaux):
        fltk.ligne((x)*larg_car,long_fenetre,x*larg_car,0)
        fltk.ligne(larg_fenetre,(x)*long_car,0,x*long_car)

def afficher_carte(nbr_car,long,larg,long_car,larg_car):
    fltk.efface_tout()
    quad(nbr_car,long,larg,long_car,larg_car)
    for x in range(len(list_image)):
        for y in range(len(list_image[x])):
            if list_image[x][y]!='Vide':
                fltk.image(y*larg_car , x*long_car , "tuiles/"+list_image[x][y], long_car, larg_car, ancrage='nw', tag='image'+str(y)+str(x))   





list_image=[['Vide' for x in range(nbr_carreau)] for y in range(nbr_carreau)]
quad(nbr_carreau,longueur,largeur,long_carreau,larg_carreau)

mode='choisir_case'

while True:
    ev = fltk.donne_ev()
    tev = fltk.type_ev(ev)
    if ev!=None :
        print(ev,tev)

    if tev== "Scroll":
        if mode == 'choisir_tuile':
            direction = int(fltk.attribut(ev,"delta")/120)
            #print(liste_num_affichage)
            if liste_num_affichage[0][0][0]!=0 and direction == 1:
                for x in range(len(liste_num_affichage)):
                    for y in range(len(liste_num_affichage[x])):
                        lig = liste_num_affichage[x][y][1]
                        col = liste_num_affichage[x][y][0]
                        liste_num_affichage[x][y]=(col-direction,lig)
                        
            if liste_num_affichage[-1][-1][0]<(len(list_valide)//nbr_carreau) and direction == -1:
                for x in range(len(liste_num_affichage)):
                    for y in range(len(liste_num_affichage[x])):
                        lig = liste_num_affichage[x][y][1]
                        col = liste_num_affichage[x][y][0]
                        liste_num_affichage[x][y]=(col-direction,lig)
            #print(liste_num_affichage)
            afficher_tuiles(liste_num_affichage,list_valide,larg_carreau,long_carreau,nbr_carreau)

    
    if tev == "ClicGauche":
        if mode == 'choisir_case':
            num_col=fltk.ordonnee_souris()//long_carreau
            num_lig=fltk.abscisse_souris()//larg_carreau
            print(num_col,num_lig)
            if num_lig-1 >=0:
                gauche = list_image[num_col][num_lig-1][1] if list_image[num_col][num_lig-1]!='Vide' else '0' 
            else :
                gauche = '0'
            if num_lig+1 <len(list_image[0]):
                droite = list_image[num_col][num_lig+1][3] if list_image[num_col][num_lig+1]!='Vide' else '0' 
            else :
                droite = '0'
            if num_col-1 >=0:
                haut = list_image[num_col-1][num_lig][2] if list_image[num_col-1][num_lig]!='Vide' else '0' 
            else :
                haut = '0'
            if num_col+1 <len(list_image):
                bas = list_image[num_col+1][num_lig][0] if list_image[num_col+1][num_lig]!='Vide' else '0' 
            else :
                bas = '0'

            #print('haut',haut,'droite',droite,'bas',bas,'gauche',gauche)

            list_valide=[]
            for tuile in liste_tuiles:
                if (tuile[3]==gauche or gauche=='0') and (tuile[1]==droite or droite=='0') and (tuile[0]==haut or haut=='0') and (tuile[2]==bas or bas=='0'):
                    list_valide.append(tuile)
            print(list_valide,len(list_valide))
            

            if list_valide!=[]:
                liste_num_affichage = prepare_lst_tuiles(list_valide)
                afficher_tuiles(liste_num_affichage,list_valide,larg_carreau,long_carreau,nbr_carreau)
                mode='choisir_tuile'


        elif mode=='choisir_tuile':
            print(num_col,num_lig)
            x=fltk.ordonnee_souris()//long_carreau
            y=fltk.abscisse_souris()//larg_carreau
            if liste_num_affichage[x][y][1]+nbr_carreau*liste_num_affichage[x][y][0]<len(list_valide):
                case=list_valide[liste_num_affichage[x][y][1]+nbr_carreau*liste_num_affichage[x][y][0]]
                print(liste_num_affichage[x][y][1]+nbr_carreau*liste_num_affichage[x][y][0])
                list_image[num_col][num_lig]=case
                #print(num_lig*larg_carreau , num_col*long_carreau)
                afficher_carte(nbr_carreau,longueur,largeur,long_carreau,larg_carreau)
                mode = 'choisir_case'




    if tev == "ClicDroit":
        if mode == 'choisir_case':
            y_sup=fltk.ordonnee_souris()//long_carreau
            x_sup=fltk.abscisse_souris()//larg_carreau
            #Efface l'image graphiquement
            fltk.efface('image'+str(x_sup)+str(y_sup))
            #Efface la tuile dans la liste
            list_image[y_sup][x_sup]='Vide'


    if tev == "Touche":
        touche_ev = fltk.touche(ev)
        
        if touche_ev == "l":
            num_col=fltk.ordonnee_souris()//long_carreau
            num_lig=fltk.abscisse_souris()//larg_carreau
            #print(fltk.objet_survole())
            #print(list_image[num_col][num_lig])

    if tev == "Quitte":

        print("Fin de partie")
        fltk.ferme_fenetre()
        break
    
    fltk.mise_a_jour()