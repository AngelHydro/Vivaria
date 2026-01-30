# Projet : Vivaria
# Auteurs : Benjamin MICHALAK, Angel SANCHEZ, Augustin MINOT

"""
Contient toute la logique de simulation de l'écosystème.
"""

import random

import pygame
from math import *


class Plantes(pygame.sprite.Sprite):
    """Classe représentant les plantes dans l'écosystème."""

    def __init__(self, display, name, x, y, screen, temps):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.age = 0
        self.display = display
        img = pygame.Surface((10, 10))
        pygame.draw.rect(
            img,
            (255, 255, 0),
            [self.x, self.y, 10, 10],  # à remplacer plus tard par une image
        )
        self.image = img
        self.rect = pygame.Rect(
            self.x, self.y, 10, 10
        )  # à changer en self.image.get_rect() quand il y aura une image

    def die(self):
        self.kill()

    def grow(self):
        self.age += 1
        self.check_life()

    def check_life(self):  # Les plantes vivent 100 ans
        if self.age > 36500:
            self.die()
        if self.display.verifier_collision(
            self, self.display.tous_herbivores
        ):  # Si plante sur la position de herbivore
            self.die()


class Herbivores(pygame.sprite.Sprite):
    """Classe représentant les herbivores dans l'écosystème."""

    def __init__(self, display, name, x, y, screen, temps):
        super().__init__()
        self.screen = screen
        self.display = display
        self.x = x
        self.y = y
        self.age = 0
        img = pygame.Surface((5, 5))
        pygame.draw.circle(
            img, (255, 0, 0), (self.x, self.y), 5
        )  # à remplacer plus tard par une image
        self.image = img
        self.image.fill((255, 0, 0))
        self.rect = pygame.Rect(
            self.x - 5, self.y - 5, 5 * 2, 5 * 2
        )  # à changer en self.image.get_rect() quand il y aura une image
        self.energy = 100
        self.hunger = 0
        self.direction = 0
        self.vitesse = 1.5
        #self.energy_coutee_par_frame = 0.25
        #self.energy_coutee_par_deplacement = 0.25
        self.hunger_coutee_par_frame = 0.25
        self.hunger_coutee_par_deplacement = 0.25
        self.rayon_vision = 100

    def die(self):
        self.kill()

    def grow(self):
        self.age += 0.001
        #self.energy -= self.energy_coutee_par_frame
        #self.energy -= self.energy_coutee_par_deplacement
        self.hunger -= self.hunger_coutee_par_frame
        self.hunger -= self.hunger_coutee_par_deplacement
        self.check_life()
        if self.display.verifier_collision(
            self, self.display.tous_plantes
        ):  # Si plante sur la position de herbivore
            self.eat()
        if self.display.verifier_collision(
            self, self.display.tous_carnivores
        ):
            self.die()

    def check_life(self):  # Les herbivores vivent 30 ans
        if self.age > 10950 or self.energy <= 0:
            self.die()

    def calcul_distance_proie(self, position_proie):
        return dist((self.x, self.y), position_proie)

    def calcul_angle_proie(self, position_proie):
        self.delta_x = position_proie[0] - self.x
        self.delta_y = position_proie[1] - self.y
        return degrees(atan2(self.delta_y, self.delta_x))

    def ciblage_proie(self, angle):
        self.direction = angle

    def calcul_distance_predateur(self, position_predateur):
        return dist((self.x, self.y), position_predateur)

    def calcul_angle_predateur(self, position_predateur):
        self.delta_x = position_predateur[0] - self.x
        self.delta_y = position_predateur[1] - self.y
        return degrees(atan2(self.delta_y, self.delta_x))

    def fuite(self, angle):
        self.direction = - angle

    def changer_direction(self, var_direction):
        self.direction += random.choice(var_direction)

    def bordure(self):
        if self.x < 0 or self.x > self.screen.get_width():
            self.direction = 180 - self.direction
            self.changer_direction([-20, 20])
        elif self.y < 0 or self.y > self.screen.get_height():
           self.direction = - self.direction
           self.changer_direction([-20, 20])

    def move(self):  # Se déplace aléatoirement en fonction de sa vitesse
        self.x += cos(radians(self.direction)) * self.vitesse
        self.y += sin(radians(self.direction)) * self.vitesse
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def eat(self):
        if self.hunger < 100:
            #self.energy += 10
            self.hunger -= 10


class Carnivores(pygame.sprite.Sprite):
    """Classe représentant les carnivores dans l'écosystème."""

    def __init__(self, display, name, x, y, screen, temps):
        super().__init__()
        self.screen = screen
        self.display = display
        self.x = x
        self.y = y
        self.age = 0
        img = pygame.Surface((5, 5))
        pygame.draw.circle(
            img, (0, 0, 255), (self.x, self.y), 5
        )  # à remplacer plus tard par une image
        self.image = img
        self.image.fill((0, 0, 255))
        self.rect = pygame.Rect(
            self.x - 5, self.y - 5, 5 * 2, 5 * 2
        )  # à changer en self.image.get_rect() quand il y aura une image
        self.energy = 100
        self.hunger = 0
        self.direction = 0
        self.vitesse = 1.5
        #self.energy_coutee_par_frame = 0.25
        #self.energy_coutee_par_deplacement = 0.25
        self.hunger_coutee_par_frame = 0.25
        self.hunger_coutee_par_deplacement = 0.25
        self.rayon_vision = 100

    def grow(self):
        self.age += 0.001
        #self.energy -= self.energy_coutee_par_frame
        #self.energy -= self.energy_coutee_par_deplacement
        self.hunger -= self.hunger_coutee_par_frame
        self.hunger -= self.hunger_coutee_par_deplacement
        self.check_life()
        if self.display.verifier_collision(
            self, self.display.tous_herbivores
        ):  # Si herbivore sur la position de carnivore
            self.eat()

    def die(self):
        self.kill()

    def check_life(self):  # Les carnivores vivent 15 ans
        if self.age > 5475 or self.energy <= 0:
            self.die()

    def calcul_distance_proie(self, position_proie):
        return dist((self.x, self.y), position_proie)

    def calcul_angle_proie(self, position_proie):
        self.delta_x = position_proie[0] - self.x
        self.delta_y = position_proie[1] - self.y
        return degrees(atan2(self.delta_y, self.delta_x))

    def ciblage_proie(self, angle):
        self.direction = angle

    def changer_direction(self, var_direction):
        self.direction += random.choice(var_direction)

    def bordure(self):
        if self.x < 0 or self.x > self.screen.get_width():
            self.direction = 180 - self.direction
        elif self.y < 0 or self.y > self.screen.get_height():
           self.direction = - self.direction

    def move(self):  # Se déplace aléatoirement en fonction de sa vitesse
        self.x += cos(radians(self.direction)) * self.vitesse
        self.y += sin(radians(self.direction)) * self.vitesse
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)


    def eat(self):
        if self.hunger < 100:
            #self.energy += 10
            self.hunger -= 10
