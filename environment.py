# Projet : Vivaria
# Auteurs : Benjamin MICHALAK, Angel SANCHEZ, Augustin MINOT

"""
Contient toute la logique de simulation de l'environnement.
"""

import pygame

import ecosystem

# Ajouter les effets de bases des différentes classes
...


class Biomes:
    """Classe qui gère les biomes du jeu (effet et visuel compris)."""

    def __init__(self, display):
        self.display = display
        self.etat = "plaine"

    def plaine(self):
        self.etat = "plaine"

    def foret(self):
        self.etat = "foret"

    def desert(self):
        self.etat = "desert"

    def toundra(self):
        self.etat = "toundra"

    def effets(self):
        if self.etat == "plaine":
            for herbivore in self.display.tous_herbivores:
                herbivore.multiplicateur_vitesse(1.1)
            for carnivore in self.display.tous_carnivores:
                carnivore.multiplicateur_vitesse(1.1)
        elif self.etat == "foret":
            for plante in self.display.tous_plantes:
                plante.multiplicateur_grow(1.2)
            for herbivore in self.display.tous_herbivores:
                herbivore.multiplicateur_vitesse(0.9)
            for carnivore in self.display.tous_carnivores:
                carnivore.multiplicateur_vitesse(0.9)
        elif self.etat == "desert":
            for plante in self.display.tous_plantes:
                plante.multiplicateur_grow(0.5)
            for herbivore in self.display.tous_herbivores:
                herbivore.multiplicateur_energy(1.2)
            for carnivore in self.display.tous_carnivores:
                carnivore.multiplicateur_energy(1.2)
        elif self.etat == "toundra":
            for plante in self.display.tous_plantes:
                plante.multiplicateur_grow(0.8)


class Meteo:
    """Classe qui gère la météo du jeu (effet et visuel compris)."""

    def __init__(self, display):
        self.display = display
        self.etat = "soleil"

    def soleil(self):
        self.etat = "soleil"

    def pluie(self):
        self.etat = "pluie"

    def orage(self):
        self.etat = "orage"

    def neige(self):
        self.etat = "neige"

    def effets(self):
        if self.etat == "soleil":
            for plante in self.display.tous_plantes:
                self.croissance = 1
        elif self.etat == "pluie":
            for plante in self.display.tous_plantes:
                plante.multiplicateur_grow(1.5)
        elif self.etat == "orage":
            for plante in self.display.tous_plantes:
                plante.multiplicateur_grow(0.8)
        elif self.etat == "neige":
            for plante in self.display.tous_plantes:
                plante.multiplicateur_grow(0.5)


class Saisons:
    """Classe qui gère les saisons du jeu (effet et visuel compris)."""

    def __init__(self, display):
        self.display = display
        self.etat = "printemps"

    def printemps(self):
        self.etat = "printemps"

    def ete(self):
        self.etat = "ete"

    def automne(self):
        self.etat = "automne"

    def hiver(self):
        self.etat = "hiver"

    def effets(self):
        if self.etat == "printemps":
            for plante in self.display.tous_plantes:
                plante.multiplicateur_grow(1.5)
        elif self.etat == "et":
            for plante in self.display.tous_plantes:
                self.croissance = 1
        elif self.etat == "automne":
            for plante in self.display.tous_plantes:
                plante.multiplicateur_grow(0.8)
        elif self.etat == "hiver":
            for plante in self.display.tous_plantes:
                plante.multiplicateur_grow(0.5)
