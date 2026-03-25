# Projet : Vivaria
# Auteurs : Benjamin MICHALAK, Angel SANCHEZ, Augustin MINOT

"""
Gère l'importation des images de pluie, de neige et d'orage
"""

import pygame
import os

import config

def charger_image(chemin):
    liste_images = []
    liste_fichiers = os.listdir(chemin)
    liste_fichiers = sorted(liste_fichiers)
    for fichier in liste_fichiers:
        if fichier.endswith(".png"):
            chemin_img = os.path.join(chemin, fichier)
            image = pygame.image.load(chemin_img)
            image.convert_alpha()
            liste_images.append(image)
    return liste_images
