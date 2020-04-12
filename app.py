# coding: utf-8

"""TrackManiaReloaded : by el famoso Killian Monnier

TrackManiaReloaded est un jeu bien connu des pilotes.

Usage: python app.py
-
-
-
-

"""

# Importation de tkinter
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

# Dessine des lignes entre chaque click de la souris
def draw_track(event):
    global mycanvas, firstClick, x1, y1
    perimeter = 75
    radius = perimeter / 2
    
    if firstClick:
        # Récupération des coordonnées de la souris
        x1 = event.x
        y1 = event.y

        # Création du cercle
        xyP1 = x1-perimeter, y1-perimeter, x1+perimeter, y1+perimeter
        mycanvas.create_oval(xyP1)

        xyR1 = x1-radius, y1-radius, x1+radius, y1+radius
        mycanvas.create_oval(xyR1)

        firstClick = False
        
    else:
        # Récupération des coordonnées de la souris
        x2 = event.x
        y2 = event.y

        # Création du cercle
        xyP2 = x2-perimeter, y2-perimeter, x2+perimeter, y2+perimeter
        mycanvas.create_oval(xyP2)

        xyR2 = x2-radius, y2-radius, x2+radius, y2+radius
        mycanvas.create_oval(xyR2)

        """Création de la route"""
        # Distance Euclidienne entre deux cercles
        distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        
        
        # Création de l'angle
        #mycanvas.create_arc(xy, start=0, extent=360, fill="red")

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
    app.iconbitmap("logo.ico")
    app.config(background=bg_color)

    # Afficher
    app.mainloop()