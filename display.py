# Projet : Vivaria
# Auteurs : Benjamin MICHALAK, Angel SANCHEZ, Augustin MINOT

"""
Gère l'affichage graphique.
"""

from random import randint

import pygame

import config
import ecosystem
from ecosystem import Carnivores, Herbivores, Plantes


class Display:
    """Class Display qui sert à faire fonctionner toutes les interactions entre les êtres vivants"""

    def __init__(self):
        self.is_playing = False
        self.tous_plantes = pygame.sprite.Group()
        self.tous_herbivores = pygame.sprite.Group()
        self.tous_carnivores = pygame.sprite.Group()
        self.temps_echelle = 1
        self.pause = True

    def demarrage(self, screen, temps):
        """Méthode démarrage qui sert à démarrer la simulation créant les êtres vivants"""
        self.is_playing = True
        self.pause = False
        # méthodes de spawn des êtres vivants à créer
        self.apparaitre_plante(
            Plantes(
                self,
                "Pissenlit",
                randint(0, config.LARGEUR),
                randint(0, config.HAUTEUR),
                screen,
                temps
            )
        )
        self.apparaitre_herbivore(
            Herbivores(
                self,
                "Vache",
                randint(0, config.LARGEUR),
                randint(0, config.HAUTEUR),
                screen,
                temps
            )
        )
        self.apparaitre_carnivore(
            Carnivores(
                self,
                "Loup",
                randint(0, config.LARGEUR),
                randint(0, config.HAUTEUR),
                screen,
                temps
            )
        )

    def mise_a_jour(self, screen):
        """Méthode qui met à jour l'écran et permet l'affichage et les déplacements des êtres vivants"""
        if self.pause:
            return
        
        for herbivore in self.tous_herbivores:
            # créer déplacements des herbivores
            herbivore.move()
            herbivore.grow()
        for carnivore in self.tous_carnivores:
            # créer déplacements des carnivores
            carnivore.move()
            carnivore.grow()
        for plante in self.tous_plantes:
            plante.grow()

        for _ in range(self.temps_echelle):
            self.temps += 1

        self.tous_plantes.draw(screen)
        self.tous_herbivores.draw(screen)
        self.tous_carnivores.draw(screen)

    def verifier_collision(self, sprite, group):
        return pygame.sprite.spritecollide(
            sprite, group, False, None
        )  # mettre pygame.sprite.collide_mask à la place de None quand les sprites seront ajoutés

    def apparaitre_plante(self, plantes_class):
        self.tous_plantes.add(plantes_class)

    def apparaitre_herbivore(self, herbivores_class):
        self.tous_herbivores.add(herbivores_class)

    def apparaitre_carnivore(self, carnivores_class):
        self.tous_carnivores.add(carnivores_class)
