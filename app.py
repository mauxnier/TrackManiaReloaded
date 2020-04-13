# coding: utf-8

"""TrackManiaReloaded : by el famoso Killian Monnier

TrackManiaReloaded est un jeu bien connu des pilotes.

Usage: python app.py
-
-
-
-

"""

# Importation de librairies
from tkinter import *
import math

""" https://stackoverflow.com/questions/22835289/how-to-get-tkinter-canvas-to-dynamically-resize-to-window-width """
# Une sous-classe de Canvas pour redimensionner le canva en fonction de la window
class ResizingCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        # Détermine le ratio de l'ancien width/height au nouveau width/height
        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height

        # Redimensionne le canvas
        self.config(width = self.width, height = self.height)

        """
        # Redimensionne tout les objets avec le tag "all"
        self.scale("all", 0, 0, wscale, hscale)
        """

# Affiche les coordonnées de la souris dans la console
def display_coordinates(event):
    x = event.x
    y = event.y
    print(x, y)

# Définition des variables globales
firstClick = True
mycanvas = None
x1 = 0
y1 = 0
x2 = 0
y2 = 0

# Dessine des lignes entre chaque click de la souris
def draw_track(event):
    global mycanvas, firstClick, x1, y1
    radius1 = 100
    radius2 = radius1 / 2
    radius3 = radius1-radius2
    
    if firstClick:
        # Récupération des coordonnées de la souris
        x1 = event.x
        y1 = event.y

        # Création du cercle
        xyR1 = x1-radius1, y1-radius1, x1+radius1, y1+radius1
        mycanvas.create_oval(xyR1)

        firstClick = False
        
    else:
        # Récupération des coordonnées de la souris
        x2 = event.x
        y2 = event.y

        # Création du cercle
        xyR1 = x2-radius1, y2-radius1, x2+radius1, y2+radius1
        mycanvas.create_oval(xyR1)

        xyR2 = x1-radius2, y1-radius2, x1+radius2, y1+radius2
        mycanvas.create_oval(xyR2)

        xyR3 = x2-radius3, y2-radius3, x2+radius3, y2+radius3
        mycanvas.create_oval(xyR3)

        """Création de la route : https://gieseanw.wordpress.com/2012/09/12/finding-external-tangent-points-for-two-circles/"""
        a = x1
        b = y1

        # Distance Euclidienne entre deux cercles : D
        #mycanvas.create_line(x1, y1, x2, y2)
        distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        D = distance
        print("D = distance =", D)

        # H
        #mycanvas.create_line(x1, y1-radius2, x2, y2)
        H = math.sqrt(D**2 - (radius1-radius2)**2)
        print("H :", H)

        # X = H
        #mycanvas.create_line(x1, y1-radius1, x2, y2-radius3)
        X = H
        print("X = H =", X)

        # Y
        #mycanvas.create_line(x1, y1-radius1, x2, y2)
        Y = math.sqrt(H**2 + radius2**2)
        print("Y :", Y)

        # Theta
        theta = math.acos((radius1**2 + D**2 - Y**2) / (2 * radius1 * D))
        theta = theta + math.atan2(y2 - y1, x2 - x1)
        print("Theta :", theta)

        # Xt : Point de la tangente externe
        e1R1 = x1 + radius1 * math.cos(theta)
        f1R1 = y1 + radius1 * math.sin(theta)
        Xt1R1 = (e1R1,f1R1)

        e2R1 = x2 + radius1 * math.cos(theta)
        f2R1 = y2 + radius1 * math.sin(theta)
        Xt2R1 = (e2R1,f2R1)

        e1R2 = x1 + radius2 * math.cos(theta)
        f1R2 = y1 + radius2 * math.sin(theta)
        Xt1R2 = (e1R2, f1R2)

        e2R2 = x2 + radius2 * math.cos(theta)
        f2R2 = y2 + radius2 * math.sin(theta)
        Xt2R2 = (e2R2, f2R2)

        mycanvas.create_line(Xt1R1, Xt2R1, fill='red')
        mycanvas.create_line(Xt1R2, Xt2R2, fill='red')
    
        x1 = x2
        y1 = y2


bg_color = '#00AE4E'

# The Application
class Application(Tk):
    def __init__(self):
        """Constructeur de l'application"""
        Tk.__init__(self)
        self.start()

    # Fonction de départ
    def start(self):
        # Création et packing du frame pour le texte et le bouton
        self.myframe = Frame(self, bg=bg_color)
        self.myframe.pack(expand=YES)

        # Création et packing du texte et du bouton
        self.label = Label(self.myframe, text="Bienvenue sur TrackMania\nReloaded", font=("calibri", 40), bg=bg_color, fg='white')
        self.bouton = Button(self.myframe, text="Appuyez pour commencer ...", font=("calibri", 25), bg='white', fg=bg_color, command=self.trackmaker)
        self.label.pack()
        self.bouton.pack(pady=50)

    # Fonction principale pour fabriquer le circuit
    def trackmaker(self):
        global mycanvas  
        # Suppression du frame contenant le bouton et le texte
        self.myframe.pack_forget()
        
        # Création et packing du canvas
        mycanvas = ResizingCanvas(self, width=850, height=400, bg=bg_color, highlightthickness=0)
        mycanvas.pack(fill=BOTH, expand=YES)

        # Actions sur le canvas
        mycanvas.bind('<Button-1>', display_coordinates)
        mycanvas.bind('<Button-3>', draw_track)


if __name__ == "__main__":
    app = Application()

    # Personnalisation de la fenêtre
    app.title("TrackMania Reloaded")
    app.geometry("720x480")
    app.minsize(640, 360)
    app.iconbitmap("img/logo.ico")
    app.config(background=bg_color)

    # Afficher
    app.mainloop()