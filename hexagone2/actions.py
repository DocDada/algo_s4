#coding: utf-8
"""
liste des methodes disponibles

graphe.getBleu() -> Sommet

graphe.getRouge() -> Sommet

graphe.addFleche(sommet1, sommet2, couleur) -> None

graphe.change_couleur_arc(sommet1, sommet2, couleur) -> None

graphe.change_couleur_hex(self, sommet, couleur) -> None

graphe.addTexte(sommet, str) -> None

graphe.getListeSommets() -> [Sommet, Sommet, ...]

graphe.getVoisinsSortants( sommet) -> [Sommet, Sommet, ...]

graphe.getVoisinsEntrants(self, sommet):-> [Sommet, Sommet, ...]


"""



from dxg_graphe import *
import random
import time

def distribution_menu_algo(graphe, label):
    if label == "Parcours en largeur":
        parcoursEnLargeur(graphe)
    elif label == "Composantes connexes":
        compConnexes(graphe)
    elif label == "Numérotation topologique":
        num_topo_ou_cycle(graphe)
    elif label == "Parcours en profondeur":
        parcoursEnProfondeur(graphe)




def parcoursEnLargeur(graphe):
	pass
	

def num_topo_ou_cycle(graphe):
    pass

def compConnexes(graphe):
    pass

def parcoursEnProfondeur(graphe):
	pred = {}
	pre = {}
	suf = {}
	connu = set([])

	for s in graphe.getListeSommets():
		if s not in connu:
			parcoursEnProfondeurEtape(graphe, pred, pre, suf, connu, s)

	return [pre, suf, pred]


def parcoursEnProfondeurEtape(graphe, pred, pre, suf, connu, s):
	connu.add(s)
	pre[s] = len(pre)
	for v in graphe.getVoisinsSortants(s):
		if v not in connu:
			pred[v] = s
			parcoursEnProfondeurEtape(graphe, pred, pre, suf, connu, v)
	suf[s] = len(suf)
	graphe.addTexte(s, str(pre[s]) +  "/" + str(suf[s]))





