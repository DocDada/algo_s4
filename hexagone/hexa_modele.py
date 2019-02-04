#coding: utf-8
import random
import math

class Grille_modele(object):

    def __init__(self, observateur, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.hexs = {}  # dictionnaire de (coordonnees : Hex)
        self.observateur = observateur
        self.hexs = {}  # dictionnaire de (coordonnees : Hex)
        for x in range(self.largeur):
            for y in range(self.hauteur):
                self.hexs[(x,y)] = Hex(x, y, self.observateur)
        self.depart = self.hexs[(0,self.hauteur-1)]
        self.depart.change_couleur("Magenta")
        self.objectif = self.hexs[(self.largeur-1,0)]
        self.objectif.change_couleur("Red")

    def distance_a_vide(self,sommet1, sommet2):
        x1, y1 = sommet1.x, sommet1.y - sommet1.x/2
        z1 = -x1 -y1
        x2, y2 = sommet2.x, sommet2.y - sommet2.x/2
        z2 = -x2 -y2
        return max(abs(x1-x2), abs(y1-y2), abs(z1-z2))


    def reset(self, couleur):
        for key,hex in self.hexs.items():
            hex.change_couleur(couleur, False)
        self.depart.change_couleur("Magenta")
        self.objectif.change_couleur("Red")


    def addFleche(self, sommet1, sommet2, couleur):
        return self.observateur.add_arrow(sommet1.x, sommet1.y, sommet2.x, sommet2.y, couleur)

    def delFleche(self, ref):
        self.observateur.delete(ref)

    def deltexte(self, ref):
        self.observateur.delete(ref)

    def addTexte(self, sommet, texte):
        return self.observateur.add_text(sommet.x, sommet.y, texte)

    def getListeSommets(self, tous=False):
        liste = []
        for key, value in self.hexs.items():
            if tous or value.couleur != "Black":
                liste.append(value)
        return liste

    def getDepart(self):
        return self.depart

    def getObjectif(self):
        return self.objectif

    def notify(self, message):
        self.observateur.miseAJour(message)

    def getVoisins(self, sommet, tous=False):
        #renvoie la liste des voisins par coordonnees
        vois = []
        for u,v in ( (-1,-1 + sommet.x%2), (-1,0 + sommet.x%2), (1,-1 + sommet.x%2), (1,0 + sommet.x%2), (0,-1), (0,1)):
            xv = sommet.x + u
            yv = sommet.y + v
            if self.hexs.has_key((xv, yv)):
               if tous or self.hexs[(xv, yv)].couleur != "Black":
                    vois.append(self.hexs[(xv, yv)])
        return vois


    def change_objectif(self, nouvelObjectif):
        self.objectif.change_couleur("White")
        self.objectif = self.hexs[nouvelObjectif]
        self.objectif.change_couleur("Red")


    def change_depart(self, nouveauDepart):
        self.depart.change_couleur("White")
        self.depart = self.hexs[nouveauDepart]
        self.depart.change_couleur("Magenta")

    def random(self):
        couleurs = ["White", "Blue", "Green", "Yellow", "Black"]
        for key, hex in self.hexs.items():
            if hex != self.depart and hex != self.objectif:
                hex.change_couleur(couleurs[random.randint(0,4)])


    def longueur(self, sommet1, sommet2):
        """calcule la longueur de l'arête entre deux sommets voisins suivant leur couleur.
        A chaque couleur est associée un cout.
        la distance est alors (cout1 + cout2) / 2 """
        couts = {"White" : 1,
                 "Blue" : 10,
                 "Green" : 5,
                 "Yellow" : 2,
                 "Red" : 1,
                 "Magenta" : 1}
        return (couts[sommet1.couleur]+couts[sommet2.couleur])/2


class Hex(object):
    def __init__(self, x, y, observateur):
        self.text = ""
        self.couleur = "White"
        self.x = x
        self.y = y
        self.observateur = observateur



    def change_couleur(self, couleur, notify = True):
        self.couleur = couleur
        parametres = {"x": self.x, "y": self.y, "type" : "couleur", "arg" : self.couleur}
        if notify:
            self.notify(parametres)

    def notify(self, parametres):
        self.observateur.miseAjour(parametres)


class File_Priorite:
    def __init__(self, liste = []):
        self.tab = [None]
        self.indices = {}
        for cle, valeur in liste:
            self.ajouter(cle, valeur)

    def _echanger(self, i1, i2):
        assert len(self.tab) == len(self.indices) + 1
        self.tab[i1], self.tab[i2] = self.tab[i2], self.tab[i1]
        self.indices[ self.tab[i1][0] ] = i1
        self.indices[ self.tab[i2][0] ] = i2

    def _ajouter_feuille(self,cle, valeur):
        self.tab.append((cle,valeur))
        self.indices[cle] = len(self.tab) - 1
 

    def ajouter(self,cle, valeur):
        if cle in self:
            raise Exception("clé déjà présente dans la file")

        self._ajouter_feuille(cle, valeur)
        i = self.indices[cle]

        while i>1 and self.tab[i/2][1] > self.tab[i][1] :
            self._echanger(i, i/2)
            i = i/2


    def diminuer_valeur(self, cle, nouvelle_val):
        assert len(self.tab) == len(self.indices) + 1
        i = self.indices[cle]
        self.tab[i] = (cle, nouvelle_val)
        while i>1 and self.tab[i/2][1] > self.tab[i][1]:
            self._echanger(i, i/2)
            i = i/2

    def extraire_min(self):
        assert len(self.tab) == len(self.indices) + 1
        if len(self.tab) <=1:
            raise Exception("La file de priorités est vide")
        result = self.tab[1]


        self.indices.pop(result[0])
        if len(self.tab) == 2:
            self.tab.pop()
            return result
        self.tab[1] = self.tab.pop()
        i = 1
        fini = False
        while not fini:
            fini = True
            mini = self.tab[i][1]
            if 2*i < len(self.tab):
                mini = min(mini, self.tab[2*i][1])
            if 2*i + 1 < len(self.tab): 
                mini = min(mini, self.tab[2*i+1][1])
            if mini < self.tab[i][1]:
                fini = False
                if mini == self.tab[2*i][1]:
                    self._echanger(i,2*i)
                    i = 2*i
                else:
                    self._echanger(i,2*i+1)
                    i = 2*i +1

        return result

    def __nonzero__(self):
        return len(self.tab) > 1

    def __contains__(self, cle):
        return cle in self.indices
