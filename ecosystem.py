# Projet : Vivaria
# Auteurs : Benjamin MICHALAK, Angel SANCHEZ, Augustin MINOT

"""
Contient toute la logique de simulation de l'écosystème.
"""

import math
import random

import pygame

# Si dist n'existe pas dans la bibliothèque math, on la crée
if not hasattr(math, "dist"):
    def dist(p, q):
        return math.sqrt(sum((px - qx) ** 2 for px, qx in zip(p, q)))
else:
    from math import dist


class Plantes(pygame.sprite.Sprite):
    """Classe représentant les plantes dans l'écosystème."""

    def __init__(self, display, name, x, y, screen, temps, img):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.age = 1
        self.display = display
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.croissance_base = 1  # valeur de base
        self.croissance = self.croissance_base

    def appliquer_multiplicateurs(self, mult_biome=1, mult_meteo=1, mult_saison=1):
        self.croissance = self.croissance_base * mult_biome * mult_meteo * mult_saison

    def multiplicateur_grow(self, multiplicateur):
        """Multiplie la vitesse de croissance de la plante (déprécié, utiliser appliquer_multiplicateurs)."""
        self.croissance = self.croissance * multiplicateur

    def die(self):
        self.kill()

    def grow(self):
        # Utilise le multiplicateur de croissance si défini, sinon croissance normale
        if hasattr(self, 'croissance'):
            self.age += self.croissance
        else:
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

    def __init__(self, display, name, x, y, screen, temps, img):
        super().__init__()
        self.screen = screen
        self.display = display
        self.x = x
        self.y = y
        self.age = 1
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.energy = 100
        self.direction = 0
        self.vitesse_base = 1.0
        self.vitesse = self.vitesse_base
        self.cout_energy_base = 0.1
        self.cout_energy = self.cout_energy_base
        self.rayon_vision = 100

    def appliquer_multiplicateurs(self, mult_biome_vitesse=1, mult_biome_cout=1):
        self.vitesse = self.vitesse_base * mult_biome_vitesse
        self.cout_energy = self.cout_energy_base * mult_biome_cout

    def multiplicateur_vitesse(self, vitesse):
        self.vitesse = self.vitesse * vitesse

    def multiplicateur_energy(self, energy):
        self.cout_energy += self.cout_energy * energy

    def die(self):
        self.kill()

    def grow(self):
        self.age +=
        self.energy -= self.cout_energy
        self.check_life()
        if self.display.verifier_collision(
            self, self.display.tous_plantes
        ):  # Si plante sur la position de herbivore
            self.eat()
        if self.display.verifier_collision(self, self.display.tous_carnivores):
            self.die()

    def check_life(self):  # Les herbivores vivent 30 ans
        if self.age > 10950 or self.energy <= 0:
            self.die()

    def calcul_distance_proie(self, position_proie):
        return dist((self.x, self.y), position_proie)

    def calcul_angle_proie(self, position_proie):
        self.delta_x = position_proie[0] - self.x
        self.delta_y = position_proie[1] - self.y
        return math.degrees(math.atan2(self.delta_y, self.delta_x))

    def ciblage_proie(self, angle):
        self.direction = angle

    def calcul_distance_predateur(self, position_predateur):
        return dist((self.x, self.y), position_predateur)

    def calcul_angle_predateur(self, position_predateur):
        self.delta_x = position_predateur[0] - self.x
        self.delta_y = position_predateur[1] - self.y
        return math.degrees(math.atan2(self.delta_y, self.delta_x))

    def fuite(self, angle):
        self.direction = -angle

    def changer_direction(self, var_direction):
        self.direction += random.choice(var_direction)

    def bordure(self):
        if self.x < 0 or self.x > self.screen.get_width():
            self.direction = 180 - self.direction
            self.changer_direction([-20, 20])
        elif self.y < 0 or self.y > self.screen.get_height():
            self.direction = -self.direction
            self.changer_direction([-20, 20])

    def move(self):  # Se déplace aléatoirement en fonction de sa vitesse
        self.x += math.cos(math.radians(self.direction)) * self.vitesse
        self.y += math.sin(math.radians(self.direction)) * self.vitesse
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def eat(self):
        if self.hunger < 100:
            # self.energy += 10
            self.hunger -= 10


class Carnivores(pygame.sprite.Sprite):
    """Classe représentant les carnivores dans l'écosystème."""

    def __init__(self, display, name, x, y, screen, temps, img):
        super().__init__()
        self.screen = screen
        self.display = display
        self.x = x
        self.y = y
        self.age = 1
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.energy = 100
        self.direction = 0
        self.vitesse_base = 1.0
        self.vitesse = self.vitesse_base
        self.cout_energy_base = 0.001
        self.cout_energy = self.cout_energy_base
        self.rayon_vision = 100

    def appliquer_multiplicateurs(self, mult_biome_vitesse=1, mult_biome_cout=1):
        self.vitesse = self.vitesse_base * mult_biome_vitesse
        self.cout_energy = self.cout_energy_base * mult_biome_cout

    def multiplicateur_vitesse(self, vitesse):
        self.vitesse = self.vitesse * vitesse

    def multiplicateur_energy(self, energy):
        self.cout_energy += self.cout_energy * energy

    def grow(self):
        self.age += 0.001
        self.energy -= self.cout_energy
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
        return math.degrees(math.atan2(self.delta_y, self.delta_x))

    def ciblage_proie(self, angle):
        self.direction = angle

    def changer_direction(self, var_direction):
        self.direction += random.choice(var_direction)

    def bordure(self):
        if self.x < 0 or self.x > self.screen.get_width():
            self.direction = 180 - self.direction
        elif self.y < 0 or self.y > self.screen.get_height():
            self.direction = -self.direction

    def move(self):  # Se déplace aléatoirement en fonction de sa vitesse
        self.x += math.cos(math.radians(self.direction)) * self.vitesse
        self.y += math.sin(math.radians(self.direction)) * self.vitesse
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def eat(self):
        if self.hunger < 100:
            # self.energy += 10
            self.hunger -= 10
