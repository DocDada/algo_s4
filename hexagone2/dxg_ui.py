#coding: utf-8
import Tkinter as tk
from dxg_graphe import *
from actions import *
from functools import partial

class Root(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # VALEURS A MODIFIER POUR LE NB DE CASES ET LA TAILLE DES HEXAGONES ####
        nbcasesx = 20
        nbcasesy = 20
        unit = 20
        ########################################################################

        hauteur = (4*unit+1)*(nbcasesy+.5)
        largeur = (3*unit+1)*(nbcasesx+.5)


        self.title('Graphes orientés')
        vue = MainWindow(self,  largeur, hauteur, nbcasesx,nbcasesy, unit)
        graphe = Graphe(vue.grille, nbcasesx, nbcasesy)
        vue.grille.graphe = graphe


def truc(main, param):
    main.action(param)

class MainWindow(tk.Frame):
    def __init__(self, parent, largeur, hauteur, nbcasesx, nbcasesy, unit):
        tk.Frame.__init__(self, parent)
        self.grid()
        self.parent = parent
        self.palette = Palette(self)
        self.palette.grid(row=0,column=0, sticky = 'W')


        self.grille = Grille(largeur, hauteur, nbcasesx, nbcasesy, unit, self)
        self.grille.grid(row=0,column=1, sticky = 'E')
        self.focus_set()

        #Menu du dessus
        menubar = tk.Menu(self.parent)
        editmenu = tk.Menu(menubar, tearoff=0)
        algomenu = tk.Menu(menubar, tearoff=0)

        editmenu.add_command(label = "Réinitialiser", command = (lambda:self.grille.reset(self)))
        editmenu.add_command(label = "Effacer annotations", command = self.grille.reset_all_but_graph)
        editmenu.add_command(label = "Charger", command = (lambda :None))
        editmenu.add_command(label = "Sauvegarder", command = (lambda :None))
        editmenu.add_command(label = "Générer graphe aléatoire", command = (lambda :None))
        self.labels = ["Parcours en profondeur", "Parcours en largeur", "Numérotation topologique", "Composantes connexes"]

        for lab in self.labels:
            algomenu.add_command(label = lab, command = (lambda lab = lab:self.menu_called(lab)))
        #rq sur la ligne ci-dessus : afin que la lambda-fonction, a qui on ne donnera
        #pas de paramètre, evalue lab dans la boucle for et pas plus tard,
        #on utilise un parametre lb avec valeur par défaut lab.
        self.menubar = menubar
        menubar.add_cascade(label="Édition", menu=editmenu)
        menubar.add_cascade(label="Algorithmes", menu=algomenu)
        #montrer le menu
        self.parent.config(menu=menubar)
        self.freezed = False

    def menu_called(self, event):
        self.freezed = True
        self.freeze()
        distribution_menu_algo(self.grille.graphe, event)
        self.unfreeze()
        self.freezed = False

    def freeze(self):
        for lab in ["Édition", "Algorithmes"]:
            self.menubar.entryconfig(lab, state = "disabled")

    def unfreeze(self):
        for lab in ["Édition", "Algorithmes"]:
            self.menubar.entryconfig(lab, state = "normal")

    def getPaletteMode(self):
        return self.palette.mode.get()


class Palette(tk.Frame):
    """le menu à gauche """
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width = 40, height= 50)
        self.parent = parent
        self.mode = tk.StringVar()
        self.radio = []
        couleurs = ("+Sommet",  "+Arc","-Sommet","select bleu", "select rouge")
        for i in range(len(couleurs)):
            self.radio.append(tk.Radiobutton(self, width = 10, height = 4,indicatoron = 0, variable = self.mode, text = couleurs[i], value = couleurs[i]).grid(row=i+1,column=0))
        self.mode.set("+Arc")
        self.grid()



class Hex:
    def __init__(self, grille, i, j):
        self.i = i
        self.j = j
        u = grille.unit
        x, y = 2*u+ (3*u+1)*i,2*u +(4*u+1)*j +(2*u)*(i%2)
        self.x = x
        self.y = y
        self.grille = grille
        self.handle = grille.create_polygon(x+2*u, y, x+u, y+2*u, x- u, y+2*u, x-2*u, y, x-u,y-2*u, x+u, y-2*u, fill = "Gray90", outline="Gray85")
        self.tk_dot = None
        self.fleches_sortantes = {}  #dico hex voisins -> handle fleche
        grille.tag_bind(self.handle, "<B1-Motion>", self.onClick)
        grille.tag_bind(self.handle, "<Button-1>", self.onClick)

    def __hash__(self):
        return self.handle

    def onClick(self, event):
        self.grille.gestionClicks(event)

    def add_dot(self):
        if not self.has_dot():
            x = self.x  ; y = self.y ; u = self.grille.unit / 2
            self.tk_dot = self.grille.create_oval(x-u,y-u,x+u,y+u,fill='Black', outline='Gray80', state="disabled")
            self.grille.change_hex_color(self, "White")
            self.grille.graphe.ajouter_sommet(self)

    def remove_dot(self):
        self.grille.delete(self.tk_dot)
        self.tk_dot = None
        self.grille.graphe.supprimer_sommet(self)
        self.grille.change_hex_color(self, "Gray90")

    def has_dot(self):
        return self.tk_dot != None

    def remove_fleche_sortante(self, hex):
            self.grille.delete(self.fleches_sortantes[hex])
            del self.fleches_sortantes[hex]



    def remove_all_arrows(self):
        vois = self.getHexVoisins()
        for hex in vois:
            if hex in self.fleches_sortantes:
                self.remove_fleche_sortante(hex)
            if self in hex.fleches_sortantes:
                hex.remove_fleche_sortante(self)


    def getHexVoisins(self):
        #renvoie la liste des Hex voisins
        vois = []
        for u,v in ( (-1,-1 + self.i%2), (-1,0 + self.i%2), (1,-1 + self.i%2), (1,0 + self.i%2), (0,-1), (0,1)):
            xv = self.i + u
            yv = self.j + v

            if self.grille.coord_to_Hex.has_key((xv, yv)):
               vois.append(self.grille.coord_to_Hex[(xv, yv)])
        return vois






class Grille(tk.Canvas):
    def __init__(self, largeur, hauteur, nbcasesx, nbcasesy, unit, parent):
        tk.Canvas.__init__(self, width=largeur, height=hauteur, bg="Gray80", confine=True)
        self.Graphe = None  #mis à jour par Root
        self.hexs = {}   #dico des hex par numero tk associe
        self.coord_to_Hex = {}
        self.texts = {}
        self.zoom = 0
        self.unit = unit
        self.largeur = largeur
        self.hauteur = hauteur
        self.xview = 0 #largeur/2
        self.yview = 0 #hauteur/2
        self.parent = parent
        for i in range(nbcasesx):
            for j in range(nbcasesy):
                hex = Hex(self,i,j)
                self.coord_to_Hex[(i,j)] = hex
                self.hexs[hex.handle] = hex
        self.config(scrollregion=self.bbox("all"))

        self.tetedArc = None
        self.bind("<ButtonRelease>", self.buttonRelease)

        self.bleu = None
        self.rouge = None


    def buttonRelease(self, event):
        self.tetedArc = None


    def add_arrow(self, hex1, hex2, couleur):
        if hex2 not in hex1.fleches_sortantes and hex1 not in hex2.fleches_sortantes:
            marge = 0.15
            x1, x2, y1, y2 = hex1.x, hex2.x, hex1.y, hex2.y
            x1, y1, x2, y2 = x1 + marge*(x2-x1), y1 + marge*(y2-y1), x2-marge*(x2-x1), y2-marge*(y2-y1)
            fleche =self.create_line(x1, y1, x2, y2, fill =couleur, arrow = "last", width = 5,smooth=1)
            hex1.fleches_sortantes[hex2] = fleche


            #mise a jour graphe
            self.graphe.sommets[hex1].voisins_sortants.append(self.graphe.sommets[hex2])
            self.graphe.sommets[hex2].voisins_entrants.append(self.graphe.sommets[hex1])

            return fleche

    def change_arrow_color(self, hex1, hex2, couleur):
        self.itemconfig(hex1.fleches_sortantes[hex2], fill=couleur)


    def change_hex_color(self, hex, couleur):
        self.itemconfig(hex.handle, fill=couleur)

    def add_text(self, hex, texte):
        x, y = hex.x -self.unit, hex.y - self.unit
        text_handle = self.create_text(x, y, text=texte)
        rect_handle = self.create_rectangle(self.bbox(text_handle), fill='White')
        self.tag_lower(rect_handle, text_handle)
        self.texts[hex] = (text_handle, rect_handle)

    def remove_text(self, hex):
        self.delete(self.texts[hex][0]) #suppression du texte
        self.delete(self.texts[hex][1]) #suppression du cadre du texte
        self.texts.pop(hex)


    def change_couleur_dot(self, hex, couleur):
        if hex and hex.has_dot():
            self.itemconfig(hex.tk_dot, fill = couleur)


    def reset(self):
        pass

    def reset_all_but_graph(self):
        for h in self.texts:
            handles = self.texts[h]
            print h
            self.delete(handles[0])
            self.delete(handles[1])
        self.texts = {}





    def gestionClicks(self, event):
        if not self.parent.freezed :
            handle = self.find_closest(self.canvasx(event.x), self.canvasy(event.y))[0]
            if handle in self.hexs:
                hex = self.hexs[handle]
                mode = self.parent.getPaletteMode()
                if mode == "+Sommet" and not hex.has_dot():
                    hex.add_dot()
                elif mode == "-Sommet" and hex.has_dot():
                    hex.remove_all_arrows()
                    hex.remove_dot()
                elif mode == "+Arc" and self.tetedArc==None:
                    self.tetedArc = hex
                elif mode == "+Arc":
                    if hex in self.tetedArc.getHexVoisins():
                        #on ajoute les sommets s'ils n'existent pas
                        if not hex.has_dot():
                            hex.add_dot()
                        if not self.tetedArc.has_dot():
                            self.tetedArc.add_dot()
                        self.add_arrow(self.tetedArc, hex, "Gray40")
                    self.tetedArc = hex
                elif mode == "select bleu":
                    self.change_couleur_dot(self.bleu, "Black")
                    self.bleu = hex
                    self.change_couleur_dot(hex, "Blue")
                    self.graphe.bleu = self.graphe.sommets[hex]
                elif mode == "select rouge":
                    self.change_couleur_dot(self.rouge, "Black")
                    self.rouge = hex
                    self.change_couleur_dot(hex, "Red")
                    self.graphe.rouge = self.graphe.sommets[hex]
                elif mode == "Random":
                    self.randomGraph()


    def randomGraph(self):
        pSommet = 0.7
        pArc = 0.4
        for h in self.hexs.values():
            if random.random() < pSommet:
                h.add_dot()
        hexs = self.hexs.values()
        random.shuffle(hexs)
        for h in hexs:
            if h.has_dot():
                for h1 in h.getHexVoisins():
                    if h1.has_dot() and random.random() < pArc:
                        self.add_arrow(h,h1,"Gray40")



if __name__ == '__main__':
    root = Root()
    root.mainloop()

