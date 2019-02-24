#coding: utf-8
"""
    Les actions que vous écrirez prennent en paramètre un modele.
    Les objets manipulés sont :
        - les sommets (visuellement, les cases hexagonales).
             (Les sommets sont des objets 'Hex' mais 
             vous n'avez pas besoin de les manipuler directement,
             seulement de les passer en paramètre.)

        - les flèches
            (même remarque que pour les sommets
            ce sont en fait des entiers qui representent des objets manipulés
            par la bibliothèque graphique Tkinter)

    Les methodes de l'objet modele utilisables sont les suivantes :

    ### METHODES LIEES AU MODELE THEORIQUE #########################

    modele.getListeSommets():
        renvoie la liste des sommets du modele.
        Rq : modele.getListeSommets(True) renvoie la liste de tous les
        sommets même noirs

    modele.getDepart():
        renvoie le sommet de départ

    modele.getObjectif(self):
        renvoie le sommet objectif

    modele.getVoisins(self, sommet):
        renvoie la liste des sommets voisins d'un sommet donné.
        Rq : modele.getVoisins(True) renvoie la liste de tous les
        voisins même noirs

    modele.longueur(sommet1, sommet2):
        renvoie la longueur de l'arete entre ces deux sommets
        configurable en changeant les valeurs dans hexa_modele

    ### METHODES GRAPHIQUES #########################

    modele.addFleche(sommet1, sommet2, couleur):
        ajoute une fleche du sommet 1 au sommet 2, de la couleur donnée,
        et renvoie un indentifiant (un entier) qui permet de la supprimer plus tard
        couleurs : "Black", "Red", etc.

    modele.delFleche(ref):
        supprimer la fleche dont l'identifiant est ref

    modele.addTexte(sommet, texte):
        ajoute un texte sur le sommet donne. Renvoie un identifiant pour
        pouvoir le supprimer.

    modele.deltexte(ref):
        suppprime le texte dont l'identifiant est ref.

"""



from hexa_modele import *
import random
import time
from collections import deque
from random import randint

COLORS = ["Red", "Blue", "Grey", "Green"]

def parcoursEnLargeur(modele, wrong_paths = False, true_path = True):
    """effectue un parcours en largeur du sommet de depart
    affiche les prédécesseurs par des flèches grises et le chemin jusqu'à
    l'objectif en rouge"""
    pred = {}# arrays of predecessors
    begin = modele.getDepart()
    distance = {begin:0}
    fifo = [begin]

    while fifo:# till it's not empty
        current = fifo.pop(0)# take out the first element
        for n in modele.getVoisins(current):
            if n not in distance:
                distance[n] = distance[current] + 1
                pred[n] = current
                fifo.append(n)
                if wrong_paths:
                    modele.addFleche(current, n, "Black")

    if true_path:
        draw_path_start_end(modele, pred)

    return


def draw_path_start_end(modele, pred):
    begin = modele.getDepart()
    v = modele.getObjectif()
    #known = set([])

    #while v != begin and (v not in known) and pred[v]:
    while v != begin:
        in_neighb = pred[v]
        modele.addFleche(in_neighb, v, "Red")
        #known.add(v)
        v = in_neighb

    return

def compConnexes(modele, color = False, text = True):
    """Affiche pour chaque sommet le numéro de la composante auquelle
    il appartient"""
    component = {}# vertex : number of connected component
    number = 0

    for v in modele.getListeSommets():
        if v in component:
            continue
        n = [v]

        while n:
            vertexe = n.pop(0)
            for s in modele.getVoisins(vertexe):
                if s not in component:
                    component[s] = number
                    if color:
                        s.change_couleur(COLORS[number])
                    elif text:
                        modele.addTexte(s, number)
                    n.append(s)


        number += 1

    pass


def parcoursEnProfondeur(modele, wrong_path = True, true_path = True):
    """effectue un parcours en profondeur du sommet de depart
    affiche les prédécesseurs par des flèches grises et le chemin jusqu'à
    l'objectif en rouge
    Affiche le numero prefixe"""
    known = set([])# vertexes that are known
    pred = {}

    for v in modele.getListeSommets():
        if v not in known:
            parcoursEnProfondeurEtape(modele, known, pred, v, wrong_path)

    if true_path:
        draw_path_start_end(modele, pred)

    return

def parcoursEnProfondeurEtape(modele, known, pred, s, wrong_path = False):
    known.add(s)

    for v in modele.getVoisins(s):
        if v not in known:
            pred[v] = s
            if wrong_path:
                modele.addFleche(s, v, "Black")
            parcoursEnProfondeurEtape(modele, known, pred, v, wrong_path)

    return

def bellmanFord(modele):
    pass
   
def relacher_arc(modele, distances, pred, v1, v2):
    pass
   
def dijkstra(modele):
    pass


def astar(modele):
    pass

