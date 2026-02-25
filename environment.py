# Projet : Vivaria
# Auteurs : Benjamin MICHALAK, Angel SANCHEZ, Augustin MINOT

"""
Contient toute la logique de simulation de l'environnement.
"""

import pygame

import ecosystem

# Les classes suivantes définissent les différents environnements du jeu :
# - Biomes : influence la croissance des plantes et les caractéristiques des animaux selon le type de terrain
# - Meteo : influence la croissance des plantes selon la météo courante
# - Saisons : influence la croissance des plantes selon la saison courante

# Ajouter les effets de bases des différentes classes
...


class Biomes:
    """Classe qui gère les biomes du jeu (effet et visuel compris)."""

    def __init__(self, display):
        self.display = display
        self.etat = "plaine"  # État courant du biome

    def plaine(self):
        # Définit le biome courant comme une plaine
        self.etat = "plaine"

    def foret(self):
        # Définit le biome courant comme une forêt
        self.etat = "foret"

    def desert(self):
        # Définit le biome courant comme un désert
        self.etat = "desert"

    def toundra(self):
        # Définit le biome courant comme une toundra
        self.etat = "toundra"

    def multiplicateur_plante(self):
        # Retourne un multiplicateur de croissance pour les plantes selon le biome
        if self.etat == "foret":
            return 1.2
        elif self.etat == "desert":
            return 0.5
        elif self.etat == "toundra":
            return 0.8
        return 1

    def multiplicateur_vitesse_animaux(self):
        # Retourne un multiplicateur de vitesse pour les animaux selon le biome
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
        # Retourne un multiplicateur de coût énergétique pour les animaux selon le biome
        if self.etat == "desert":
            return 1.2
        return 1


class Meteo:
    """Classe qui gère la météo du jeu (effet et visuel compris)."""

    def __init__(self, display):
        self.display = display
        self.etat = "soleil"  # État courant de la météo

    def soleil(self):
        # Définit la météo sur "soleil"
        self.etat = "soleil"

    def pluie(self):
        # Définit la météo sur "pluie"
        self.etat = "pluie"

    def orage(self):
        # Définit la météo sur "orage"
        self.etat = "orage"

    def neige(self):
        # Définit la météo sur "neige"
        self.etat = "neige"

    def multiplicateur_plante(self):
        # Retourne un multiplicateur de croissance pour les plantes selon la météo
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
        self.etat = "printemps"  # Saison courante

    def printemps(self):
        # Définit la saison sur "printemps"
        self.etat = "printemps"

    def ete(self):
        # Définit la saison sur "été"
        self.etat = "ete"

    def automne(self):
        # Définit la saison sur "automne"
        self.etat = "automne"

    def hiver(self):
        # Définit la saison sur "hiver"
        self.etat = "hiver"

    def multiplicateur_plante(self):
        # Retourne un multiplicateur de croissance pour les plantes selon la saison
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

    - Les plantes voient leur croissance modifiée par les trois facteurs.
    - Les animaux voient leur vitesse et leur coût énergétique modifiés par le biome.
    """
    # --- Application des multiplicateurs sur les plantes ---
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

    # --- Application des multiplicateurs sur les herbivores ---
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

    # --- Application des multiplicateurs sur les carnivores ---
    for carnivore in display.tous_carnivores:
        if hasattr(carnivore, "appliquer_multiplicateurs"):
            carnivore.appliquer_multiplicateurs(
                mult_biome_vitesse=mult_biome_vitesse, mult_biome_cout=mult_biome_cout
            )
