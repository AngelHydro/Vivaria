"""
Gère l'affichage graphique.
"""

import pygame

from ecosystem import Carnivores, Herbivores, Plantes


class Display:
    """Class Display qui sert à faire fonctionner toutes les interactions entre les êtres vivants"""

    def __init__(self):
        self.is_playing = False
        self.tous_plantes = pygame.sprite.Group()
        self.tous_herbivores = pygame.sprite.Group()
        self.tous_carnivores = pygame.sprite.Group()
        self.temps = 0
        self.temps_echelle = 1
        self.pause = True

    def demarrage(self):
        """Méthode démarrage qui sert à démarrer la simulation créant les êtres vivants"""
        self.is_playing = True
        # méthodes de spawn des êtres vivants à créer
        self.apparaitre_plante(Plantes)
        self.apparaitre_herbivore(Herbivores)
        self.apparaitre_carnivore(Carnivores)

    def mise_a_jour(self, screen):
        """Méthode qui met à jour l'écran et permet l'affichage et les déplacements des êtres vivants"""
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

        if self.pause:
            return

        for _ in range(self.temps_echelle):
            self.temps += 1

        self.tous_plantes.draw(screen)
        self.tous_herbivores.draw(screen)
        self.tous_carnivores.draw(screen)

    def verifier_collision(self, sprite, group):
        return pygame.sprite.spritecollide(
            sprite, group, False, pygame.sprite.collide_mask
        )

    def apparaitre_plante(self, plantes_class_name):
        self.tous_plantes.add(plantes_class_name.__call__(self))

    def apparaitre_herbivore(self, herbivores_class_name):
        self.tous_herbivores.add(herbivores_class_name.__call__(self))

    def apparaitre_carnivore(self, carnivores_class_name):
        self.tous_carnivores.add(carnivores_class_name.__call__(self))
