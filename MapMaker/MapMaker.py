print('Hello World !')
import fltk



longueur=800
largeur=800
fltk.cree_fenetre(longueur,largeur)
nbr_carreau=10
long_carreau=longueur/nbr_carreau
larg_carreau=largeur/nbr_carreau
for x in range(nbr_carreau):
    fltk.ligne(0,(x)*long_carreau,0,(x+1)*long_carreau)
    #fltk.ligne
fltk.mise_a_jour()