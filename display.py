# Projet : Vivaria
# Auteurs : Benjamin MICHALAK, Angel SANCHEZ, Augustin MINOT

"""
Gère l'affichage graphique.
"""

from random import randint

import pygame
from math import *

import config
import ecosystem
from ecosystem import Carnivores, Herbivores, Plantes


class Display:
    """Class Display qui sert à faire fonctionner toutes les interactions entre les êtres vivants"""

    def __init__(self, screen):
        self.is_playing = False
        self.tous_herbivores = pygame.sprite.Group()
        self.tous_carnivores = pygame.sprite.Group()
        self.temps_echelle = 1

    def demarrage(self, screen, temps):
        """Méthode démarrage qui sert à démarrer la simulation créant les êtres vivants"""
        self.plante = Plantes(
                self,
                "Pissenlit",
                randint(0, config.LARGEUR),
                randint(0, config.HAUTEUR),
                screen,
                temps
            )
        self.herbivore = Herbivores(
                self,
                "Vache",
                randint(0, config.LARGEUR),
                randint(0, config.HAUTEUR),
                screen,
                temps,
                "data/img/Herbivore2_plaine.png"
            )
        self.carnivore = Carnivores(
                self,
                "Loup",
                randint(0, config.LARGEUR),
                randint(0, config.HAUTEUR),
                screen,
                temps
            )
        self.tous_plantes = pygame.sprite.Group()
        self.is_playing = True
        # méthodes de spawn des êtres vivants à créer
        self.apparaitre_plante(self.plante)
        self.apparaitre_herbivore(self.herbivore)
        self.apparaitre_carnivore(self.carnivore)

    def mise_a_jour(self, screen):
        """Méthode qui met à jour l'écran et permet l'affichage et les déplacements des êtres vivants"""
        if not self.is_playing:
            return
        else:
            screen.blit(self.herbivore.image, self.herbivore.rect)
            for carnivore in self.tous_carnivores:
                if carnivore.x < 0 or carnivore.x > screen.get_width() or carnivore.y < 0 or carnivore.y > screen.get_height():
                    carnivore.bordure()
                else:
                    proies_detectees = []
                    distance_proies = []
                    for herbivore in self.tous_herbivores:
                        distance = carnivore.calcul_distance_proie((herbivore.x, herbivore.y))
                        if distance <= carnivore.rayon_vision:
                            proies_detectees.append(herbivore)
                            distance_proies.append(distance)
                    if proies_detectees == []:
                        carnivore.changer_direction([-5, 0, 5])
                    else:
                        proie_la_plus_proche = min(distance_proies)
                        indice_proie = distance_proies.index(proie_la_plus_proche)
                        proie_cible = proies_detectees[indice_proie]
                        angle_cible = carnivore.calcul_angle_proie((proie_cible.x, proie_cible.y))
                        carnivore.ciblage_proie(angle_cible)
                carnivore.move()
                carnivore.grow()

            for herbivore in self.tous_herbivores:
                marge = 20
                au_bord = (herbivore.x < marge or herbivore.x > screen.get_width() - marge or
                           herbivore.y < marge or herbivore.y > screen.get_height() - marge)
                if au_bord:
                    herbivore.bordure()
                else:
                    predateurs_detectes = []
                    distance_predateurs = []
                    for carnivore in self.tous_carnivores:
                        distance = herbivore.calcul_distance_predateur((carnivore.x, carnivore.y))
                        if distance <= herbivore.rayon_vision:
                            predateurs_detectes.append(carnivore)
                            distance_predateurs.append(distance)
                    if predateurs_detectes == []:
                        for herbivore in self.tous_herbivores:
                            proies_detectees = []
                            distance_proies = []
                            for plante in self.tous_plantes:
                                distance = herbivore.calcul_distance_proie((plante.x, plante.y))
                                if distance <= herbivore.rayon_vision:
                                    proies_detectees.append(plante)
                                    distance_proies.append(distance)
                            if proies_detectees == []:
                                herbivore.changer_direction([-5, 0, 5])
                            else:
                                proie_la_plus_proche = min(distance_proies)
                                indice_proie = distance_proies.index(proie_la_plus_proche)
                                proie_cible = proies_detectees[indice_proie]
                                angle_cible = herbivore.calcul_angle_proie((proie_cible.x, proie_cible.y))
                                herbivore.ciblage_proie(angle_cible)
                    else:
                        predateur_le_plus_proche = min(distance_predateurs)
                        indice_predateur = distance_predateurs.index(predateur_le_plus_proche)
                        predateur_danger = predateurs_detectes[indice_predateur]
                        angle_danger = herbivore.calcul_angle_predateur((predateur_danger.x, predateur_danger.y))
                        herbivore.fuite(angle_danger)
                herbivore.move()
                herbivore.grow()

            for plante in self.tous_plantes:
                plante.grow()

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
