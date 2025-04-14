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




for x in range(1,nbr_carreau):
    fltk.ligne((x)*larg_carreau,longueur,x*larg_carreau,0,couleur="red")
    fltk.ligne(largeur,(x)*long_carreau,0,x*long_carreau)
fltk.image(0 , 0 , "megatuile/MegaMMMM.png", long_carreau, larg_carreau, ancrage='nw')

list_image=[['Vide' for x in range(nbr_carreau)] for y in range(nbr_carreau)]

while True:
    ev = fltk.donne_ev()
    tev = fltk.type_ev(ev)
    

    if tev == "ClicGauche":
        num_col=fltk.ordonnee_souris()//long_carreau
        num_lig=fltk.abscisse_souris()//larg_carreau
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

        print('haut',haut,'droite',droite,'bas',bas,'gauche',gauche)

        list_valide=[]
        for tuile in liste_tuiles:
            if (tuile[3]==gauche or gauche=='0') and (tuile[1]==droite or droite=='0') and (tuile[0]==haut or haut=='0') and (tuile[2]==bas or bas=='0'):
                list_valide.append(tuile)
        print(list_valide)
        if list_valide !=[]:
            case=random.choice(list_valide)
            list_image[num_col][num_lig]=case
            fltk.image(num_lig*larg_carreau , num_col*long_carreau , "tuiles/"+case, long_carreau, larg_carreau, ancrage='nw', tag='image'+str(num_lig)+str(num_col))
        print(case)
        



    if tev == "ClicDroit":
        num_col=fltk.ordonnee_souris()//long_carreau
        num_lig=fltk.abscisse_souris()//larg_carreau
        fltk.efface('image'+str(num_lig)+str(num_col))
        list_image[num_col][num_lig]='Vide'


    if tev == "Touche":
        touche_ev = fltk.touche(ev)
        
        if touche_ev == "l":
            num_col=fltk.ordonnee_souris()//long_carreau
            num_lig=fltk.abscisse_souris()//larg_carreau
            print(fltk.objet_survole())
            print(list_image[num_col][num_lig])

    if tev == "Quitte":

        print("Fin de partie")
        fltk.ferme_fenetre()
        break
    
    fltk.mise_a_jour()