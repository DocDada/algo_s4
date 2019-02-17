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
    depart = graphe.getBleu()
    pred = {}
    distance = {}
    if not depart:
        depart = (graphe.getListeSommets())[0]
    distance[depart] = 0
    attente = [depart]

    while attente:
        v = attente.pop(0)

        for s in graphe.getVoisinsSortants(v):
            pred[s] = v
            distance[s] = distance[v] + 1
            graphe.addTexte(s, distance[s])
            attente.append(s)

    draw_path_start_end(graphe, pred)


def draw_path_start_end(graphe, pred):
    """Draws a red line between the blue and the red dot, if they exist
    """
    v = graphe.getRouge()
    depart = graphe.getBleu()

    if not (v and depart):
        return

    while v in pred:
        predecesseur = pred[v]
        graphe.change_couleur_arc(predecesseur, v, "red")
        if predecesseur == depart:
            break
        v = predecesseur




def num_topo_ou_cycle(graphe):
    """Détection de cycles et tri topologique"""
    pre= {}
    suf = {}
    connus = set([])
    couple_vertexes = None
    #through = True

    for s in graphe.getListeSommets():
        if not pre.has_key(s):
            cycle = pp_etape(graphe, pre, suf, s)
            if cycle:
                print "\nCYCLE : ", cycle
                if not couple_vertexes:
                    couple_vertexes = cycle
                else:
                    for d in cycle:
                        couple_vertexes.append(d)


    print "-------------------"

    #inv_pre = {v: k for k, v in pre.iteritems()}
    #inv_suf = {v: k for k, v in suf.iteritems()}
    inv_pre = dict((v, k) for k, v in pre.iteritems())
    inv_suf = dict((v, k) for k, v in suf.iteritems())
    print inv_pre, inv_suf


    print "-------------------"

    if couple_vertexes:
        print "\n\nCOUPLE_VERTEXES : ", couple_vertexes
        # only draws one cycle
        for vertexes in couple_vertexes:
            print "\nVERTEXES : ", vertexes
            draw_cycle_v3(graphe, pre[vertexes[0]], suf[vertexes[1]], inv_pre, inv_suf)
            print "\nFINI\n"

    return


def pp_etape(graphe, pre, suf, s):
    pre[s] = len(pre)
    has_cycle = None

    for v in graphe.getVoisinsSortants(s):
        if not pre.has_key(v):
            has_cycle = pp_etape(graphe, pre, suf, v)
        elif not suf.has_key(v):# cycle/boucle
            graphe.change_couleur_arc(s, v, "blue")
            if not has_cycle:
                has_cycle = [[s, v]]
            else:
                has_cycle.append([s, v])

    suf[s] = len(suf)
    graphe.addTexte(s, str(pre[s]) + "/" + str(suf[s]))

    return has_cycle






def draw_cycle(graphe, s, v):
    """Draws a red cycle between the dots s and v"""
    while s != v:# while the dots are not the same
        s2 = (graphe.getVoisinsEntrants(s)).pop()
        v2 = (graphe.getVoisinsSortants(v)).pop()
        graphe.change_couleur_arc(s2, s, "red")
        graphe.change_couleur_arc(v, v2, "red")
        s = s2
        v = v2





def draw_cycle_v2(graphe, s, v):
    """Draws a red cycle between the dots s and v"""

    while s != v:# while the dots are not the same
        if len(graphe.getVoisinsSortants(s)) == 1:
            s2 = (graphe.getVoisinsEntrants(s)).pop(0)
            graphe.change_couleur_arc(s2, s, "red")
            s = s2
        if len(graphe.getVoisinsSortants(v)) == 1:
            v2 = (graphe.getVoisinsSortants(v)).pop(0)
            graphe.change_couleur_arc(v, v2, "red")
            v = v2






def draw_cycle_v3(graphe, s, v, pre, suf):
    """Draws a red cycle between the dots s and v"""

    first = True
    while (pre[s] and suf[v] and pre[s] != suf[v]) or first:# while the dots are not the same
        #graphe.change_couleur_arc(pre[s - 1], pre[s], "red")
        #graphe.change_couleur_arc(suf[v], suf[v + 1], "red")
        #s = s - 1
        #v = v - 1
        graphe.change_couleur_arc(suf[s + 1], suf[s], "red")
        if suf[v] in graphe.getVoisinsSortants(suf[v-1]):
            graphe.change_couleur_arc(suf[v - 1], suf[v], "green")
        else:
            graphe.change_couleur_arc(suf[v], suf[v - 1], "green")
        s = s - 1
        v = v - 1
        print "S = ", s, "V : ", v
        first = False











def pp_etape_cycle(graphe, s):
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





