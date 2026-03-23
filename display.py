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
from graphique import *


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
        self.meteo = Meteo(self)
        self.chrono_ms = 0
        self.heures = 0
        self.jours = 0
        # On utilise un timer pour contrôler la fréquence d'apparition
        self.spawn_timer_plante = 0  # Initialisation du timer
        self.spawn_timer_herbivore = 0
        self.spawn_timer_carnivore = 0

        self.chrono_graphique = 0
        self.chrono_graphique_update = 0

        self.historique_plantes = [self.nb_plantes]
        self.historique_herbivores = [self.nb_herbivores]
        self.historique_carnivores = [self.nb_carnivores]
        self.liste_jours = [0]
        self.fig, self.ax = creer_figure()
        self.surface_graphique = None
        self.affichage_graphique = False

        self.vitesse_sim = config.VITESSE_SIMULATION_BASE

        self.dico_images = {
            # Plantes plaine
            "FleurPrintemps_Plaine": pygame.image.load("data/img/FleurPrintemps_Plaine.png"),
            "PlantePrintemps_plaine": pygame.image.load("data/img/PlantePrintemps_plaine.png"),
            "PlanteEte_plaine": pygame.image.load("data/img/PlanteEte_plaine-Grown.png"), # à changer plus tard quand texture créée
            "PlanteAutomne_plaine": pygame.image.load("data/img/PlanteAutomne_plaine-Grown.png"),
            "PlanteHiver_plaine": pygame.image.load("data/img/PlanteHiver_plaine-Grown.png"),
            # Plantes forêt
            "PlantePrintemps_Foret": pygame.image.load("data/img/PlantePrintemps_Foret.png"),
            #"PlanteEte_Foret": pygame.image.load("data/img/PlanteEte_Foret.png"),
            #"PlanteAutomne_Foret": pygame.image.load("data/img/PlanteAutomne_Foret.png"),
            #"PlanteHiver_Foret": pygame.image.load("data/img/PlanteHiver_Foret.png"),
            # Plantes désert
            "PlantePrintemps_Desert": pygame.image.load("data/img/PlantePrintemps_Desert.png"),
            #"PlanteEte_Desert": pygame.image.load("data/img/PlanteEte_Desert.png"),
            #"PlanteAutomne_Desert": pygame.image.load("data/img/PlanteAutomne_Desert.png"),
            #"PlanteHiver_Desert": pygame.image.load("data/img/PlanteHiver_Desert.png"),
            # Plantes toundra
            "PlantePrintemps_Toundra": pygame.image.load("data/img/PlantePrintemps_Toundra.png"),
            "PlanteEte_Toundra": pygame.image.load("data/img/PlanteEte_Toundra.png"),
            "PlanteAutomne_Toundra": pygame.image.load("data/img/PlanteAutomne_Toundra.png"),
            "PlanteHiver_Toundra": pygame.image.load("data/img/PlanteHiver_Toundra.png"),
            # Herbivores
            "Herbivore_plaine": pygame.image.load("data/img/Herbivore_plaine.png"),
            "Herbivore2_plaine": pygame.image.load("data/img/Herbivore2_plaine.png"),
            "Herbivore_foret": pygame.image.load("data/img/Herbivore_foret.png"),
            "Herbivore_desert": pygame.image.load("data/img/Herbivore_desert.png"),
            "Herbivore_toundra": pygame.image.load("data/img/Herbivore_toundra.png"),
            # Carnivores
            "Predateur_plaine": pygame.image.load("data/img/Predateur_plaine.png"),
            "Predateur_foret": pygame.image.load("data/img/Predateur_foret.png"),
            "Predateur_desert": pygame.image.load("data/img/Predateur_desert.png"),
            "Predateur_toundra": pygame.image.load("data/img/Predateur_toundra.png"),
        }

    def demarrage(
        self,
        screen,
        temps,
        nb_initial_plantes,
        nb_initial_herbivores,
        nb_initial_carnivores,
    ):
        """
        Méthode démarrage qui sert à démarrer la simulation en créant les êtres vivants.
        Le type d'entité et son apparence dépendent du biome courant.
        """
        self.start = True
        for _ in range(nb_initial_plantes):
            # Sélectionne l'image de la plante selon le biome (à améliorer pour plus de variété)
            # Textures des plantes de la plaine
            if self.biome.etat == "plaine":
                # Textures des plantes de la plaine au printemps
                if self.saison.etat == "printemps":
                    self.type_plante = choice(["Fleur", "Buisson"])
                    if self.type_plante == "Fleur":
                        self.plante_image = self.dico_images["FleurPrintemps_Plaine"]
                    else:
                        self.plante_image = self.dico_images["PlantePrintemps_plaine"]
                # Textures des plantes de la plaine en été
                elif self.saison.etat == "ete":
                    self.type_plante = "Buisson"
                    self.plante_image = self.dico_images["PlanteEte_plaine"]
                # Textures des plantes de la plaine en automne
                elif self.saison.etat == "automne":
                    self.type_plante = "Buisson"
                    self.plante_image = self.dico_images["PlanteAutomne_plaine"]
                # Textures des plantes de la plaine en hiver
                elif self.saison.etat == "hiver":
                    self.type_plante = "Buisson"
                    self.plante_image = self.dico_images["PlanteHiver_plaine"]

            # Textures des plantes de la forêt
            elif self.biome.etat == "foret":
                self.type_plante = "Buisson"
                # Textures des plantes de la forêt au printemps
                if self.saison.etat == "printemps":
                    self.plante_image = self.dico_images["PlantePrintemps_Foret"]
                # Textures des plantes de la forêt en été
                elif self.saison.etat == "ete":
                    self.plante_image = self.dico_images["PlanteEte_Foret"]
                # Textures des plantes de la forêt en automne
                elif self.saison.etat == "automne":
                    self.plante_image = self.dico_images["PlanteAutomne_Foret"]
                # Textures des plantes de la fôret en hier
                elif self.saison.etat == "hiver":
                    self.plante_image = self.dico_images["PlanteHiver_Foret"]

            # Textures des plantes du désert
            elif self.biome.etat == "desert":
                self.type_plante = "Cactus"
                # Textures des plantes du désert au printemps
                if self.saison.etat == "printemps":
                    self.plante_image = self.dico_images["PlantePrintemps_Desert"]
                # Textures des plantes du désert en été
                elif self.saison.etat == "ete":
                    self.plante_image = self.dico_images["PlanteEte_Desert"]
                # Textures des plantes du désert en automne
                elif self.saison.etat == "automne":
                    self.plante_image = self.dico_images["PlanteAutomne_Desert"]
                # Textures des plantes du désert en hiver
                elif self.saison.etat == "hiver":
                    self.plante_image = self.dico_images["PlanteHiver_Desert"]

            # Textures des plantes de la toundra
            elif self.biome.etat == "toundra":
                self.type_plante = "Buisson"
                # Textures des plantes de la toundra au printemps
                if self.saison.etat == "printemps":
                    self.plante_image = self.dico_images["PlantePrintemps_Toundra"]
                # Textures des plantes de la toundra en été
                elif self.saison.etat == "ete":
                    self.plante_image = self.dico_images["PlanteEte_Toundra"]
                # Textures des plantes de la toundra en automne
                elif self.saison.etat == "automne":
                    self.plante_image = self.dico_images["PlanteAutomne_Toundra"]
                # Textures des plantes de la toundra en hiver
                elif self.saison.etat == "hiver":
                    self.plante_image = self.dico_images["PlanteHiver_Toundra"]
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

        for _ in range(nb_initial_herbivores):
            # Sélectionne l'image de l'herbivore selon le biome (à améliorer pour plus de variété)
            # Textures des herbivores de la plaine
            if self.biome.etat == "plaine":
                self.type_herbivore = choice(["Poule", "Vache"])
                if self.type_herbivore == "Poule":
                    self.herbivore_image = self.dico_images["Herbivore_plaine"]
                elif self.type_herbivore == "Vache":
                    self.herbivore_image = self.dico_images["Herbivore2_plaine"]
            # Textures des herbivores de la forêt
            elif self.biome.etat == "foret":
                self.type_herbivore = "Sanglier"
                self.herbivore_image = self.dico_images["Herbivore_foret"]
            # Textures des herbivores du désert
            elif self.biome.etat == "desert":
                self.type_herbivore = "Chameau"
                self.herbivore_image = self.dico_images["Herbivore_desert"]
            # Textures des herbivores de la toundra
            elif self.biome.etat == "toundra":
                self.type_herbivore = "Cerf"
                self.herbivore_image = self.dico_images["Herbivore_toundra"]
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
        for _ in range(nb_initial_carnivores):
            # Sélectionne l'image du carnivore selon le biome (à améliorer pour plus de variété)
            # Textures des carnivores de la plaine
            if self.biome.etat == "plaine":
                self.type_carnivore = "Renard"
                self.carnivore_image = self.dico_images["Predateur_plaine"]
            # Textures des carnivores de la forêt
            elif self.biome.etat == "foret":
                self.type_carnivore = "Ours"
                self.carnivore_image = self.dico_images["Predateur_foret"]
            # Textures des carnivores du désert
            elif self.biome.etat == "desert":
                self.type_carnivore = "Fennec"
                self.carnivore_image = self.dico_images["Predateur_desert"]
            # Textures des carnivores de la toundra
            elif self.biome.etat == "toundra":
                self.type_carnivore = "Loup"
                self.carnivore_image = self.dico_images["Predateur_toundra"]
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

        self.historique_plantes = [self.nb_plantes]
        self.historique_herbivores = [self.nb_herbivores]
        self.historique_carnivores = [self.nb_carnivores]
        self.liste_jours = [0]
        update_graphique(self)
        # Démarre la simulation
        self.is_playing = True
        self.pause = False
        print("Lancement")

    def creer_grille_spatiale(self, taille_cellule=100):
        """Divise l'écran en grille pour optimiser la détection."""
        grille = {}
        
        # Place chaque entité dans sa cellule
        for plante in self.tous_plantes:
            cell_x = int(plante.x // taille_cellule)
            cell_y = int(plante.y // taille_cellule)
            key = (cell_x, cell_y)
            if key not in grille:
                grille[key] = {'plantes': [], 'herbivores': [], 'carnivores': []}
            grille[key]['plantes'].append(plante)
        
        for herbivore in self.tous_herbivores:
            cell_x = int(herbivore.x // taille_cellule)
            cell_y = int(herbivore.y // taille_cellule)
            key = (cell_x, cell_y)
            if key not in grille:
                grille[key] = {'plantes': [], 'herbivores': [], 'carnivores': []}
            grille[key]['herbivores'].append(herbivore)
        
        for carnivore in self.tous_carnivores:
            cell_x = int(carnivore.x // taille_cellule)
            cell_y = int(carnivore.y // taille_cellule)
            key = (cell_x, cell_y)
            if key not in grille:
                grille[key] = {'plantes': [], 'herbivores': [], 'carnivores': []}
            grille[key]['carnivores'].append(carnivore)
        
        return grille

    def get_voisins(self, grille, cell_x, cell_y, type_entite):
        """Récupère les entités voisines dans un rayon de 1 cellule."""
        voisins = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                key = (cell_x + dx, cell_y + dy)
                if key in grille:
                    voisins.extend(grille[key][type_entite])
        return voisins

    def mise_a_jour(self, screen, temps):
        """
        Met à jour l'écran et permet l'affichage et les déplacements des êtres vivants.
        Gère la logique de poursuite, fuite, et bordures pour chaque entité.
        """
        if not self.is_playing or self.pause:
            return
        else:
            grille = self.creer_grille_spatiale(taille_cellule=100)
            # --- Gestion des carnivores ---
            for carnivore in self.tous_carnivores:
                # Si le carnivore sort de l'écran, il rebondit sur le bord
                if (
                    carnivore.x < 20
                    or carnivore.x > screen.get_width() - 20
                    or carnivore.y < 20
                    or carnivore.y > screen.get_height() - 20
                ):
                    carnivore.bordure()
                else:
                    # Recherche des proies (herbivores) dans le rayon de vision
                    cell_x = int(carnivore.x // 100)
                    cell_y = int(carnivore.y // 100)
                    herbivores_proches = self.get_voisins(grille, cell_x, cell_y, 'herbivores')
                    
                    proies_detectees = []
                    distance_proies = []
                    for herbivore in herbivores_proches:
                        distance = carnivore.calcul_distance_proie(
                            (herbivore.x, herbivore.y)
                        )
                        if distance <= carnivore.rayon_vision ** 2:
                            proies_detectees.append(herbivore)
                            distance_proies.append(distance)
                    if proies_detectees == []:
                        # Si aucune proie détectée, le carnivore change de direction aléatoirement
                        carnivore.changer_direction([-5, 0, 5])
                    else:
                        # Sinon, il cible la proie la plus proche
                        indice_proie = distance_proies.index(min(distance_proies))
                        proie_cible = proies_detectees[indice_proie]
                        angle_cible = carnivore.calcul_angle_proie(
                            (proie_cible.x, proie_cible.y)
                        )
                        carnivore.ciblage_proie(angle_cible)
                carnivore.move()
                carnivore.grow()

            # --- Gestion des herbivores ---
            for herbivore in self.tous_herbivores:
                # Détection de la proximité des bords de l'écran
                au_bord = (
                    herbivore.x < 20
                    or herbivore.x > screen.get_width() - 20
                    or herbivore.y < 20
                    or herbivore.y > screen.get_height() - 20
                )
                if au_bord:
                    herbivore.bordure()
                    herbivore.move()
                    herbivore.grow()
                else:
                    # Recherche de prédateurs (carnivores) dans le rayon de vision
                    cell_x = int(herbivore.x // 100)
                    cell_y = int(herbivore.y // 100)
                    carnivores_proches = self.get_voisins(grille, cell_x, cell_y, 'carnivores')
                    predateurs_detectes = []
                    distance_predateurs = []
                    for carnivore in carnivores_proches:
                        distance = herbivore.calcul_distance_predateur(
                            (carnivore.x, carnivore.y)
                        )
                        if distance <= herbivore.rayon_vision ** 2:
                            predateurs_detectes.append(carnivore)
                            distance_predateurs.append(distance)
                    if predateurs_detectes == []:
                        # Si aucun prédateur détecté, recherche de plantes à manger
                        cell_x = int(herbivore.x // 100)
                        cell_y = int(herbivore.y // 100)
                        plantes_proches = self.get_voisins(grille, cell_x, cell_y, 'plantes')
                        proies_detectees = []
                        distance_proies = []
                        for plante in plantes_proches:
                            distance = herbivore.calcul_distance_proie(
                                (plante.x, plante.y)
                            )
                            if distance <= herbivore.rayon_vision ** 2:
                                proies_detectees.append(plante)
                                distance_proies.append(distance)
                        if proies_detectees == []:
                            # Si aucune plante détectée, déplacement aléatoire
                            herbivore.changer_direction([-5, 0, 5])
                        else:
                            # Sinon, cible la plante la plus proche
                            indice_proie = distance_proies.index(min(distance_proies))
                            proie_cible = proies_detectees[indice_proie]
                            angle_cible = herbivore.calcul_angle_proie(
                                (proie_cible.x, proie_cible.y)
                            )
                            herbivore.ciblage_proie(angle_cible)
                        herbivore.move()
                        herbivore.grow()
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
                        herbivore.changer_direction([-20, -10, 0, 10, 20])
                        herbivore.move()
                        herbivore.grow()

            # --- Gestion des plantes ---
            # --- Apparition périodique de nouvelles entités ---
            self.spawn_timer_plante += 1  # Incrémentation du timer à chaque frame
            self.spawn_timer_herbivore += 1
            self.spawn_timer_carnivore += 1
            if (
                self.spawn_timer_plante >= config.DELAIS_SPAWN_PLANTES
            ):  # Toutes les 5 secondes (à 60 FPS)
                self.spawn_timer_plante = 0  # Réinitialisation du timer
                # On génère entre 1 et 4 nouvelles plantes à chaque apparition
                nb_nouvelles = randint(1, 4)
                for _ in range(nb_nouvelles):
                    # Sélection du type et de l'image de la plante selon le biome et la saison
                    # Apparition de nouvelles plantes selon le biome et la saison, avec des noms de fichiers cohérents
                    # Plantes de la plaine
                    if self.biome.etat == "plaine":
                        # Textures des plantes de la plaine au printemps
                        if self.saison.etat == "printemps":
                            self.type_plante = choice(["Fleur", "Buisson"])
                            if self.type_plante == "Fleur":
                                self.plante_image = self.dico_images["FleurPrintemps_Plaine"]
                            else:
                                self.plante_image = self.dico_images["PlantePrintemps_plaine"]
                        # Textures des plantes de la plaine en été
                        elif self.saison.etat == "ete":
                            self.type_plante = "Buisson"
                            self.plante_image = self.dico_images["PlanteEte_plaine"]
                        # Textures des plantes de la plaine en automne
                        elif self.saison.etat == "automne":
                            self.type_plante = "Buisson"
                            self.plante_image = self.dico_images["PlanteAutomne_plaine"]
                        # Textures des plantes de la plaine en hiver
                        elif self.saison.etat == "hiver":
                            self.type_plante = "Buisson"
                            self.plante_image = self.dico_images["PlanteHiver_plaine"]

                    # Textures des plantes de la forêt
                    elif self.biome.etat == "foret":
                        self.type_plante = "Buisson"
                        # Textures des plantes de la forêt au printemps
                        if self.saison.etat == "printemps":
                            self.plante_image = self.dico_images["PlantePrintemps_Foret"]
                        # Textures des plantes de la forêt en été
                        elif self.saison.etat == "ete":
                            self.plante_image = self.dico_images["PlanteEte_Foret"]
                        # Textures des plantes de la forêt en automne
                        elif self.saison.etat == "automne":
                            self.plante_image = self.dico_images["PlanteAutomne_Foret"]
                        # Textures des plantes de la fôret en hier
                        elif self.saison.etat == "hiver":
                            self.plante_image = self.dico_images["PlanteHiver_Foret"]

                    # Textures des plantes du désert
                    elif self.biome.etat == "desert":
                        self.type_plante = "Cactus"
                        # Textures des plantes du désert au printemps
                        if self.saison.etat == "printemps":
                            self.plante_image = self.dico_images["PlantePrintemps_Desert"]
                        # Textures des plantes du désert en été
                        elif self.saison.etat == "ete":
                            self.plante_image = self.dico_images["PlanteEte_Desert"]
                        # Textures des plantes du désert en automne
                        elif self.saison.etat == "automne":
                            self.plante_image = self.dico_images["PlanteAutomne_Desert"]
                        # Textures des plantes du désert en hiver
                        elif self.saison.etat == "hiver":
                            self.plante_image = self.dico_images["PlanteHiver_Desert"]

                    # Textures des plantes de la toundra
                    elif self.biome.etat == "toundra":
                        self.type_plante = "Buisson"
                        # Textures des plantes de la toundra au printemps
                        if self.saison.etat == "printemps":
                            self.plante_image = self.dico_images["PlantePrintemps_Toundra"]
                        # Textures des plantes de la toundra en été
                        elif self.saison.etat == "ete":
                            self.plante_image = self.dico_images["PlanteEte_Toundra"]
                        # Textures des plantes de la toundra en automne
                        elif self.saison.etat == "automne":
                            self.plante_image = self.dico_images["PlanteAutomne_Toundra"]
                        # Textures des plantes de la toundra en hiver
                        elif self.saison.etat == "hiver":
                            self.plante_image = self.dico_images["PlanteHiver_Toundra"]

                    # Création de la nouvelle plante et ajout au groupe de sprites
                    nouvelle_plante = Plantes(
                        self,
                        self.type_plante,
                        randint(0, config.LARGEUR),
                        randint(0, config.HAUTEUR),
                        screen,
                        0,
                        self.plante_image,
                    )
                    self.apparaitre_plante(nouvelle_plante)
                    self.nb_plantes += 1

            if (
                self.spawn_timer_herbivore >= config.DELAIS_SPAWN_HERBIVORES
            ):  # Toutes les 7.5 secondes (à 60 FPS)
                self.spawn_timer_herbivore = 0  # Réinitialisation du timer
                if not len(self.tous_herbivores) == 0:
                    nb_nouvelles = randint(1, 2)
                    index = randint(0, len(self.tous_herbivores) - 1)
                    for _ in range(nb_nouvelles):
                        if self.biome.etat == "plaine":
                            if list(self.tous_herbivores)[index].name == "Poule":
                                self.type_herbivore = "Poule"
                                self.herbivore_image = self.dico_images["Herbivore_plaine"]
                            elif list(self.tous_herbivores)[index].name == "Vache":
                                self.type_herbivore = "Vache"
                                self.herbivore_image = self.dico_images["Herbivore2_plaine"]
                        elif self.biome.etat == "foret":
                            self.type_herbivore = "Sanglier"
                            self.herbivore_image = self.dico_images["Herbivore_foret"]
                        elif self.biome.etat == "desert":
                            self.type_herbivore = "Chameau"
                            self.herbivore_image = self.dico_images["Herbivore_desert"]
                        elif self.biome.etat == "toundra":
                            self.type_herbivore = "Cerf"
                            self.herbivore_image = self.dico_images["Herbivore_toundra"]
                        # Création et ajout de l'herbivore
                        self.herbivore = Herbivores(
                            self,
                            self.type_herbivore,
                            list(self.tous_herbivores)[index].x,
                            list(self.tous_herbivores)[index].y,
                            screen,
                            temps,
                            self.herbivore_image,
                        )
                        self.apparaitre_herbivore(self.herbivore)
                        self.nb_herbivores += 1

            if (
                self.spawn_timer_carnivore >= config.DELAIS_SPAWN_CARNIVORES
            ):  # Toutes les 10 secondes (à 60 FPS)
                self.spawn_timer_carnivore = 0  # Réinitialisation du timer
                if not len(self.tous_carnivores) == 0:
                    nb_nouvelles = randint(1, 2)
                    for _ in range(nb_nouvelles):
                        if self.biome.etat == "plaine":
                            self.type_carnivore = "Renard"
                            self.carnivore_image = self.dico_images["Predateur_plaine"]
                        # Textures des carnivores de la forêt
                        elif self.biome.etat == "foret":
                            self.type_carnivore = "Ours"
                            self.carnivore_image = self.dico_images["Predateur_foret"]
                        # Textures des carnivores du désert
                        elif self.biome.etat == "desert":
                            self.type_carnivore = "Fennec"
                            self.carnivore_image = self.dico_images["Predateur_desert"]
                        # Textures des carnivores de la toundra
                        elif self.biome.etat == "toundra":
                            self.type_carnivore = "Loup"
                            self.carnivore_image = self.dico_images["Predateur_toundra"]
                        # Création et ajout du carnivore
                        index = randint(0, len(self.tous_carnivores) - 1)
                        self.carnivore = Carnivores(
                            self,
                            self.type_carnivore,
                            list(self.tous_carnivores)[index].x,
                            list(self.tous_carnivores)[index].y,
                            screen,
                            temps,
                            self.carnivore_image,
                        )
                        self.apparaitre_carnivore(self.carnivore)
                        self.nb_carnivores += 1

            # Fait grandir chaque plante (croissance, vieillissement, etc.)
            for plante in list(self.tous_plantes):
                plante.grow()

            # Affichage de tous les sprites sur l'écran
            self.tous_plantes.draw(screen)
            self.tous_herbivores.draw(screen)
            self.tous_carnivores.draw(screen)

            self.chrono_ms += temps  # accumule les millisecondes
            if self.chrono_ms >= config.CHRONO_MS:
                self.heures += 1
                self.chrono_ms -= config.CHRONO_MS
                if self.heures >= 24:
                    self.jours += 1
                    self.heures = 0

            self.chrono_graphique += temps
            if self.chrono_graphique >= config.CHRONO_GRAPH:
                self.liste_jours.append(self.jours * 24 + self.heures)
                self.historique_plantes.append(self.nb_plantes)
                self.historique_herbivores.append(self.nb_herbivores)
                self.historique_carnivores.append(self.nb_carnivores)
                self.chrono_graphique -= config.CHRONO_GRAPH

            if len(self.historique_plantes) > 1000:
                self.historique_plantes.pop(0)
            if len(self.historique_herbivores) > 1000:
                self.historique_herbivores.pop(0)
            if len(self.historique_carnivores) > 1000:
                self.historique_carnivores.pop(0)
            if len(self.liste_jours) > 1000:
                self.liste_jours.pop(0)

            self.chrono_graphique_update += temps
            if self.chrono_graphique_update >= config.CHRONO_GRAPH_UPDATE:
                if self.affichage_graphique:
                    update_graphique(self)
                self.chrono_graphique_update -= config.CHRONO_GRAPH_UPDATE

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
        self.spawn_timer_plante = 0
        self.spawn_timer_herbivore = 0
        self.spawn_timer_carnivore = 0
        self.chrono_ms = 0
        self.heures = 0
        self.jours = 0
        self.chrono_graphique = 0
        self.liste_jours = [0]
        self.historique_plantes = [self.nb_plantes]
        self.historique_herbivores = [self.nb_herbivores]
        self.historique_carnivores = [self.nb_carnivores]
        self.ax.clear()
        self.start = False
        self.is_playing = False
        self.pause = False

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

    def change_vitesse_simulation(self, val_vitesse):
        if self.vitesse_sim == val_vitesse:
            # change les valeurss de tous les attributs de vitesse, d'energie et de delais de spawn
            config.CROISSANCE = config.CROISSANCE_BASE * self.vitesse_sim
            config.DELAIS_SPAWN_PLANTES = config.DELAIS_SPAWN_PLANTES_BASE / self.vitesse_sim
            config.DELAIS_SPAWN_HERBIVORES = config.DELAIS_SPAWN_HERBIVORES_BASE / self.vitesse_sim
            config.DELAIS_SPAWN_CARNIVORES = config.DELAIS_SPAWN_CARNIVORES_BASE / self.vitesse_sim
            config.COUT_ENERGY_HERBIVORE = config.COUT_ENERGY_HERBIVORE_BASE * self.vitesse_sim
            config.COUT_ENERGY_CARNIVORE = config.COUT_ENERGY_CARNIVORE_BASE * self.vitesse_sim
            config.VITESSE_HERBIVORE = config.VITESSE_HERBIVORE_BASE * self.vitesse_sim
            config.VITESSE_CARNIVORE = config.VITESSE_CARNIVORE_BASE * self.vitesse_sim
            config.CHRONO_MS = config.CHRONO_MS_BASE / self.vitesse_sim
            config.CHRONO_GRAPH = config.CHRONO_GRAPH_BASE / self.vitesse_sim
            config.CHRONO_GRAPH_UPDATE = config.CHRONO_GRAPH_UPDATE_BASE / self.vitesse_sim
            # met à jour les valeurs pour chaque animaux
            for herbivore in list(self.tous_herbivores):
                herbivore.vitesse_base = config.VITESSE_HERBIVORE
                herbivore.vitesse = config.VITESSE_HERBIVORE
                herbivore.cout_energy_base = config.COUT_ENERGY_HERBIVORE
                herbivore.cout_energy = config.COUT_ENERGY_HERBIVORE
            for carnivore in list(self.tous_carnivores):
                carnivore.vitesse_base = config.VITESSE_CARNIVORE
                carnivore.vitesse = config.VITESSE_CARNIVORE
                carnivore.cout_energy_base = config.COUT_ENERGY_CARNIVORE
                carnivore.cout_energy = config.COUT_ENERGY_CARNIVORE
