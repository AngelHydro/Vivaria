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

    def multiplicateur_plante(self):
        if self.etat == "foret":
            return 1.2
        elif self.etat == "desert":
            return 0.5
        elif self.etat == "toundra":
            return 0.8
        return 1

    def multiplicateur_vitesse_animaux(self):
        if self.etat == "plaine":
            return 1.1
        elif self.etat == "foret":
            return 0.9
        elif self.etat == "desert":
            return 1
        elif self.etat == "toundra":
            return 1
        return 1

    def multiplicateur_cout_energie_animaux(self):
        if self.etat == "desert":
            return 1.2
        return 1


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

    def multiplicateur_plante(self):
        if self.etat == "pluie":
            return 1.5
        elif self.etat == "orage":
            return 0.8
        elif self.etat == "neige":
            return 0.5
        return 1


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

    def multiplicateur_plante(self):
        if self.etat == "printemps":
            return 1.5
        elif self.etat == "automne":
            return 0.8
        elif self.etat == "hiver":
            return 0.5
        return 1


def appliquer_effets_environnement(display, biome, meteo, saison):
    """
    Applique les multiplicateurs cumulés de biome, météo et saison
    sur les entités du display (plantes, herbivores, carnivores).
    À appeler à chaque frame ou à chaque changement d'état environnemental.
    """
    # Plantes
    mult_biome_plante = biome.multiplicateur_plante()
    mult_meteo_plante = meteo.multiplicateur_plante()
    mult_saison_plante = saison.multiplicateur_plante()
    for plante in display.tous_plantes:
        if hasattr(plante, "appliquer_multiplicateurs"):
            plante.appliquer_multiplicateurs(
                mult_biome=mult_biome_plante,
                mult_meteo=mult_meteo_plante,
                mult_saison=mult_saison_plante,
            )

    # Herbivores
    mult_biome_vitesse = (
        biome.multiplicateur_vitesse_animaux()
        if hasattr(biome, "multiplicateur_vitesse_animaux")
        else 1
    )
    mult_biome_cout = (
        biome.multiplicateur_cout_energie_animaux()
        if hasattr(biome, "multiplicateur_cout_energie_animaux")
        else 1
    )
    for herbivore in display.tous_herbivores:
        if hasattr(herbivore, "appliquer_multiplicateurs"):
            herbivore.appliquer_multiplicateurs(
                mult_biome_vitesse=mult_biome_vitesse, mult_biome_cout=mult_biome_cout
            )

    # Carnivores
    for carnivore in display.tous_carnivores:
        if hasattr(carnivore, "appliquer_multiplicateurs"):
            carnivore.appliquer_multiplicateurs(
                mult_biome_vitesse=mult_biome_vitesse, mult_biome_cout=mult_biome_cout
            )
