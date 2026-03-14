# Projet : Vivaria
# Auteurs : Benjamin MICHALAK, Angel SANCHEZ, Augustin MINOT

"""
Contient toute la logique de simulation de l'écosystème.
"""

import math
import random

import pygame

import config


# Fonction dist compatible avec tous les Python et le typage statique.
# Utilise math.dist si disponible, sinon une version manuelle.
def dist(p, q):
    if hasattr(math, "dist"):
        return math.dist(p, q)
    else:
        return math.sqrt(sum((px - qx) ** 2 for px, qx in zip(p, q)))


class Plantes(pygame.sprite.Sprite):
    """Classe représentant les plantes dans l'écosystème."""

    def __init__(self, display, name, x, y, screen, temps, img):
        super().__init__()
        self.screen = screen
        self.name = name
        self.x = x
        self.y = y
        self.age = 1  # Âge de la plante (en "jours" de simulation)
        self.display = display
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, config.TAILLE_SPRITE)
        self.rect = self.image.get_rect()
        self.croissance_base = 1
        self.croissance = self.croissance_base
        self.rect.x = self.x
        self.rect.y = self.y

    def appliquer_multiplicateurs(self, mult_biome=1, mult_meteo=1, mult_saison=1):
        # Applique les multiplicateurs de croissance liés au biome, à la météo et à la saison
        self.croissance = self.croissance_base * mult_biome * mult_meteo * mult_saison

    def multiplicateur_grow(self, multiplicateur):
        """Multiplie la vitesse de croissance de la plante (déprécié, utiliser appliquer_multiplicateurs)."""
        self.croissance = self.croissance * multiplicateur

    def die(self):
        # Supprime la plante de la simulation et décrémente le compteur global
        self.display.nb_plantes -= 1
        self.kill()

    def grow(self):
        # Vieillit la plante selon sa vitesse de croissance
        if hasattr(self, "croissance"):
            self.age += self.croissance
        else:
            self.age += 1
        self.check_life()

    def check_life(self):  # Les plantes vivent 100 ans
        # Si la plante a dépassé son espérance de vie, elle meurt
        if self.age > 36500:
            self.die()
        # Si un herbivore est en collision avec la plante, elle est mangée (meurt)
        if self.display.verifier_collision(self, self.display.tous_herbivores):
            self.die()


class Herbivores(pygame.sprite.Sprite):
    """Classe représentant les herbivores dans l'écosystème."""

    def __init__(self, display, name, x, y, screen, temps, img):
        super().__init__()
        self.screen = screen
        self.display = display
        self.name = name
        self.x = x
        self.y = y
        self.age = 1  # Âge de l'herbivore
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.energy = (
            config.ENERGIE_MAX_HERBIVORE
        )  # Énergie de l'herbivore (diminue à chaque déplacement)
        self.direction = 0  # Direction actuelle (en degrés)
        self.vitesse_base = config.VITESSE_HERBIVORE  # Vitesse de base
        self.vitesse = self.vitesse_base
        self.cout_energy_base = (
            config.COUT_ENERGY_HERBIVORE
        )  # Coût énergétique de base par déplacement
        self.rayon_vision = (
            config.RAYON_VISION_HERBIVORE
        )  # Rayon de vision pour détecter proies/prédateurs
        self.rect.x = self.x
        self.rect.y = self.y

    def appliquer_multiplicateurs(self, mult_biome_vitesse=1, mult_biome_cout=1):
        # Applique les multiplicateurs de vitesse et de coût énergétique selon le biome
        self.vitesse = self.vitesse_base * mult_biome_vitesse
        self.cout_energy = self.cout_energy_base * mult_biome_cout

    def multiplicateur_vitesse(self, vitesse):
        # Multiplie la vitesse actuelle par un facteur
        self.vitesse = self.vitesse * vitesse

    def multiplicateur_energy(self, energy):
        # Augmente le coût énergétique par un facteur
        self.cout_energy += self.cout_energy * energy

    def die(self):
        # Supprime l'herbivore de la simulation et décrémente le compteur global
        self.display.nb_herbivores -= 1
        self.kill()

    def grow(self):
        # Vieillit l'herbivore et réduit son énergie à chaque "tick"
        self.age += config.CROISSANCE  # à ajuster selon l'échelle de temps souhaitée
        self.energy -= self.cout_energy
        self.check_life()
        # Si un carnivore est en collision avec l'herbivore, il meurt (prédation)
        if self.display.verifier_collision(self, self.display.tous_carnivores):
            self.die()
        # Si une plante est en collision avec l'herbivore, il la mange et gagne de l'énergie
        plante_mangee = self.display.verifier_collision(self, self.display.tous_plantes)
        if plante_mangee:
            self.energy += (
                config.ENERGIE_RECHARGE
            )  # Valeur à ajuster selon l'équilibrage souhaité
            if self.energy > config.ENERGIE_MAX_HERBIVORE:
                self.energy = config.ENERGIE_MAX_HERBIVORE  # Limite l'énergie maximale

    def check_life(self):  # Les herbivores vivent 30 ans
        # Meurt si l'âge ou l'énergie tombe à zéro
        if self.age > 10950 or self.energy <= 0:
            self.die()

    def calcul_distance_proie(self, position_proie):
        # Calcule la distance à une proie (plante ou autre)
        return dist((self.x, self.y), position_proie)

    def calcul_angle_proie(self, position_proie):
        # Calcule l'angle vers une proie pour cibler sa direction
        self.delta_x = position_proie[0] - self.x
        self.delta_y = position_proie[1] - self.y
        return math.degrees(math.atan2(self.delta_y, self.delta_x))

    def ciblage_proie(self, angle):
        # Oriente l'herbivore vers la proie
        self.direction = angle

    def calcul_distance_predateur(self, position_predateur):
        # Calcule la distance à un prédateur
        return dist((self.x, self.y), position_predateur)

    def calcul_angle_predateur(self, position_predateur):
        # Calcule l'angle vers un prédateur pour fuir dans la direction opposée
        self.delta_x = position_predateur[0] - self.x
        self.delta_y = position_predateur[1] - self.y
        return math.degrees(math.atan2(self.delta_y, self.delta_x))

    def fuite(self, angle):
        # Fait fuir l'herbivore dans la direction opposée à celle du prédateur
        self.direction = (angle + 180) % 360

    def changer_direction(self, var_direction):
        # Change la direction de l'herbivore de façon aléatoire parmi les valeurs proposées
        self.direction += random.choice(var_direction)

    def bordure(self):
        # Si l'herbivore atteint le bord de l'écran, il rebondit et change légèrement de direction
        if self.x < 0 or self.x > self.screen.get_width():
            self.direction = 180 - self.direction
            self.changer_direction([-20, 20])
        elif self.y < 0 or self.y > self.screen.get_height():
            self.direction = -self.direction
            self.changer_direction([-20, 20])

    def move(self):  # Se déplace aléatoirement en fonction de sa vitesse
        # Met à jour la position de l'herbivore selon sa direction et sa vitesse
        self.x += math.cos(math.radians(self.direction)) * self.vitesse
        self.y += math.sin(math.radians(self.direction)) * self.vitesse
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)


class Carnivores(pygame.sprite.Sprite):
    """Classe représentant les carnivores dans l'écosystème."""

    def __init__(self, display, name, x, y, screen, temps, img):
        super().__init__()
        self.screen = screen
        self.display = display
        self.name = name
        self.x = x
        self.y = y
        self.age = 1  # Âge du carnivore
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.energy = config.ENERGIE_MAX_CARNIVORE  # Énergie du carnivore
        self.direction = 0  # Direction actuelle (en degrés)
        self.vitesse_base = config.VITESSE_CARNIVORE  # Vitesse de base
        self.vitesse = self.vitesse_base
        self.cout_energy_base = (
            config.COUT_ENERGY_CARNIVORE
        )  # Coût énergétique de base par déplacement
        self.cout_energy = self.cout_energy_base
        self.rayon_vision = (
            config.RAYON_VISION_CARNIVORE
        )  # Rayon de vision pour détecter les proies
        self.rect.x = self.x
        self.rect.y = self.y

    def appliquer_multiplicateurs(self, mult_biome_vitesse=1, mult_biome_cout=1):
        # Applique les multiplicateurs de vitesse et de coût énergétique selon le biome
        self.vitesse = self.vitesse_base * mult_biome_vitesse
        self.cout_energy = self.cout_energy_base * mult_biome_cout

    def multiplicateur_vitesse(self, vitesse):
        # Multiplie la vitesse actuelle par un facteur
        self.vitesse = self.vitesse * vitesse

    def multiplicateur_energy(self, energy):
        # Augmente le coût énergétique par un facteur
        self.cout_energy += self.cout_energy * energy

    def grow(self):
        # Vieillit le carnivore et réduit son énergie à chaque "tick"
        self.age += config.CROISSANCE
        self.energy -= self.cout_energy
        self.check_life()
        # Si un herbivore est en collision avec le carnivore, il le mange et gagne de l'énergie
        herbivore_mange = self.display.verifier_collision(
            self, self.display.tous_herbivores
        )
        if herbivore_mange:
            self.energy += (
                config.ENERGIE_RECHARGE
            )  # Valeur à ajuster selon l'équilibrage souhaité
            if self.energy > config.ENERGIE_MAX_CARNIVORE:
                self.energy = config.ENERGIE_MAX_CARNIVORE  # Limite l'énergie maximale

    def die(self):
        # Supprime le carnivore de la simulation et décrémente le compteur global
        self.display.nb_carnivores -= 1
        self.kill()

    def check_life(self):  # Les carnivores vivent 15 ans
        # Meurt si l'âge ou l'énergie tombe à zéro
        if self.age > 5475 or self.energy <= 0:
            self.die()

    def calcul_distance_proie(self, position_proie):
        # Calcule la distance à une proie (herbivore)
        return dist((self.x, self.y), position_proie)

    def calcul_angle_proie(self, position_proie):
        # Calcule l'angle vers une proie pour cibler sa direction
        self.delta_x = position_proie[0] - self.x
        self.delta_y = position_proie[1] - self.y
        return math.degrees(math.atan2(self.delta_y, self.delta_x))

    def ciblage_proie(self, angle):
        # Oriente le carnivore vers la proie
        self.direction = angle

    def changer_direction(self, var_direction):
        # Change la direction du carnivore de façon aléatoire parmi les valeurs proposées
        self.direction += random.choice(var_direction)

    def bordure(self):
        # Si le carnivore atteint le bord de l'écran, il rebondit
        if self.x < 0 or self.x > self.screen.get_width():
            self.direction = 180 - self.direction
        elif self.y < 0 or self.y > self.screen.get_height():
            self.direction = -self.direction

    def move(self):  # Se déplace aléatoirement en fonction de sa vitesse
        # Met à jour la position du carnivore selon sa direction et sa vitesse
        self.x += math.cos(math.radians(self.direction)) * self.vitesse
        self.y += math.sin(math.radians(self.direction)) * self.vitesse
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
