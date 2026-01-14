"""
Contient toute la logique de simulation de l'environnement.
"""

import pygame

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
            ...
        elif self.etat == "foret":
            ...
        elif self.etat == "desert":
            ...
        elif self.etat == "toundra":
            ...


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
            ...
        elif self.etat == "pluie":
            ...
        elif self.etat == "orage":
            ...
        elif self.etat == "neige":
            ...


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
            ...
        elif self.etat == "ete":
            ...
        elif self.etat == "automne":
            ...
        elif self.etat == "hiver":
            ...
