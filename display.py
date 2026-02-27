# Projet : Vivaria
# Auteurs : Benjamin MICHALAK, Angel SANCHEZ, Augustin MINOT

"""
Gère l'affichage graphique.
"""

from random import choice, randint

import pygame

import config
from ecosystem import Carnivores, Herbivores, Plantes
from environment import Biomes, Meteo, Saisons


class Display:
    """Class Display qui sert à faire fonctionner toutes les interactions entre les êtres vivants"""

    def __init__(self, screen):
        # Indique si la simulation est en cours
        self.is_playing = False
        # Indique si la simulation est en pause
        self.pause = False
        # Groupes de sprites pour chaque type d'entité
        self.tous_plantes = pygame.sprite.Group()
        self.tous_herbivores = pygame.sprite.Group()
        self.tous_carnivores = pygame.sprite.Group()
        # Échelle de temps pour la simulation (non utilisé directement ici)
        self.temps_echelle = 1
        # Indique si la simulation a déjà démarré au moins une fois
        self.start = False
        # Compteurs d'entités pour l'affichage
        self.nb_plantes = 0
        self.nb_herbivores = 0
        self.nb_carnivores = 0
        # Biome courant (modifie les comportements et apparences)
        self.biome = Biomes(self)
        self.saison = Saisons(self)

    def demarrage(self, screen, temps, nb_entites):
        """
        Méthode démarrage qui sert à démarrer la simulation en créant les êtres vivants.
        Le type d'entité et son apparence dépendent du biome courant.
        """
        self.start = True
        for _ in range(nb_entites):
            # Sélection aléatoire du type d'entité à faire apparaître
            self.spawn_entite = choice(["plante", "herbivore", "carnivore"])
            if self.spawn_entite == "plante":
                # Sélectionne l'image de la plante selon le biome (à améliorer pour plus de variété)
                if self.biome.etat == "plaine":
                    if self.saison.etat == "printemps":
                        self.type_plante = choice(["Fleur", "Buisson"])
                        if self.type_plante == "Fleur":
                            self.plante_image = "data/img/FleurPrintemps_Plaine.png"
                        else:
                            self.plante_image = "data/img/PlantePrintemps_plaine.png"
                    elif self.saison.etat == "ete":
                        self.type_plante = "Buisson"
                        self.plante_image = "data/img/PlanteEte_plaine.png"
                    elif self.saison.etat == "automne":
                        self.type_plante = "Buisson"
                        self.plante_image = "data/img/PlanteAutomne_plaine.png"
                    elif self.saison.etat == "hiver":
                        self.type_plante = "Buisson"
                        self.plante_image = "data/img/PlanteHiver_plaine.png"
                elif self.biome.etat == "foret":
                    self.type_plante = "Buisson"
                    if self.saison.etat == "printemps":
                        self.plante_image = "data/img/PlantePrintemps_Foret.png"
                    elif self.saison.etat == "ete":
                        self.plante_image = "data/img/PlanteEte_Foret.png"
                    elif self.saison.etat == "automne":
                        self.plante_image = "data/img/PlanteAutomne_Foret.png"
                    elif self.saison.etat == "hiver":
                        self.plante_image = "data/img/PlanteHiver_Foret.png"
                elif self.biome.etat == "desert":
                    self.type_plante = "Cactus"
                    if self.saison.etat == "printemps":
                        self.plante_image = "data/img/PlantePrintemps_Desert.png"
                    elif self.saison.etat == "ete":
                        self.plante_image = "data/img/PlanteEte_Desert.png"
                    elif self.saison.etat == "automne":
                        self.plante_image = "data/img/PlanteAutomne_Desert.png"
                    elif self.saison.etat == "hiver":
                        self.plante_image = "data/img/PlanteHiver_Desert.png"
                elif self.biome.etat == "toundra":
                    self.type_plante = "Buisson"
                    if self.saison.etat == "printemps":
                        self.plante_image = "data/img/PlantePrintemps_Toundra.png"
                    elif self.saison.etat == "ete":
                        self.plante_image = "data/img/PlanteEte_Toundra.png"
                    elif self.saison.etat == "automne":
                        self.plante_image = "data/img/PlanteAutomne_Toundra.png"
                    elif self.saison.etat == "hiver":
                        self.plante_image = "data/img/PlanteHiver_Toundra.png"
                # Création et ajout de la plante
                self.plante = Plantes(
                    self,
                    self.type_plante,
                    randint(0, config.LARGEUR),
                    randint(0, config.HAUTEUR),
                    screen,
                    temps,
                    self.plante_image,
                )
                self.apparaitre_plante(self.plante)
                self.nb_plantes += 1
            elif self.spawn_entite == "herbivore":
                # Sélectionne l'image de l'herbivore selon le biome
                if self.biome.etat == "plaine":
                    self.type_herbivore = choice(["Poule", "Vache"])
                    if self.type_herbivore == "Poule":
                        self.herbivore_image = "data/img/Herbivore_plaine.png"
                    elif self.type_herbivore == "Vache":
                        self.herbivore_image = "data/img/Herbivore2_plaine.png"
                elif self.biome.etat == "foret":
                    self.type_herbivore = "Sanglier"
                    self.herbivore_image = "data/img/Herbivore_foret.png"
                elif self.biome.etat == "desert":
                    self.type_herbivore = "Chameau"
                    self.herbivore_image = "data/img/Herbivore_desert.png"
                elif self.biome.etat == "toundra":
                    self.type_herbivore = "Cerf"
                    self.herbivore_image = "data/img/Herbivore_toundra.png"
                # Création et ajout de l'herbivore
                self.herbivore = Herbivores(
                    self,
                    self.type_herbivore,
                    randint(0, config.LARGEUR),
                    randint(0, config.HAUTEUR),
                    screen,
                    temps,
                    self.herbivore_image,
                )
                self.apparaitre_herbivore(self.herbivore)
                self.nb_herbivores += 1
            elif self.spawn_entite == "carnivore":
                # Sélectionne l'image du carnivore selon le biome
                if self.biome.etat == "plaine":
                    self.type_carnivore = "Renard"
                    self.carnivore_image = "data/img/Predateur_plaine.png"
                elif self.biome.etat == "foret":
                    self.type_carnivore = "Ours"
                    self.carnivore_image = "data/img/Predateur_foret.png"
                elif self.biome.etat == "desert":
                    self.type_carnivore = "Fennec"
                    self.carnivore_image = "data/img/Predateur_desert.png"
                elif self.biome.etat == "toundra":
                    self.type_carnivore = "Loup"
                    self.carnivore_image = "data/img/Predateur_toundra.png"
                # Création et ajout du carnivore
                self.carnivore = Carnivores(
                    self,
                    self.type_carnivore,
                    randint(0, config.LARGEUR),
                    randint(0, config.HAUTEUR),
                    screen,
                    temps,
                    self.carnivore_image,
                )
                self.apparaitre_carnivore(self.carnivore)
                self.nb_carnivores += 1
        # Démarre la simulation
        self.is_playing = True
        self.pause = False

    def mise_a_jour(self, screen):
        """
        Met à jour l'écran et permet l'affichage et les déplacements des êtres vivants.
        Gère la logique de poursuite, fuite, et bordures pour chaque entité.
        """
        if not self.is_playing:
            return
        elif self.pause:
            pass
        else:
            # --- Gestion des carnivores ---
            for carnivore in self.tous_carnivores:
                # Si le carnivore sort de l'écran, il rebondit sur le bord
                if (
                    carnivore.x < 0
                    or carnivore.x > screen.get_width()
                    or carnivore.y < 0
                    or carnivore.y > screen.get_height()
                ):
                    carnivore.bordure()
                else:
                    # Recherche des proies (herbivores) dans le rayon de vision
                    proies_detectees = []
                    distance_proies = []
                    for herbivore in self.tous_herbivores:
                        distance = carnivore.calcul_distance_proie(
                            (herbivore.x, herbivore.y)
                        )
                        if distance <= carnivore.rayon_vision:
                            proies_detectees.append(herbivore)
                            distance_proies.append(distance)
                    if proies_detectees == []:
                        # Si aucune proie détectée, le carnivore change de direction aléatoirement
                        carnivore.changer_direction([-5, 0, 5])
                    else:
                        # Sinon, il cible la proie la plus proche
                        proie_la_plus_proche = min(distance_proies)
                        indice_proie = distance_proies.index(proie_la_plus_proche)
                        proie_cible = proies_detectees[indice_proie]
                        angle_cible = carnivore.calcul_angle_proie(
                            (proie_cible.x, proie_cible.y)
                        )
                        carnivore.ciblage_proie(angle_cible)
                carnivore.move()
                carnivore.grow()

            # --- Gestion des herbivores ---
            for herbivore in self.tous_herbivores:
                marge = 20
                # Détection de la proximité des bords de l'écran
                au_bord = (
                    herbivore.x < marge
                    or herbivore.x > screen.get_width() - marge
                    or herbivore.y < marge
                    or herbivore.y > screen.get_height() - marge
                )
                if au_bord:
                    herbivore.bordure()
                else:
                    # Recherche de prédateurs (carnivores) dans le rayon de vision
                    predateurs_detectes = []
                    distance_predateurs = []
                    for carnivore in self.tous_carnivores:
                        distance = herbivore.calcul_distance_predateur(
                            (carnivore.x, carnivore.y)
                        )
                        if distance <= herbivore.rayon_vision:
                            predateurs_detectes.append(carnivore)
                            distance_predateurs.append(distance)
                    if predateurs_detectes == []:
                        # Si aucun prédateur détecté, recherche de plantes à manger
                        for herbivore in self.tous_herbivores:
                            proies_detectees = []
                            distance_proies = []
                            for plante in self.tous_plantes:
                                distance = herbivore.calcul_distance_proie(
                                    (plante.x, plante.y)
                                )
                                if distance <= herbivore.rayon_vision:
                                    proies_detectees.append(plante)
                                    distance_proies.append(distance)
                            if proies_detectees == []:
                                # Si aucune plante détectée, déplacement aléatoire
                                herbivore.changer_direction([-5, 0, 5])
                            else:
                                # Sinon, cible la plante la plus proche
                                proie_la_plus_proche = min(distance_proies)
                                indice_proie = distance_proies.index(
                                    proie_la_plus_proche
                                )
                                proie_cible = proies_detectees[indice_proie]
                                angle_cible = herbivore.calcul_angle_proie(
                                    (proie_cible.x, proie_cible.y)
                                )
                                herbivore.ciblage_proie(angle_cible)
                    else:
                        # Si un prédateur est détecté, fuite dans la direction opposée
                        predateur_le_plus_proche = min(distance_predateurs)
                        indice_predateur = distance_predateurs.index(
                            predateur_le_plus_proche
                        )
                        predateur_danger = predateurs_detectes[indice_predateur]
                        angle_danger = herbivore.calcul_angle_predateur(
                            (predateur_danger.x, predateur_danger.y)
                        )
                        herbivore.fuite(angle_danger)
                herbivore.move()
                herbivore.grow()

            # --- Gestion des plantes ---
            for plante in self.tous_plantes:
                plante.grow()

            # Affichage de tous les sprites sur l'écran
            self.tous_plantes.draw(screen)
            self.tous_herbivores.draw(screen)
            self.tous_carnivores.draw(screen)

    def reinitialiser(self):
        """
        Réinitialise la simulation en supprimant toutes les entités et en réinitialisant les compteurs.
        """
        for plante in self.tous_plantes:
            self.tous_plantes.remove(plante)
        for herbivore in self.tous_herbivores:
            self.tous_herbivores.remove(herbivore)
        for carnivore in self.tous_carnivores:
            self.tous_carnivores.remove(carnivore)
        self.nb_plantes = 0
        self.nb_herbivores = 0
        self.nb_carnivores = 0
        self.start = False

    def verifier_collision(self, sprite, group):
        """
        Vérifie s'il y a collision (avec masque) entre un sprite et un groupe de sprites.
        Retourne la liste des collisions.
        """
        return pygame.sprite.spritecollide(
            sprite, group, False, pygame.sprite.collide_mask
        )

    def apparaitre_plante(self, plantes_class):
        """
        Ajoute une plante au groupe de sprites correspondant.
        """
        self.tous_plantes.add(plantes_class)

    def apparaitre_herbivore(self, herbivores_class):
        """
        Ajoute un herbivore au groupe de sprites correspondant.
        """
        self.tous_herbivores.add(herbivores_class)

    def apparaitre_carnivore(self, carnivores_class):
        """
        Ajoute un carnivore au groupe de sprites correspondant.
        """
        self.tous_carnivores.add(carnivores_class)
