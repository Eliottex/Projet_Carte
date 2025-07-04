import subprocess
import sys
import tkinter as tk
from collections import deque
from functools import wraps
from os import system
import os
from pathlib import Path
from time import sleep, time
from tkinter import PhotoImage
from tkinter.font import Font
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Deque,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    TypeVar,
    Union,
)


try:
    # noinspection PyUnresolvedReferences
    from PIL import Image, ImageTk

    print("Bibliothèque PIL chargée.", file=sys.stderr)
    PIL_AVAILABLE = True
except ImportError as e:
    PIL_AVAILABLE = False

if TYPE_CHECKING:
    from typing_extensions import Literal

    Anchor = Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"]
    TkEvent = tk.Event[tk.BaseWidget]
else:
    Anchor = str
    TkEvent = tk.Event
FltkEvent = Tuple[str, Optional[TkEvent]]


__all__ = [
    # gestion de fenêtre
    "cree_fenetre",
    "ferme_fenetre",
    "redimensionne_fenetre",
    "mise_a_jour",
    # dessiner
    "arc",
    "cercle",
    "fleche",
    "image",
    "ligne",
    "ovale",
    "point",
    "polygone",
    "rectangle",
    "taille_texte",
    "texte",
    # modif et info objets
    "efface_tout",
    "efface",
    "modifie",
    "deplace",
    "couleur",
    "remplissage",
    "type_objet",
    # utilitaires
    "attente",
    "capture_ecran",
    "touche_pressee",
    "repere",
    # événements
    "donne_ev",
    "attend_ev",
    "attend_clic_gauche",
    "attend_fermeture",
    "type_ev",
    "abscisse",
    "ordonnee",
    "touche",
    # info fenetre
    "abscisse_souris",
    "ordonnee_souris",
    "hauteur_fenetre",
    "largeur_fenetre",
    "objet_survole",
]

class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground


class CustomCanvas:
    """
    Classe qui encapsule tous les objets tkinter nécessaires à la création
    d'un canevas.
    """

    _on_osx = sys.platform.startswith("darwin")

    _ev_mapping = {
        "ClicGauche": "<Button-1>",
        "ClicMilieu": "<Button-2>",
        "ClicDroit": "<Button-2>" if _on_osx else "<Button-3>",
        "Deplacement": "<Motion>",
        "Touche": "<Key>",
        "Redimension": "<Configure>",
        "Scroll" : "<MouseWheel>",
        "Up" : "<Button-4>",
        "Down" : "<Button-5>",
    }

    _default_ev = ["ClicGauche", "ClicDroit", "Touche","Scroll","Up","Down"]

    def __init__(
            self,
            width: int,
            height: int,
            refresh_rate: int = 100,
            events: Optional[List[str]] = None,
            resizing: bool = False
    ) -> None:
        # width and height of the canvas
        self.width = width
        self.height = height
        self.interval = 1 / refresh_rate

        # root Tk object
        self.root = tk.Tk()

        # canvas attached to the root object
        self.canvas = tk.Canvas(
            self.root, width=width, height=height, highlightthickness=0
        )

        # adding the canvas to the root window and giving it focus
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.root.resizable(width=resizing, height=resizing)
        self.canvas.focus_set()
        self.first_resize = True

        # binding events
        self.ev_queue: Deque[FltkEvent] = deque()
        self.pressed_keys: Set[str] = set()
        self.events = CustomCanvas._default_ev if events is None else events
        self.bind_events()

        # update for the first time
        self.last_update = time()
        self.root.update()

        if CustomCanvas._on_osx:
            system(
                """/usr/bin/osascript -e 'tell app "Finder" \
                   to set frontmost of process "Python" to true' """
            )

    def update(self) -> None:
        t = time()
        self.root.update()
        sleep(max(0.0, self.interval - (t - self.last_update)))
        self.last_update = time()

    def Button(self,parent,texte,commande,xa,ya,couleur,hi_couleur,brdw=1,actfg="grey",hlcolor="green",hl_bg="red",f=('Helvetica','20')):
        btn = HoverButton(parent,font=f,activeforeground=actfg,borderwidth=brdw,highlightcolor=hlcolor,highlightbackground=hl_bg,background=couleur,activebackground=hi_couleur,text=texte,command=commande,anchor="center",fg="white")
        btn.place(relx=xa,rely=ya,anchor="center")

    def Entry(self,parent):
        self.entry = tk.Entry(parent,font=('Helvetica','20'))
        self.entry.place(relx=0.5,rely=0.5,anchor="center")

    def Return_entry(self):
        abc = self.entry.get()
        return abc

    def resize(self, width: int, height: int) -> None:
        self.root.geometry(f"{int(width)}x{int(height)}")

    def bind_events(self) -> None:
        self.root.protocol("WM_DELETE_WINDOW", self.event_quit)
        self.canvas.bind("<Configure>", self.event_resize)
        self.canvas.bind("<KeyPress>", self.register_key)
        self.canvas.bind("<KeyRelease>", self.release_key)
        for name in self.events:
            self.bind_event(name)

    # noinspection PyUnresolvedReferences
    def register_key(self, ev: TkEvent) -> None:
        self.pressed_keys.add(ev.keysym)

    # noinspection PyUnresolvedReferences
    def release_key(self, ev: TkEvent) -> None:
        if ev.keysym in self.pressed_keys:
            self.pressed_keys.remove(ev.keysym)

    def event_quit(self) -> None:
        self.ev_queue.append(("Quitte", None))

    # noinspection PyUnresolvedReferences
    def event_resize(self, event: TkEvent) -> None:
        if event.widget.widgetName == "canvas":
            if self.width != event.width or self.height != event.height:
                self.width, self.height = event.width, event.height
                if not self.ev_queue or self.ev_queue[-1][0] != "Redimension":
                    self.ev_queue.append(("Redimension", event))

    def bind_event(self, name: str) -> None:
        e_type = CustomCanvas._ev_mapping.get(name, name)

        def handler(event: TkEvent, _name: str = name) -> None:
            self.ev_queue.append((_name, event))

        self.canvas.bind(e_type, handler, "+")

    def unbind_event(self, name: str) -> None:
        e_type = CustomCanvas._ev_mapping.get(name, name)
        self.canvas.unbind(e_type)


__canevas: Optional[CustomCanvas] = None
__img: Dict[Tuple[Path, int, int], PhotoImage] = {}

__trans_object_type = {
    "arc": "arc",
    "image": "image",
    "line": "ligne",
    "oval": "ovale",
    "polygon": "polygone",
    "rectangle": "rectangle",
    "text": "texte",
}

__trans_options = {
    "remplissage": "fill",
    "couleur": "outline",
    "epaisseur": "width",
}


#############################################################################
# Exceptions
#############################################################################


class TypeEvenementNonValide(Exception):
    pass


class FenetreNonCree(Exception):
    pass


class FenetreDejaCree(Exception):
    pass


Ret = TypeVar("Ret")


def _fenetre_creee(func: Callable[..., Ret]) -> Callable[..., Ret]:
    @wraps(func)
    def new_func(*args: Any, **kwargs: Any) -> Ret:
        if __canevas is None:
            raise FenetreNonCree(
                'La fenêtre n\'a pas été crée avec la fonction "cree_fenetre".'
            )
        return func(*args, **kwargs)

    return new_func


#############################################################################
# Initialisation, mise à jour et fermeture
#############################################################################


def cree_fenetre(
        largeur: int, hauteur: int, frequence: int = 100,
        redimension: bool = False, affiche_repere : bool = False
) -> None:
    """
    Crée une fenêtre de dimensions ``largeur`` x ``hauteur`` pixels.
    :rtype:
    """
    global __canevas
    if __canevas is not None:
        raise FenetreDejaCree(
            'La fenêtre a déjà été crée avec la fonction "cree_fenetre".'
        )
    __canevas = CustomCanvas(largeur, hauteur, frequence, resizing=redimension)
    if affiche_repere:
        repere()


@_fenetre_creee
def ferme_fenetre() -> None:
    """
    Détruit la fenêtre.
    """
    global __canevas
    assert __canevas is not None
    __canevas.root.destroy()
    __canevas = None


@_fenetre_creee
def redimensionne_fenetre(largeur: int, hauteur: int) -> None:
    """
    Fixe les dimensions de la fenêtre à (``hauteur`` x ``largeur``) pixels.

    Le contenu du canevas n'est pas automatiquement mis à l'échelle et doit
    être redessiné si nécessaire.
    """
    assert __canevas is not None
    __canevas.resize(width=largeur, height=hauteur)


@_fenetre_creee
def mise_a_jour() -> None:
    """
    Met à jour la fenêtre. Les dessins ne sont affichés qu'après
    l'appel à  cette fonction.
    """
    assert __canevas is not None
    __canevas.update()


#############################################################################
# Fonctions de dessin
#############################################################################


# Formes géométriques
@_fenetre_creee
def bouton(texte,commande,x,y,couleur,hi_couleur,brdw=1) -> int:
    """
        Dessin un bouton clicable du point ``(ax, ay)`` au point ``(bx, by)``.

        :param float ax: abscisse du premier point
        :param float ay: ordonnée du premier point
        :param float bx: abscisse du second point
        :param float by: ordonnée du second point
        :param str couleur: couleur de trait (défaut 'black')
        :param float epaisseur: épaisseur de trait en pixels (défaut 1)
        :param str tag: étiquette d'objet (défaut : pas d'étiquette)
        :return: identificateur d'objet
        """
    assert __canevas is not None
    return __canevas.Button(__canevas.canvas,texte, commande,x,y,couleur,hi_couleur,brdw)

@_fenetre_creee
def entree() :
    assert __canevas is not None
    return __canevas.Entry(__canevas.canvas)
  
def renvoie_entree():
    assert __canevas is not None
    return __canevas.Return_entry()


@_fenetre_creee
def ligne(
        ax: float,
        ay: float,
        bx: float,
        by: float,
        couleur: str = "black",
        epaisseur: float = 1,
        tag: str = "",
) -> int:
    """
    Trace un segment reliant le point ``(ax, ay)`` au point ``(bx, by)``.

    :param float ax: abscisse du premier point
    :param float ay: ordonnée du premier point
    :param float bx: abscisse du second point
    :param float by: ordonnée du second point
    :param str couleur: couleur de trait (défaut 'black')
    :param float epaisseur: épaisseur de trait en pixels (défaut 1)
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    assert __canevas is not None
    return __canevas.canvas.create_line(
        ax, ay, bx, by, fill=couleur, width=epaisseur, tags=tag
    )


@_fenetre_creee
def fleche(
        ax: float,
        ay: float,
        bx: float,
        by: float,
        couleur: str = "black",
        epaisseur: float = 1,
        tag: str = "",
) -> int:
    """
    Trace une flèche du point ``(ax, ay)`` au point ``(bx, by)``.

    :param float ax: abscisse du premier point
    :param float ay: ordonnée du premier point
    :param float bx: abscisse du second point
    :param float by: ordonnée du second point
    :param str couleur: couleur de trait (défaut 'black')
    :param float epaisseur: épaisseur de trait en pixels (défaut 1)
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    x, y = (bx - ax, by - ay)
    n = (x ** 2 + y ** 2) ** 0.5
    x, y = x / n, y / n
    points = [
        bx,
        by,
        bx - x * 5 - 2 * y,
        by - 5 * y + 2 * x,
        bx - x * 5 + 2 * y,
        by - 5 * y - 2 * x,
    ]
    assert __canevas is not None
    return __canevas.canvas.create_polygon(
        points, fill=couleur, outline=couleur, width=epaisseur, tags=tag
    )


@_fenetre_creee
def polygone(
        points: List[float],
        couleur: str = "black",
        remplissage: str = "",
        epaisseur: float = 1,
        tag: str = "",
) -> int:
    """
    Trace un polygone dont la liste de points est fournie.

    :param list points: liste de couples (abscisse, ordonnee) de points
    :param str couleur: couleur de trait (défaut 'black')
    :param str remplissage: couleur de fond (défaut transparent)
    :param float epaisseur: épaisseur de trait en pixels (défaut 1)
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    assert __canevas is not None
    if epaisseur == 0:
        couleur = ""
    return __canevas.canvas.create_polygon(
        points, fill=remplissage, outline=couleur, width=epaisseur, tags=tag
    )


@_fenetre_creee
def rectangle(
        ax: float,
        ay: float,
        bx: float,
        by: float,
        couleur: str = "black",
        remplissage: str = "",
        epaisseur: float = 1,
        tag: str = "",
) -> int:
    """
    Trace un rectangle noir ayant les point ``(ax, ay)`` et ``(bx, by)``
    comme coins opposés.

    :param float ax: abscisse du premier coin
    :param float ay: ordonnée du premier coin
    :param float bx: abscisse du second coin
    :param float by: ordonnée du second coin
    :param str couleur: couleur de trait (défaut 'black')
    :param str remplissage: couleur de fond (défaut transparent)
    :param float epaisseur: épaisseur de trait en pixels (défaut 1)
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    assert __canevas is not None
    return __canevas.canvas.create_rectangle(
        ax, ay, bx, by,
        outline=couleur, fill=remplissage, width=epaisseur, tags=tag
    )


@_fenetre_creee
def cercle(
        x: float,
        y: float,
        r: float,
        couleur: str = "black",
        remplissage: str = "",
        epaisseur: float = 1,
        tag: str = "",
) -> int:
    """
    Trace un cercle de centre ``(x, y)`` et de rayon ``r`` en noir.

    :param float x: abscisse du centre
    :param float y: ordonnée du centre
    :param float r: rayon
    :param str couleur: couleur de trait (défaut 'black')
    :param str remplissage: couleur de fond (défaut transparent)
    :param float epaisseur: épaisseur de trait en pixels (défaut 1)
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    assert __canevas is not None
    return __canevas.canvas.create_oval(
        x - r,
        y - r,
        x + r,
        y + r,
        outline=couleur,
        fill=remplissage,
        width=epaisseur,
        tags=tag,
    )


@_fenetre_creee
def ovale(
        ax: float,
        ay: float,
        bx : float,
        by : float,
        couleur: str = "black",
        remplissage: str = "",
        epaisseur: float = 1,
        tag: str = "",
) -> int:
    """
    Trace un ovale compris dans le rectangle de coins ``(ax, ay)`` et ``(bx, by)``.

    :param float ax: abscisse du premier coin
    :param float ay: ordonnée du premier coin
    :param float bx: abscisse du second coin
    :param float by: ordonnée du second coin
    :param str couleur: couleur de trait (défaut 'black')
    :param str remplissage: couleur de fond (défaut transparent)
    :param float epaisseur: épaisseur de trait en pixels (défaut 1)
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    assert __canevas is not None
    return __canevas.canvas.create_oval(
        ax, ay, bx, by,
        outline=couleur,
        fill=remplissage,
        width=epaisseur,
        tags=tag,
    )


@_fenetre_creee
def arc(
        x: float,
        y: float,
        r: float,
        ouverture: float = 90,
        depart: float = 0,
        couleur: str = "black",
        remplissage: str = "",
        epaisseur: float = 1,
        tag: str = "",
) -> int:
    """
    Trace un arc de cercle de centre ``(x, y)``, de rayon ``r`` et
    d'angle d'ouverture ``ouverture`` (défaut : 90 degrés, dans le sens
    contraire des aiguilles d'une montre) depuis l'angle initial ``depart``
    (défaut : direction 'est').

    :param float x: abscisse du centre
    :param float y: ordonnée du centre
    :param float r: rayon
    :param float ouverture: abscisse du centre
    :param float depart: ordonnée du centre
    :param str couleur: couleur de trait (défaut 'black')
    :param str remplissage: couleur de fond (défaut transparent)
    :param float epaisseur: épaisseur de trait en pixels (défaut 1)
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    assert __canevas is not None
    return __canevas.canvas.create_arc(
        x - r,
        y - r,
        x + r,
        y + r,
        extent=ouverture,
        start=depart,
        style=tk.ARC,
        outline=couleur,
        fill=remplissage,
        width=epaisseur,
        tags=tag,
    )


@_fenetre_creee
def point(
        x: float, y: float,
        couleur: str = "black", epaisseur: float = 1,
        tag: str = ""
) -> int:
    """
    Trace un point aux coordonnées ``(x, y)`` en noir.

    :param float x: abscisse
    :param float y: ordonnée
    :param str couleur: couleur du point (défaut 'black')
    :param float epaisseur: épaisseur de trait en pixels (défaut 1)
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    assert __canevas is not None
    return cercle(x, y, epaisseur,
                  couleur=couleur, remplissage=couleur, tag=tag)


# Image


@_fenetre_creee
def image(
        x: float,
        y: float,
        fichier: str,
        largeur: Optional[int] = None,
        hauteur: Optional[int] = None,
        ancrage: Anchor = "center",
        tag: str = "",
) -> int:
    """
    Affiche l'image contenue dans ``fichier`` avec ``(x, y)`` comme centre. Les
    valeurs possibles du point d'ancrage sont ``'center'``, ``'nw'``,
    etc. Les arguments optionnels ``largeur`` et ``hauteur`` permettent de
    spécifier des dimensions maximales pour l'image (sans changement de
    proportions).

    :param float x: abscisse du point d'ancrage
    :param float y: ordonnée du point d'ancrage
    :param str fichier: nom du fichier contenant l'image
    :param largeur: largeur de l'image
    :param hauteur: hauteur de l'image
    :param ancrage: position du point d'ancrage par rapport à l'image
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    assert __canevas is not None
    if PIL_AVAILABLE:
        tk_image = _load_pil_image(fichier, hauteur, largeur)
    else:
        tk_image = _load_tk_image(fichier, hauteur, largeur)
    img_object = __canevas.canvas.create_image(
        x, y, anchor=ancrage, image=tk_image, tags=tag
    )
    return img_object


def _load_tk_image(fichier: str,
                   hauteur: Optional[int] = None,
                   largeur: Optional[int] = None) -> PhotoImage:
    chemin = Path(fichier)
    ph_image = PhotoImage(file=fichier)
    largeur_o = ph_image.width()
    hauteur_o = ph_image.height()
    if largeur is None:
        largeur = largeur_o
    if hauteur is None:
        hauteur = hauteur_o
    zoom_l = max(1, largeur // largeur_o)
    zoom_h = max(1, hauteur // hauteur_o)
    red_l = max(1, largeur_o // largeur)
    red_h = max(1, hauteur_o // hauteur)
    largeur = largeur_o * zoom_l // red_l
    hauteur = hauteur_o * zoom_h // red_h
    if (chemin, largeur, hauteur) in __img:
        return __img[(chemin, largeur, hauteur)]
    ph_image = ph_image.zoom(zoom_l, zoom_h)
    ph_image = ph_image.subsample(red_l, red_h)
    __img[(chemin, largeur, hauteur)] = ph_image
    return ph_image


def _load_pil_image(fichier: str,
                    hauteur: Optional[int] = None,
                    largeur: Optional[int] = None) -> PhotoImage:
    chemin = Path(fichier)
    img = Image.open(fichier)
    if largeur is None:
        largeur = img.width
    if hauteur is None:
        hauteur = img.height
    if (chemin, largeur, hauteur) in __img:
        return __img[(chemin, largeur, hauteur)]
    img = img.resize((largeur, hauteur))
    ph_image = ImageTk.PhotoImage(img)
    __img[(chemin, largeur, hauteur)] = ph_image  # type:ignore
    return ph_image  # type:ignore


# Texte


@_fenetre_creee
def texte(
        x: float,
        y: float,
        chaine: str,
        couleur: str = "black",
        remplissage: str = "black",
        ancrage: Anchor = "nw",
        police: str = "Helvetica",
        taille: int = 24,
        tag: str = "",
) -> int:
    """
    Affiche la chaîne ``chaine`` avec ``(x, y)`` comme point d'ancrage (par
    défaut le coin supérieur gauche).

    :param float x: abscisse du point d'ancrage
    :param float y: ordonnée du point d'ancrage
    :param str chaine: texte à afficher
    :param str couleur: couleur de texte (défaut 'black')
    :param str remplissage: synonyme de `couleur` (défaut 'black')
    :param ancrage: position du point d'ancrage (défaut 'nw')
    :param police: police de caractères (défaut : `Helvetica`)
    :param taille: taille de police (défaut 24)
    :param tag: étiquette d'objet (défaut : pas d'étiquette
    :return: identificateur d'objet
    """
    assert __canevas is not None
    if remplissage and not couleur:
        couleur = remplissage
    return __canevas.canvas.create_text(
        x, y,
        text=chaine, font=(police, taille),
        tags=tag, fill=couleur, anchor=ancrage
    )


def taille_texte(
        chaine: str, police: str = "Helvetica", taille: int = 24
) -> Tuple[int, int]:
    """
    Donne la largeur et la hauteur en pixel nécessaires pour afficher
    ``chaine`` dans la police et la taille données.

    :param str chaine: chaîne à mesurer
    :param police: police de caractères (défaut : `Helvetica`)
    :param taille: taille de police (défaut 24)
    :return: couple (w, h) constitué de la largeur et la hauteur de la chaîne
        en pixels (int), dans la police et la taille données.
    """
    font = Font(family=police, size=taille)
    return font.measure(chaine), font.metrics("linespace")


#############################################################################
# Utilitaires sur les objets
#############################################################################


@_fenetre_creee
def efface_tout() -> None:
    """
    Efface la fenêtre.
    """
    assert __canevas is not None
    __canevas.canvas.delete("all")


@_fenetre_creee
def efface(objet_ou_tag: Union[int, str]) -> None:
    """
    Efface ``objet`` de la fenêtre.

    :param: objet ou étiquette d'objet à supprimer
    :type: ``int`` ou ``str``
    """
    assert __canevas is not None
    __canevas.canvas.delete(objet_ou_tag)


@_fenetre_creee
def type_objet(objet: int) -> Optional[str]:
    assert __canevas is not None
    tobj: Optional[str] = __canevas.canvas.type(objet)  # type: ignore
    if tobj is None:
        return None
    if tobj == "oval":
        ax, ay, bx, by = __canevas.canvas.coords(objet)
        return "cercle" if bx - ax == by - ay else None
    return __trans_object_type.get(tobj, None)


@_fenetre_creee
def modifie(objet_ou_tag: Union[int, str], **options: Dict[str, str]) -> None:
    assert __canevas is not None
    if (type_objet(objet_ou_tag) == "texte"
            and "couleur" in options
            and "remplissage" not in options):
        options["remplissage"] = options["couleur"]
        del options["couleur"]
    temp = {}
    for option, valeur in options.items():
        if option in __trans_options:
            temp[__trans_options[option]] = valeur
    __canevas.canvas.itemconfigure(objet_ou_tag, **temp)


@_fenetre_creee
def deplace(objet_ou_tag: Union[int, str],
            distance_x: Union[int, float],
            distance_y: Union[int, float]) -> None:
    assert __canevas is not None
    __canevas.canvas.move(objet_ou_tag, distance_x, distance_y)


@_fenetre_creee
def couleur(objet: int) -> Optional[str]:
    assert __canevas is not None
    if type_objet(objet) == 'texte':
        option = "fill"
    else:
        option = "outline"
    return __canevas.canvas.itemcget(objet, option=option)  # type: ignore


@_fenetre_creee
def remplissage(objet: int) -> Optional[str]:
    assert __canevas is not None
    return __canevas.canvas.itemcget(objet, option="fill")  # type: ignore


#############################################################################
# Utilitaires
#############################################################################


def attente(temps: float) -> None:
    start = time()
    while time() - start < temps:
        mise_a_jour()


@_fenetre_creee
def capture_ecran(file: str) -> None:
    """
    Fait une capture d'écran sauvegardée dans ``file.png``.
    """
    assert __canevas is not None
    
    # Capture canvas as .ps file
    __canevas.canvas.postscript(  # type: ignore
        file=file + ".ps",
        height=__canevas.height,
        width=__canevas.width,
        colormode="color",
    )

    # Convert .ps to .png using ImageMagick's convert command
    subprocess.call([
    "C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe",
    "-density", "150",
    file + ".ps",
    "-background", "white",
    "-flatten",
    "-geometry", "100%",
    file + ".png"
],shell=True)

    #psimage=Image.open(file+'.ps')
    #psimage.save(file+'.png')
    # Remove the .ps file (cross-platform)
    try:
        os.remove(file + ".ps")
        print(f"Successfully removed {file}.ps")
    except Exception as e:
        print(f"Error removing {file}.ps: {e}")


@_fenetre_creee
def touche_pressee(keysym: str) -> bool:
    """
    Renvoie `True` si ``keysym`` est actuellement pressée.

    Cette fonction est utile pour la gestion des touches de déplacement dans un jeu
    car elle permet une animation mieux maîtrisée, en évitant le phénomène de répétition
    de touche lié au système d'exploitation.

    :param keysym: symbole associé à la touche à tester.
    :return: `True` si ``keysym`` est actuellement pressée, `False` sinon.
    """
    assert __canevas is not None
    return keysym in __canevas.pressed_keys


@_fenetre_creee
def repere(grad: int = 50,
           sous_grad : Union[int, None] = 10,
           valeurs: bool = True,
           couleur_grad: str = "#a0a0a0",
           couleur_sous_grad: str = "#bbbbbb") -> None:
    """affiche une grille sur la fenêtre.
    :param grad: distance en pixels entre deux graduations majeures
    :param sous_grad: distance en pixels entre deux graduations mineures, ou None
    :param valeurs: True (defaut) pour affichage des valeurs, False sinon
    :param couleur_grad: couleur des graduations majeures et du texte
    :param couleur_sous_grad: couleur des graduations mineures
    """
    assert __canevas is not None
    offset = 2
    __canevas.canvas.create_text(offset, offset, text="0", fill=couleur_grad,
                                 tags='repere', anchor='nw', font=('Helvetica', 8))
    pas = grad if sous_grad is None else sous_grad
    xy = pas
    xmax = __canevas.width
    ymax = __canevas.height
    while xy < max(xmax, ymax) :
        if xy % grad == 0:
            couleur = couleur_grad
            dash : Union[str, int] = ""
            if valeurs:
                __canevas.canvas.create_text(xy + offset, 0, text=xy, fill=couleur,
                                 tags='repere', anchor='nw', font=('Helvetica', 8))
                __canevas.canvas.create_text(0, xy + offset, text=xy, fill=couleur,
                                 tags='repere', anchor='nw', font=('Helvetica', 8))
        else:
            couleur = couleur_sous_grad
            dash = 2
        __canevas.canvas.create_line(xy, 0, xy, ymax, fill=couleur, dash=dash, tags='repere')
        __canevas.canvas.create_line(0, xy, xmax, xy, fill=couleur, dash=dash, tags='repere')
        xy += pas


#############################################################################
# Gestions des évènements
#############################################################################


@_fenetre_creee
def donne_ev() -> Optional[FltkEvent]:
    """
    Renvoie immédiatement l'événement en attente le plus ancien,
    ou ``None`` si aucun événement n'est en attente.
    """
    assert __canevas is not None
    if not __canevas.ev_queue:
        return None
    return __canevas.ev_queue.popleft()


def attend_ev() -> FltkEvent:
    """Attend qu'un événement ait lieu et renvoie le premier événement qui
    se produit."""
    while True:
        ev = donne_ev()
        if ev is not None:
            return ev
        mise_a_jour()


def attend_clic_gauche() -> Tuple[int, int]:
    """Attend qu'un clic gauche sur la fenêtre ait lieu et renvoie ses
    coordonnées. **Attention**, cette fonction empêche la détection d'autres
    événements ou la fermeture de la fenêtre."""
    while True:
        ev = donne_ev()
        if ev is not None and type_ev(ev) == "ClicGauche":
            x, y = abscisse(ev), ordonnee(ev)
            assert isinstance(x, int) and isinstance(y, int)
            return x, y
        mise_a_jour()


def attend_fermeture() -> None:
    """Attend la fermeture de la fenêtre. Cette fonction renvoie None.
    **Attention**, cette fonction empêche la détection d'autres événements."""
    while True:
        ev = donne_ev()
        if ev is not None and type_ev(ev) == "Quitte":
            ferme_fenetre()
            return
        mise_a_jour()


def type_ev(ev: Optional[FltkEvent]) -> Optional[str]:
    """
    Renvoie une chaîne donnant le type de ``ev``. Les types
    possibles sont 'ClicDroit', 'ClicGauche', 'Touche' et 'Quitte'.
    Renvoie ``None`` si ``evenement`` vaut ``None``.
    """
    return ev if ev is None else ev[0]


def abscisse(ev: Optional[FltkEvent]) -> Optional[int]:
    """
    Renvoie la coordonnée x associé à ``ev`` si elle existe, None sinon.
    """
    x = attribut(ev, "x")
    assert isinstance(x, int) or x is None
    return x


def ordonnee(ev: Optional[FltkEvent]) -> Optional[int]:
    """
    Renvoie la coordonnée y associé à ``ev`` si elle existe, None sinon.
    """
    y = attribut(ev, "y")
    assert isinstance(y, int) or y is None
    return y


def touche(ev: Optional[FltkEvent]) -> str:
    """
    Renvoie une chaîne correspondant à la touche associé à ``ev``,
    si elle existe.
    """
    keysym = attribut(ev, "keysym")
    assert isinstance(keysym, str)
    return keysym


def attribut(ev: Optional[FltkEvent], nom: str) -> Any:
    if ev is None:
        raise TypeEvenementNonValide(
            f"Accès à l'attribut {nom} impossible sur un événement vide"
        )
    tev, evtk = ev
    if not hasattr(evtk, nom):
        raise TypeEvenementNonValide(
            f"Accès à l'attribut {nom} impossible "
            f"sur un événement de type {tev}"
        )
    attr = getattr(evtk, nom)
    return attr if attr != "??" else None


#############################################################################
# Informations sur la fenêtre
#############################################################################


@_fenetre_creee
def abscisse_souris() -> int:
    assert __canevas is not None
    return __canevas.canvas.winfo_pointerx() - __canevas.canvas.winfo_rootx()


@_fenetre_creee
def ordonnee_souris() -> int:
    assert __canevas is not None
    return __canevas.canvas.winfo_pointery() - __canevas.canvas.winfo_rooty()


@_fenetre_creee
def largeur_fenetre() -> int:
    assert __canevas is not None
    return __canevas.width


@_fenetre_creee
def hauteur_fenetre() -> int:
    assert __canevas is not None
    return __canevas.height


@_fenetre_creee
def objet_survole() -> Optional[int]:
    assert __canevas is not None
    x, y = abscisse_souris(), ordonnee_souris()
    overlapping = __canevas.canvas.find_overlapping(x, y, x, y)
    if overlapping:
        return overlapping[0]
    return None
