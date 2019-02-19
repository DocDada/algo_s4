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
        compConnexes_prof(graphe)
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






# Correction
def num_topo_ou_cycle(graphe):

    connus = set([])
    suffixes = {}
    predecesseurs = {}
    res = None

    for x in graphe.getListeSommets():
        if x not in connus:
            res = numtopo_etape(graphe, x, connus, predecesseurs, suffixes)
        if res is not None:
            break

    if res is not None:
        x, v = res
        courant = x
        graphe.change_couleur_arc(x, v, "Red")

        while courant != v:
            pred = predecesseurs[courant]
            graphe.change_couleur_arc(pred, courant, "Red")
            courant = pred
    else:
        n = len(graphe.getListeSommets())
        for x in graphe.getListeSommets():
            graphe.addTexte(x, n - 1 - suffixes[x])

# Correction
def numtopo_etape(graphe, x, connus, predecesseurs, suffixes):

    connus.add(x)

    for v in graphe.getVoisinsSortants(x):
        if v not in connus:
            predecesseurs[v] = x
            res = numtopo_etape(graphe, v, connus, predecesseurs, suffixes)
            if res is not None:
                return res
        elif v not in suffixes:
            return [x, v]
    suffixes[x] = len(suffixes)
    return None



def num_topo_ou_cycle_v2(graphe):
    """Détection de cycles et tri topologique"""
    pre= {}
    suf = {}
    connus = set([])
    couple_vertexes = None

    for s in graphe.getListeSommets():
        if not pre.has_key(s):
            cycle = pp_etape(graphe, pre, suf, s)
            if cycle:
                #print "\nCYCLE : ", cycle
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
    #print inv_pre, inv_suf


    print "-------------------"

    if couple_vertexes:
        #print "\n\nCOUPLE_VERTEXES : ", couple_vertexes
        # only draws one cycle
        for vertexes in couple_vertexes:
            print "\nVERTEXES : ", vertexes
            draw_cycle(graphe, vertexes[0], vertexes[1])
            #draw_cycle_v3(graphe, pre[vertexes[0]], suf[vertexes[1]], inv_pre, inv_suf)
            print "\nFINI\n"

    return


def pp_etape(graphe, pre, suf, s):
    pre[s] = len(pre)
    has_cycle = None

    for v in graphe.getVoisinsSortants(s):
        if not pre.has_key(v):
            has_cycle = pp_etape(graphe, pre, suf, v)
        elif not suf.has_key(v):# cycle/boucle
            #graphe.change_couleur_arc(s, v, "red")
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




def compConnexes_prof(graphe):
    suffixes = (parcoursEnProfondeur(graphe))[1]
    ordre_sommets = sorted(suffixes, key=lambda x:suffixes[x], reverse = True)

    compteur_composantes = 0
    composantes = {}

    for v in ordre_sommets:
        if v not in composantes:
            #print "Compteur : ", compteur_composantes
            composantes[compteur_composantes] = sommets_accedant_a(graphe, v, composantes)
            for s in composantes[compteur_composantes]:
                #graphe.addTexte(s, compteur_composantes)
                graphe.change_couleur_hex(s, LISTE_COULEURS[compteur_composantes])
            compteur_composantes += 1




def sommets_accedant_a(graphe, but, composantes):
    connus = set([but])
    attente = [but]

    while attente:
        courant = attente.pop()
        for v in graphe.getVoisinsEntrants(courant):
            if v not in connus and v not in composantes.values():
                connus.add(v)
                attente.append(v)


    return list(connus)


def compConnexes(graphe):
    """Obtenir numérotation suffixe
    comp = sommet : numero de composante"""
    suf = (parcoursEnProfondeur(graphe))[1]

    suf_inv = {}
    compteur_comp = 0
    comp = {}
    n = graphe.getListeSommets()

    """for k, s in suf:
        suf_inv[k] = n - 1 - s
    """
    suf_inv = sorted(suf, reverse = True)
    #print suf_inv

    while suf_inv:
        v = suf_inv.pop()
        if v not in comp:
            comp[compteur_comp] = composante(graphe, v, compteur_comp)
            #print "compConnexes : ", comp
            compteur_comp += 1

    return

def composante(graphe, s, num_comp):

    """
        attente = graphe.getVoisinsSortants(s)
        while attente:
            v = attente.pop(0)

            graphe.addTexte(v, num_comp)
            attente.append(graphe.getVoisinsSortants(v))
            comp[num_comp] = v
    """

    attente = [s]
    connus = set([])
    while attente:
        v = attente.pop(0)
        for so in graphe.getVoisinsEntrants(v):
            if so not in connus:
                attente.append(so)
                connus.add(so)
                graphe.addTexte(so, num_comp)

    #print "composante : ", comp
    return list(connus)






"""
def graphe_inverse(graphe):
    graphe_inv = {key:None for key in graphe.getListeSommets()}

    for v in graphe.getListeSommets():
        for s in graphe.getVoisinsSortants(v):
            graphe_inv[s].append(v)

    return graphe_inv
"""

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
    #graphe.addTexte(s, str(pre[s]) +  "/" + str(suf[s]))





