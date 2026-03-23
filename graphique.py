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
    # création des courbes
    display.ax.clear()
    display.ax.plot(display.liste_jours, display.historique_plantes, color="green")
    display.ax.plot(display.liste_jours, display.historique_herbivores, color="blue")
    display.ax.plot(display.liste_jours, display.historique_carnivores, color="red")
    display.ax.set_xlim(min(display.liste_jours), max(display.liste_jours) + 1)
    display.ax.set_ylim(0, 40)
    # création des légendes des courbes
    for historique, couleur, label in [
        (display.historique_plantes, "green", "Plantes"),
        (display.historique_herbivores, "blue", "Herbivores"),
        (display.historique_carnivores, "red", "Carnivores"),
    ]:
        display.ax.plot(display.liste_jours, historique, color=couleur, label=label)
    display.ax.legend(loc="upper right")
    # création du titre, de la légende des abscisses et de la légende des ordonnées
    display.ax.set_title(f"Evolution du nombres d'êtres vivants dans l'environnement {display.biome.etat} en fonction du temps")
    display.ax.set_xlabel("Temps (en heures)")
    display.ax.set_ylabel("Nombres d'individus")
    display.fig.canvas.draw()
    pixel_brut = display.fig.canvas.tostring_argb()
    taille = display.fig.canvas.get_width_height()
    display.surface_graphique = pygame.image.frombuffer(pixel_brut, taille, "ARGB")
