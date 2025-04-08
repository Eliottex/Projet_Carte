print('Hello World !')
import fltk



longueur=800
largeur=800
fltk.cree_fenetre(largeur,longueur)
nbr_carreau=10
long_carreau=int(longueur/nbr_carreau)
larg_carreau=int(largeur/nbr_carreau)

for x in range(1,nbr_carreau):
    fltk.ligne((x)*larg_carreau,longueur,x*larg_carreau,0,couleur="red")
    fltk.ligne(largeur,(x)*long_carreau,0,x*long_carreau)

while True:
    ev = fltk.donne_ev()
    tev = fltk.type_ev(ev)
    fltk.image(0 , 0 , "megatuile/MegaMMMM.png", long_carreau, larg_carreau, ancrage='nw')



    if tev == "Quitte":

        print("Fin de partie")
        fltk.ferme_fenetre()
        break
    
    fltk.mise_a_jour()