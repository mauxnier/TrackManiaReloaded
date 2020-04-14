# coding: utf-8

"""TrackManiaReloaded : by el famoso Killian Monnier

TrackManiaReloaded est un jeu bien connu des pilotes.

Usage: python app.py
-
-
-
-

"""

bg_color = 'yellow'

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

# Calcul Theta en radians
def calculate_theta(xa, ya, xb, yb, radius1, radius2):
    # Distance Euclidienne entre deux cercles : D
    #mycanvas.create_line(xa, ya, xb, yb)
    distanceAB = math.sqrt((xa-xb)**2 + (ya-yb)**2)
    D = distanceAB
    #print("D =", D)

    # H
    #mycanvas.create_line(xa, ya-radius2, xb, yb)
    H = math.sqrt(D**2 - (radius1-radius2)**2)
    #print("H =", H)

    # X = H
    #mycanvas.create_line(xa, ya-radius1, xb, yb-radius3)
    X = H
    #print("X =", X)

    # Y
    #mycanvas.create_line(xa, ya-radius1, xb, yb)
    Y = math.sqrt(H**2 + radius2**2)
    #print("Y =", Y)

    # Theta en radians : Law of Cosines
    theta = math.acos((radius1**2 + D**2 - Y**2) / (2 * radius1 * D))
    theta = theta + math.atan2(yb - ya, xb - xa)
    print("Theta =", theta)

    return theta

# Définition des variables globales
firstClick = True
thirdClick = False
mycanvas = None
x1 = 0
y1 = 0
x2 = 0
y2 = 0

# Dessine des lignes entre chaque click de la souris
def draw_track(event):
    global mycanvas, firstClick, thirdClick, x1, y1, x2, y2
    radius1 = 100
    radius2 = radius1 / 2
    radius3 = radius1-radius2

    """Création de la route : https://gieseanw.wordpress.com/2012/09/12/finding-external-tangent-points-for-two-circles/"""

    if firstClick:
        # Récupération des coordonnées de la souris
        x1 = event.x
        y1 = event.y

        # Création du cercle
        xyR1 = x1-radius1, y1-radius1, x1+radius1, y1+radius1
        mycanvas.create_oval(xyR1)

        xyR2 = x1-radius2, y1-radius2, x1+radius2, y1+radius2
        mycanvas.create_oval(xyR2)

        firstClick = False
        
    else:
        if not thirdClick:
            # Récupération des coordonnées de la souris
            x2 = event.x
            y2 = event.y

            # Création du cercle
            xyR1 = x2-radius1, y2-radius1, x2+radius1, y2+radius1
            mycanvas.create_oval(xyR1)

            xyR3 = x2-radius3, y2-radius3, x2+radius3, y2+radius3
            mycanvas.create_oval(xyR3)

            # Appel de la fonction pour calculer theta
            theta = calculate_theta(x1, y1, x2, y2, radius1, radius2)

            # Xt : Point de la tangente externe
            e1R1 = x1 - radius1 * math.cos(theta)
            f1R1 = y1 - radius1 * math.sin(theta)
            Xt1R1 = (e1R1, f1R1)

            e2R1 = x2 - radius1 * math.cos(theta)
            f2R1 = y2 - radius1 * math.sin(theta)
            Xt2R1 = (e2R1, f2R1)

            e1R2 = x1 - radius2 * math.cos(theta)
            f1R2 = y1 - radius2 * math.sin(theta)
            Xt1R2 = (e1R2, f1R2)

            e2R2 = x2 - radius2 * math.cos(theta)
            f2R2 = y2 - radius2 * math.sin(theta)
            Xt2R2 = (e2R2, f2R2)

            #print("Xt1R1 =", Xt1R1, "Xt2R1 =", Xt2R1, "Xt1R2 =", Xt1R2, "Xt2R2 =", Xt2R2)
            mycanvas.create_line(Xt1R1, Xt2R1, fill='green')
            mycanvas.create_line(Xt1R2, Xt2R2, fill='green')

        if thirdClick:
            # Récupération des coordonnées de la souris
            x3 = event.x
            y3 = event.y

            # Création du cercle
            xyR1 = x3-radius1, y3-radius1, x3+radius1, y3+radius1
            mycanvas.create_oval(xyR1)

            xyR3 = x3-radius3, y3-radius3, x3+radius3, y3+radius3
            mycanvas.create_oval(xyR3)

            # Distance Euclidienne entre deux cercles : D
            #mycanvas.create_line(x2, y2, x3, y3)
            distanceAB = math.sqrt((x1-x2)**2 + (y1-y2)**2)
            distanceBC = math.sqrt((x2-x3)**2 + (y2-y3)**2)
            distanceAC = math.sqrt((x1-x3)**2 + (y1-y3)**2)
            print(distanceAB, distanceBC, distanceAC)
            # Calcul de l'angle ABC aka angleDiff en degrés: Law of Cosines
            angleDiff = math.acos((distanceAB**2 + distanceBC**2 - distanceAC**2) / (2 * distanceAB * distanceBC)) * 180 / math.pi
            print("angleDiff =", angleDiff)
            
            # Appel de la fonction pour calculer theta
            theta = calculate_theta(x2, y2, x3, y3, radius1, radius2)

            if angleDiff < 90:
                # Yt : Point de la tangente interne
                g2R1 = x2 - radius1 * math.cos(theta)
                h2R1 = y2 - radius1 * math.sin(theta)
                Yt2R1 = (g2R1, h2R1)

                g3R1 = x3 + radius1 * math.cos(theta)
                h3R1 = y3 + radius1 * math.sin(theta)
                Yt3R1 = (g3R1, h3R1)

                g2R2 = x2 - radius2 * math.cos(theta)
                h2R2 = y2 - radius2 * math.sin(theta)
                Yt2R2 = (g2R2, h2R2)

                g3R2 = x3 + radius2 * math.cos(theta)
                h3R2 = y3 + radius2 * math.sin(theta)
                Yt3R2 = (g3R2, h3R2)
            
                #print("Yt2R1 =", Yt2R1, "Yt3R1 =", Yt3R1, "Yt2R2 =", Yt2R2, "Yt3R2 =", Yt3R2)
                mycanvas.create_line(Yt2R1, Yt3R2, fill='blue')
                mycanvas.create_line(Yt2R2, Yt3R1, fill='blue')
            
            else:
                # Xt : Point de la tangente externe
                e2R1 = x2 - radius1 * math.cos(theta)
                f2R1 = y2 - radius1 * math.sin(theta)
                Xt2R1 = (e2R1, f2R1)

                e3R1 = x3 - radius1 * math.cos(theta)
                f3R1 = y3 - radius1 * math.sin(theta)
                Xt3R1 = (e3R1, f3R1)

                e2R2 = x2 - radius2 * math.cos(theta)
                f2R2 = y2 - radius2 * math.sin(theta)
                Xt2R2 = (e2R2, f2R2)

                e3R2 = x3 - radius2 * math.cos(theta)
                f3R2 = y3 - radius2 * math.sin(theta)
                Xt3R2 = (e3R2, f3R2)

                #print("Xt2R1 =", Xt2R1, "Xt3R1 =", Xt3R1, "Xt2R2 =", Xt2R2, "Xt3R2 =", Xt3R2)
                mycanvas.create_line(Xt2R1, Xt3R1, fill='red')
                mycanvas.create_line(Xt2R2, Xt3R2, fill='red')

            # Décalage des valeurs pour le prochain point
            x1 = x2
            y1 = y2
            x2 = x3
            y2 = y3

        thirdClick = True

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