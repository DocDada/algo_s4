from hexa_controleur import *
from hexa_modele import *
from hexa_vue import *


class Root(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # VALEURS A MODIFIER POUR LE NB DE CASES ET LA TAILLE DES HEXAGONES ####
        nbcasesx = 25
        nbcasesy = 10
        unit = 10
        ########################################################################

        hauteur = (4*unit+1)*(nbcasesy+.5)
        largeur = (3*unit+1)*(nbcasesx+.5)


        self.title('Hexagones')
        controleur = Controleur(None, None)
        vue = MainWindow(self,  controleur, largeur, hauteur, nbcasesx,nbcasesy, unit)
        modele = Grille_modele(vue.grille, nbcasesx, nbcasesy)
        controleur.vue = vue
        controleur.model = modele


if __name__ == '__main__':
    root = Root()
    root.mainloop()
