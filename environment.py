"""
Contient toute la logique de simulation de l'environnement.
"""

import random

import pygame


class Meteo:
    """Classe qui gère la météo du jeu (effet et visuel compris)."""

    def __init__(self, display): ...

    def soleil(self): ...

    def pluie(self): ...

    def orage(self): ...

    def neige(self): ...


class Saisons:
    """Classe qui gère les saisons du jeu (effet et visuel compris)."""

    def __init__(self, display): ...

    def printemps(self): ...

    def ete(self): ...

    def automne(self): ...

    def hiver(self): ...
