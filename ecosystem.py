"""
Contient toute la logique de simulation.
"""

import random

import pygame


class Plantes(pygame.sprite.Sprite):
    """Classe représentant les plantes dans l'écosystème."""

    def __init__(self, name, x, y):
        super().__init__(name)
        self.x = x
        self.y = y
        self.age = 0

    def grow(self):
        self.age += 1

    def die(self):  # Les plantes vivent 100 ans
        if self.age > 36500:
            self.remove()


class Herbivores(pygame.sprite.Sprite):
    """Classe représentant les herbivores dans l'écosystème."""

    def __init__(self, display, name, x, y):
        super().__init__(name)
        self.display = display
        self.x = x
        self.y = y
        self.age = 0
        self.energy = 100
        self.hunger = 0
        self.vitesse = 1
        self.energie_coutee_par_frame = 0.5
        self.energie_coutee_par_deplacement = 0.1

    def grow(self):
        self.age += 0.001
        self.energie -= self.energie_coutee_par_frame
        self.energie -= self.energie_coutee_par_deplacement
        if self.energie <= 75:
            self.hunger += 25
        self.die()
        if self.display.verifier_collision(
            self, self.display.tous_plantes
        ):  # Si plante sur la position de herbivore
            self.eat()

    def die(self):  # Les plantes vivent 30 ans
        if self.age > 10950 or self.energie <= 0:
            self.remove()

    def move(self):  # Se déplace aléatoirement en fonction de sa vitesse
        self.x += random.randint(-1, 1) * self.vitesse
        self.y += random.randint(-1, 1) * self.vitesse

    def eat(self):
        if self.hunger > 100:
            self.energy += 10
            self.hunger -= 10


class Carnivores(pygame.sprite.Sprite):
    """Classe représentant les carnivores dans l'écosystème."""

    def __init__(self, display, name, x, y):
        super().__init__(name)
        self.display = display
        self.x = x
        self.y = y
        self.age = 0
        self.energy = 100
        self.hunger = 0
        self.vitesse = 1
        self.energie_coutee_par_frame = 0.5
        self.energie_coutee_par_deplacement = 0.1

    def grow(self):
        self.age += 0.001
        self.energie -= self.energie_coutee_par_frame
        self.energie -= self.energie_coutee_par_deplacement
        if self.energie <= 75:
            self.hunger += 25
        self.die()
        if self.display.verifier_collision(
            self, self.display.tous_herbivores
        ):  # Si herbivore sur la position de carnivore
            self.eat()

    def die(self):  # Les plantes vivent 15 ans
        if self.age > 5475 or self.energie <= 0:
            self.remove()

    def move(self):  # Se déplace aléatoirement en fonction de sa vitesse
        self.x += random.randint(-1, 1) * self.vitesse
        self.y += random.randint(-1, 1) * self.vitesse

    def eat(self):
        if self.hunger < 100:
            self.energy += 10
            self.hunger -= 10
