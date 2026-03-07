# Projet : Vivaria
# Auteurs : Benjamin MICHALAK, Angel SANCHEZ, Augustin MINOT

"""
Gère les traçages de graphiques
"""

import config
import sys
import pygame
import matplotlib.pyplot as plt

def creer_figure():
    fig, ax = plt.subplots(1, 1, figsize=(config.LARGEUR/100, config.HAUTEUR/100), dpi=100)
    return fig, ax

def update_graphique(display):
    display.ax.clear()
    display.ax.plot(display.liste_jours, display.historique_plantes, color="red")
    display.ax.plot(display.liste_jours, display.historique_herbivores, color="blue")
    display.ax.plot(display.liste_jours, display.historique_carnivores, color="green")
    display.ax.set_xlim(min(display.liste_jours), max(display.liste_jours) + 1)
    display.ax.set_ylim(0, 40)
    display.ax.set_title(f"Evolution du nombres d'êtres vivants dans l'environnement {display.biome.etat} en fonction du temps")
    display.ax.set_xlabel("Temps (en heures)")
    display.ax.set_ylabel("Nombres d'individus")
    display.fig.canvas.draw()
    pixel_brut = display.fig.canvas.tostring_argb()
    taille = display.fig.canvas.get_width_height()
    display.surface_graphique = pygame.image.frombuffer(pixel_brut, taille, "ARGB")
