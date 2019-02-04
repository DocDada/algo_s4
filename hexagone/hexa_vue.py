#coding: utf-8
import Tkinter as tk
from hexa_controleur import *




class MainWindow(tk.Frame):
    def __init__(self, parent, controleur, largeur, hauteur, nbcasesx, nbcasesy, unit):
        tk.Frame.__init__(self, parent)
        self.grid()
        self.parent = parent
        self.controleur = controleur
        self.palette = Palette(self, controleur)
        self.palette.grid(row=0,column=0, sticky = 'W')


        self.grille = Grille(largeur, hauteur, nbcasesx, nbcasesy, unit, self)
        self.grille.grid(row=0,column=1, sticky = 'E')
        self.focus_set()
        menubar = tk.Menu(self.parent)
        self.labels = ["Tout blanc", "Tout noir", "Effacer Resultats", "Aleatoire","Parcours en profondeur", "Parcours en largeur", "Comp connexes", "Bellman-Ford", "Dijskstra","A-star"]

        for lab in self.labels:
            menubar.add_command(label = lab, command = (lambda lb = lab:self.action(lb)))
        #rq sur la ligne ci-dessus : afin que la lambda-fonction, a qui on ne donnera
        #pas de paramètre, evalue lab dans la boucle for et pas plus tard,
        #on utilise un parametre lb avec valeur par défaut lab.
        self.menubar = menubar
        #montrer le menu
        self.parent.config(menu=menubar)
        self.freezed = False

    def action(self, lab):
        self.freezed = True
        self.freeze()
        self.controleur.bouton(lab)
        self.unfreeze()
        self.freezed = False


    def freeze(self):
        for lab in self.labels:
            self.menubar.entryconfig(lab, state = "disabled")

    def unfreeze(self):
        for lab in self.labels:
            self.menubar.entryconfig(lab, state = "normal")

class Palette(tk.Frame):
    def __init__(self, parent, controleur):
        tk.Frame.__init__(self, parent, width = 40, height= 50)
        self.parent = parent
        self.controleur = controleur
        self.choixDeCouleur = tk.StringVar()
        self.radio = []
        self.radio.append(tk.Radiobutton(self, width = 10, indicatoron = 0, state="active", command = self.chgt, variable = self.choixDeCouleur, text = "Black", value = "Black").grid(row=0,column=0))
        couleurs = ("White",  "Blue", "Green", "Yellow", "Depart", "Objectif")
        for i in range(len(couleurs)):
            self.radio.append(tk.Radiobutton(self, width = 10, indicatoron = 0, command = self.chgt, variable = self.choixDeCouleur, text = couleurs[i], value = couleurs[i]).grid(row=i+1,column=0))
        self.choixDeCouleur.set("Black")
        self.grid()

    def chgt(self):
        pass


class Grille(tk.Canvas):
    def __init__(self, largeur, hauteur, nbcasesx, nbcasesy, unit, parent):
        tk.Canvas.__init__(self, width=largeur, height=hauteur, bg="black", confine=True)
        self.coord_to_hex = {}  #dico des hexagones par coordonnees
        self.hex_to_coord = {}  #dico des hexagones par item
        self.arrows = []
        self.texts = []
        self.zoom = 0
        self.unit = unit
        self.largeur = largeur
        self.hauteur = hauteur
        self.xview = 0 #largeur/2
        self.yview = 0 #hauteur/2
        self.parent = parent
        self.controleur = self.parent.controleur
        self.lclicked = False
        for i in range(nbcasesx):
            for j in range(nbcasesy):
                hex = self.add_hex(i,j) 
                self.tag_bind(hex, "<ButtonPress-1>", self.onLClick)
                self.tag_bind(hex, "<B1-Motion>", self.onLClick)
                self.tag_bind(hex, "<ButtonPress-3>", self.onRClick)
        self.config(scrollregion=self.bbox("all"))



        #self.pack(expand="yes")


    def reset(self, couleur):
       for x,y in self.coord_to_hex:
            self.changeCouleurHex(x, y, couleur)
       self.resetResults()


    def resetResults(self):
        for a in self.arrows:
            self.delete(a)
        self.arrows = []
        for t in self.texts:
            self.delete(t)
        self.texts = []

    def add_hex(self, i, j):
        x, y = 2*self.unit+ (3*self.unit+1)*i,2*self.unit +(4*self.unit+1)*j +(2*self.unit)*(i%2)
        hex = self.create_polygon(x+2*self.unit, y, x+self.unit, y+2*self.unit, x- self.unit, y+2*self.unit, x-2*self.unit, y, x-self.unit,y-2*self.unit, x+self.unit, y-2*self.unit, fill = "white")
        self.coord_to_hex[(i,j)] = hex
        self.hex_to_coord[hex] = (i,j)

        return hex

    def add_arrow(self, i1, j1, i2, j2, couleur):
        x1, y1 = 2*self.unit+ (3*self.unit+1)*i1,2*self.unit +(4*self.unit+1)*j1 +(2*self.unit)*(i1%2)
        x2, y2 = 2*self.unit+ (3*self.unit+1)*i2,2*self.unit +(4*self.unit+1)*j2 +(2*self.unit)*(i2%2)
        fleche =self.create_line(x1, y1, x2, y2, fill =couleur, arrow = "last", width = 5,smooth=1)
        self.arrows.append(fleche)
        return fleche


    def add_text(self, i, j, texte):
        x, y = 2*self.unit+ (3*self.unit+1)*i - self.unit,2*self.unit +(4*self.unit+1)*j +(2*self.unit)*(i%2)
        nouvtexte = self.create_text(x, y, text=texte)
        self.texts.append(nouvtexte)
        return nouvtexte

    def onLClick(self, event):
        if not self.parent.freezed:
            hextag = self.find_closest(self.canvasx(event.x),self.canvasy(event.y))[0]
            hexCoord = self.hex_to_coord[hextag]
            self.controleur.onLClick(hexCoord)

    def changeCouleurHex(self, x, y, couleur):
        self.itemconfig(self.coord_to_hex[(x,y)], fill = couleur)



    def onRClick(self, event):
        pass


    def miseAjour(self, parametres):
        x, y = parametres["x"], parametres["y"]
        self.changeCouleurHex(x, y, parametres["arg"])


    def miseAJour(self, message):
        if observable.info[0] == "couleur":
            self.changer_case(observable.info[1], observable.info[2], observable.data)
        if observable.info[0] == "aretes":
            x = observable.info[1]
            y = observable.info[2]
            d = observable.info[3]
            self.changer_arete(x, y, d, observable.data)


