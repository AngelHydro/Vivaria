# Projet : Vivaria
# Auteurs : Benjamin MICHALAK, Angel SANCHEZ, Augustin MINOT

"""
Lance la simulation avec l'interface graphique.
"""

import sys  # Pour quitter le programme

import pygame

import config
import environment
from display import Display
from graphique import *

# Initialisation de Pygame et de la fenêtre principale
pygame.init()

clock = pygame.time.Clock()
# Définit le titre de la fenêtre et l'icône de l'application
pygame.display.set_caption("Vivaria")
icone = pygame.image.load("data/img/logo.png")
pygame.display.set_icon(icone)
# Création de la fenêtre redimensionnable avec la taille définie dans config
screen = pygame.display.set_mode((config.LARGEUR, config.HAUTEUR), pygame.RESIZABLE)

# Instancie la classe Display qui gère toutes les entités et interactions
display = Display(screen)

fond = pygame.image.load("data/img/Plaine_printemps.png")
taille_w = fond.get_width()
taille_h = fond.get_height()

def draw_background():
    # Dessine un fond vert sur toute la surface de la fenêtre
    for i in range(0, config.LARGEUR, taille_w):
        for j in range(0, config.HAUTEUR, taille_h):
            screen.blit(fond, (i, j))

# Création des polices et des surfaces de texte pour les boutons de sélection de biome
# Création des polices et surfaces de texte pour chaque bouton de sélection de biome

running = True
fullscreen = False


# Fonction qui prend en paramètre l'écran et retourne les différents boutons et surfaces de l'interface redimensionnés en fonction de la taille d'écran
def recalculer_dimensions(screen):
    # Récupère la largeur et la hauteur de l'écran actuel
    w, h = screen.get_size()

    # Redimensionne et repositionne tous les boutons et surfaces selon la taille de l'écran
    bouton_demarrer = pygame.Rect(w * 83 / 100, h * 60 / 100, w * 15 / 100, h * 7 / 100)
    bouton_reinitialiser = pygame.Rect(
        w * 83 / 100, h * 70 / 100, w * 15 / 100, h * 7 / 100
    )
    surface_nb_plantes = pygame.Rect(
        w * 2 / 100, h * 3 / 100, w * 15 / 100, h * 7 / 100
    )
    surface_nb_herbivores = pygame.Rect(
        w * 2 / 100, h * 13 / 100, w * 15 / 100, h * 7 / 100
    )
    surface_nb_carnivores = pygame.Rect(
        w * 2 / 100, h * 23 / 100, w * 15 / 100, h * 7 / 100
    )
    surface_biome = pygame.Rect(0, h * 49 / 100, w * 30 / 100, h * 16 / 100)
    surface_meteo = pygame.Rect(0, h * 66 / 100, w * 30 / 100, h * 16 / 100)
    surface_saison = pygame.Rect(0, h * 83 / 100, w * 30 / 100, h * 16 / 100)
    bouton_plaine = pygame.Rect(w * 2 / 100, h * 53 / 100, w * 7 / 100, h * 4 / 100)
    bouton_foret = pygame.Rect(w * 10 / 100, h * 53 / 100, w * 7 / 100, h * 4 / 100)
    bouton_desert = pygame.Rect(w * 19 / 100, h * 53 / 100, w * 7 / 100, h * 4 / 100)
    bouton_toundra = pygame.Rect(w * 2 / 100, h * 59 / 100, w * 7 / 100, h * 4 / 100)
    bouton_soleil = pygame.Rect(w * 2 / 100, h * 70 / 100, w * 7 / 100, h * 4 / 100)
    bouton_pluie = pygame.Rect(w * 10 / 100, h * 70 / 100, w * 7 / 100, h * 4 / 100)
    bouton_orage = pygame.Rect(w * 19 / 100, h * 70 / 100, w * 7 / 100, h * 4 / 100)
    bouton_neige = pygame.Rect(w * 2 / 100, h * 76 / 100, w * 7 / 100, h * 4 / 100)
    bouton_printemps = pygame.Rect(w * 2 / 100, h * 87 / 100, w * 7 / 100, h * 4 / 100)
    bouton_ete = pygame.Rect(w * 10 / 100, h * 87 / 100, w * 7 / 100, h * 4 / 100)
    bouton_automne = pygame.Rect(w * 19 / 100, h * 87 / 100, w * 7 / 100, h * 4 / 100)
    bouton_hiver = pygame.Rect(w * 2 / 100, h * 93 / 100, w * 7 / 100, h * 4 / 100)
    surface_chrono = pygame.Rect(w * 88 / 100, h * 3 / 100, w * 10 / 100, h * 4 / 100)
    bouton_graphique = pygame.Rect(w * 83 / 100, h * 80 / 100, w * 15 / 100, h * 7 / 100)

    display.fig.set_size_inches(w / 100, h / 100)
    display.ax.clear()

    # Retourne tous les boutons et surfaces recalculés
    return (
        bouton_demarrer,
        bouton_reinitialiser,
        surface_nb_plantes,
        surface_nb_herbivores,
        surface_nb_carnivores,
        surface_biome,
        surface_meteo,
        surface_saison,
        bouton_plaine,
        bouton_foret,
        bouton_desert,
        bouton_toundra,
        bouton_soleil,
        bouton_pluie,
        bouton_orage,
        bouton_neige,
        bouton_printemps,
        bouton_ete,
        bouton_automne,
        bouton_hiver,
        surface_chrono,
        bouton_graphique
    )

contenu_texte_demarrer = "Lancer"

# Boucle principale du jeu
while running:
    draw_background()
    # Limite la boucle à 60 FPS et récupère le temps écoulé depuis la dernière frame
    temps = clock.tick(60)
    if display.biome.etat == "plaine":
        if display.saison.etat == "printemps":
            fond = pygame.image.load("data/img/Plaine_printemps.png")
        elif display.saison.etat == "ete":
            fond = pygame.image.load("data/img/Plaine_été.png")
        elif display.saison.etat == "automne":
            fond = pygame.image.load("data/img/Plaine_automne.png")
        elif display.saison.etat == "hiver":
            fond = pygame.image.load("data/img/Plaine_Hiver.png")
    elif display.biome.etat == "foret":
        if display.saison.etat == "printemps":
            fond = pygame.image.load("data/img/Foret_Printemps.png")
        elif display.saison.etat == "ete":
            fond = pygame.image.load("data/img/Foret_été.png")
        elif display.saison.etat == "automne":
            fond = pygame.image.load("data/img/Foret_automne.png")
        elif display.saison.etat == "hiver":
            fond = pygame.image.load("data/img/Foret_hiver.png")
    elif display.biome.etat == "desert":
        if display.saison.etat == "printemps":
            fond = pygame.image.load("data/img/Desert_printemps.png")
        elif display.saison.etat == "ete":
            fond = pygame.image.load("data/img/Desert_été.png")
        elif display.saison.etat == "automne":
            fond = pygame.image.load("data/img/Desert_automne.png")
        elif display.saison.etat == "hiver":
            fond = pygame.image.load("data/img/Desert_hiver.png")
    elif display.biome.etat == "toundra":
        if display.saison.etat == "printemps":
            fond = pygame.image.load("data/img/Toundra_printemps.png")
        elif display.saison.etat == "ete":
            fond = pygame.image.load("data/img/Toundra_été.png")
        elif display.saison.etat == "automne":
            fond = pygame.image.load("data/img/Toundra_automne.png")
        elif display.saison.etat == "hiver":
            fond = pygame.image.load("data/img/Toundra_hiver.png")
    # Recalcule dynamiquement les positions et tailles des boutons/surfaces à chaque frame
    (
        bouton_demarrer,
        bouton_reinitialiser,
        surface_nb_plantes,
        surface_nb_herbivores,
        surface_nb_carnivores,
        surface_biome,
        surface_meteo,
        surface_saison,
        bouton_plaine,
        bouton_foret,
        bouton_desert,
        bouton_toundra,
        bouton_soleil,
        bouton_pluie,
        bouton_orage,
        bouton_neige,
        bouton_printemps,
        bouton_ete,
        bouton_automne,
        bouton_hiver,
        surface_chrono,
        bouton_graphique
    ) = recalculer_dimensions(screen)

    # Applique les effets de l'environnement si les attributs nécessaires existent
    if (
        hasattr(display, "biome")
        and hasattr(display, "meteo")
        and hasattr(display, "saison")
    ):
        environment.appliquer_effets_environnement(
            display,
            display.biome,
            display.meteo,
            display.saison,
        )

    def affichage_nb_entites():
        # Génère dynamiquement les textes des compteurs d'entités à chaque frame
        texte_nb_plantes_font = pygame.font.Font(None, config.TAILLE_FONT)
        texte_nb_plantes = texte_nb_plantes_font.render(
            f"{display.nb_plantes} plantes", True, (0, 0, 0)
        )
        texte_nb_plantes_rect = texte_nb_plantes.get_rect(center=surface_nb_plantes.center)
        pygame.draw.rect(screen, (0, 0, 0), surface_nb_plantes, 3)
        screen.blit(texte_nb_plantes, texte_nb_plantes_rect)

        texte_nb_herbivores_font = pygame.font.Font(None, config.TAILLE_FONT)
        texte_nb_herbivores = texte_nb_herbivores_font.render(
            f"{display.nb_herbivores} herbivores", True, (0, 0, 0)
        )
        texte_nb_herbivores_rect = texte_nb_herbivores.get_rect(
            center=surface_nb_herbivores.center
        )
        pygame.draw.rect(screen, (0, 0, 0), surface_nb_herbivores, 3)
        screen.blit(texte_nb_herbivores, texte_nb_herbivores_rect)

        texte_nb_carnivores_font = pygame.font.Font(None, config.TAILLE_FONT)
        texte_nb_carnivores = texte_nb_carnivores_font.render(
            f"{display.nb_carnivores} carnivores", True, (0, 0, 0)
        )
        texte_nb_carnivores_rect = texte_nb_carnivores.get_rect(
            center=surface_nb_carnivores.center
        )
        pygame.draw.rect(screen, (0, 0, 0), surface_nb_carnivores, 3)
        screen.blit(texte_nb_carnivores, texte_nb_carnivores_rect)

    # Affichage des boutons et compteurs sur la fenêtre
    def affichage_boutons_permanents():
        texte_demarrer_font = pygame.font.Font(None, config.TAILLE_FONT)
        texte_demarrer = texte_demarrer_font.render(contenu_texte_demarrer, True, (0, 0, 0))
        texte_demarrer_rect = texte_demarrer.get_rect(center=bouton_demarrer.center)
        pygame.draw.rect(screen, (0, 0, 0), bouton_demarrer, 3)
        screen.blit(texte_demarrer, texte_demarrer_rect)

        texte_graphique_font = pygame.font.Font(None, config.TAILLE_FONT)
        texte_graphique = texte_graphique_font.render("Graphique", True, (0, 0, 0))
        texte_graphique_rect = texte_graphique.get_rect(center=bouton_graphique.center)
        pygame.draw.rect(screen, (0, 0, 0), bouton_graphique, 3)
        screen.blit(texte_graphique, texte_graphique_rect)

        texte_chrono_font = pygame.font.Font(None, config.TAILLE_FONT)
        if display.jours < 10:
            if display.heures < 10:
                contenu_texte_chrono = f"0{display.jours}j 0{display.heures}h"
            else:
                contenu_texte_chrono = f"0{display.jours}j {display.heures}h"
        elif display.heures < 10:
            contenu_texte_chrono = f"{display.jours}j 0{display.heures}h"
        else:
            contenu_texte_chrono = f"{display.jours}j {display.heures}h"
        texte_chrono = texte_chrono_font.render(contenu_texte_chrono, True, (0, 0, 0))
        texte_chrono_rect = texte_chrono.get_rect(center=surface_chrono.center)
        pygame.draw.rect(screen, (0, 0, 0), surface_chrono, 3)
        screen.blit(texte_chrono, texte_chrono_rect)

    # Si la simulation est en cours et non en pause, on met à jour les entités
    if display.is_playing and not display.pause:
        contenu_texte_demarrer = "Pause"
        display.mise_a_jour(screen, temps)
        affichage_nb_entites()
        if display.affichage_graphique and display.surface_graphique is not None:
            screen.blit(display.surface_graphique, (0, 0))
        affichage_boutons_permanents()
    else:
        contenu_texte_demarrer = "Lancer"
        # Sinon, on affiche le titre, les instructions et le bouton réinitialiser
        # (utile lors de la pause ou avant le démarrage)
        titre_font = pygame.font.Font(None, config.TAILLE_FONT)
        titre = titre_font.render(
            f"Écosystème - {display.biome.etat}", True, (255, 255, 255)
        )
        titre_rect = titre.get_rect(center=(config.LARGEUR // 2, config.HAUTEUR // 2))
        instruction_font = pygame.font.Font(None, config.TAILLE_FONT)
        instruction = instruction_font.render(
            "Cliquez sur les contrôles pour intéragir", True, (255, 255, 255)
        )
        instruction_rect = instruction.get_rect(
            center=(config.LARGEUR // 2, config.HAUTEUR // 2 + 20)
        )

        texte_reinitialiser_font = pygame.font.Font(None, config.TAILLE_FONT)
        texte_reinitialiser = texte_reinitialiser_font.render(
            "Réinitialiser", True, (0, 0, 0)
        )
        texte_reinitialiser_rect = texte_reinitialiser.get_rect(
            center=bouton_reinitialiser.center
        )

        # Titre des surfaces de boutons de changement de biome, de météo et de saison
        texte_biome_font = pygame.font.Font(None, config.TAILLE_FONT)
        texte_biome = texte_biome_font.render("Biome", True, (255, 255, 255))
        texte_biome_rect = texte_biome.get_rect(
            center=(config.LARGEUR * 13.5 / 100, config.HAUTEUR * 51 / 100)
        )

        texte_meteo_font = pygame.font.Font(None, config.TAILLE_FONT)
        texte_meteo = texte_meteo_font.render("Météo", True, (255, 255, 255))
        texte_meteo_rect = texte_meteo.get_rect(
            center=(config.LARGEUR * 13.5 / 100, config.HAUTEUR * 68 / 100)
        )

        texte_saison_font = pygame.font.Font(None, config.TAILLE_FONT)
        texte_saison = texte_saison_font.render("Saison", True, (255, 255, 255))
        texte_saison_rect = texte_saison.get_rect(
            center=(config.LARGEUR * 13.5 / 100, config.HAUTEUR * 85 / 100)
        )

        # Bouton "Plaine"
        texte_plaine_font = pygame.font.Font(None, config.TAILLE_FONT)
        texte_plaine = texte_plaine_font.render("Plaine", True, (0, 0, 0))
        texte_plaine_rect = texte_plaine.get_rect(center=bouton_plaine.center)
        # Bouton "Forêt"
        texte_foret_font = pygame.font.Font(None, config.TAILLE_FONT)
        texte_foret = texte_foret_font.render("Forêt", True, (0, 0, 0))
        texte_foret_rect = texte_foret.get_rect(center=bouton_foret.center)
        # Bouton "Désert"
        texte_desert_font = pygame.font.Font(None, config.TAILLE_FONT)
        texte_desert = texte_desert_font.render("Désert", True, (0, 0, 0))
        texte_desert_rect = texte_desert.get_rect(center=bouton_desert.center)
        # Bouton "Toundra"
        texte_toundra_font = pygame.font.Font(None, config.TAILLE_FONT)
        texte_toundra = texte_toundra_font.render("Toundra", True, (0, 0, 0))
        texte_toundra_rect = texte_toundra.get_rect(center=bouton_toundra.center)

        # Bouton "Soleil"
        texte_soleil_font = pygame.font.Font(None, config.TAILLE_FONT)
        texte_soleil = texte_soleil_font.render("Soleil", True, (0, 0, 0))
        texte_soleil_rect = texte_soleil.get_rect(center=(bouton_soleil.center))
        # Bouton "Pluie"
        texte_pluie_font = pygame.font.Font(None, config.TAILLE_FONT)
        texte_pluie = texte_pluie_font.render("Pluie", True, (0, 0, 0))
        texte_pluie_rect = texte_pluie.get_rect(center=(bouton_pluie.center))
        # Bouton "Orage"
        texte_orage_font = pygame.font.Font(None, config.TAILLE_FONT)
        texte_orage = texte_orage_font.render("Orage", True, (0, 0, 0))
        texte_orage_rect = texte_orage.get_rect(center=(bouton_orage.center))
        # Bouton "Neige"
        texte_neige_font = pygame.font.Font(None, config.TAILLE_FONT)
        texte_neige = texte_neige_font.render("Neige", True, (0, 0, 0))
        texte_neige_rect = texte_neige.get_rect(center=(bouton_neige.center))

        # Bouton "Printemps"
        texte_printemps_font = pygame.font.Font(None, config.TAILLE_FONT)
        texte_printemps = texte_printemps_font.render("Printemps", True, (0, 0, 0))
        texte_printemps_rect = texte_printemps.get_rect(
            center=(bouton_printemps.center)
        )
        # Bouton "Ete"
        texte_ete_font = pygame.font.Font(None, config.TAILLE_FONT)
        texte_ete = texte_ete_font.render("Été", True, (0, 0, 0))
        texte_ete_rect = texte_ete.get_rect(center=(bouton_ete.center))
        # Bouton "Automne"
        texte_automne_font = pygame.font.Font(None, config.TAILLE_FONT)
        texte_automne = texte_automne_font.render("Automne", True, (0, 0, 0))
        texte_automne_rect = texte_automne.get_rect(center=(bouton_automne.center))
        # Bouton "Hiver"
        texte_hiver_font = pygame.font.Font(None, config.TAILLE_FONT)
        texte_hiver = texte_hiver_font.render("Hiver", True, (0, 0, 0))
        texte_hiver_rect = texte_hiver.get_rect(center=(bouton_hiver.center))

        # Affichage des éléments de l'interface utilisateur pendant la pause ou avant le démarrage
        # Dessine les contours des différentes surfaces et boutons
        pygame.draw.rect(screen, (0, 0, 0), bouton_reinitialiser, 3)
        pygame.draw.rect(screen, (0, 0, 0), surface_biome, 3)
        pygame.draw.rect(screen, (0, 0, 0), surface_meteo, 3)
        pygame.draw.rect(screen, (0, 0, 0), surface_saison, 3)
        pygame.draw.rect(screen, (0, 0, 0), bouton_plaine, 3)
        pygame.draw.rect(screen, (0, 0, 0), bouton_desert, 3)
        pygame.draw.rect(screen, (0, 0, 0), bouton_foret, 3)
        pygame.draw.rect(screen, (0, 0, 0), bouton_toundra, 3)
        pygame.draw.rect(screen, (0, 0, 0), bouton_soleil, 3)
        pygame.draw.rect(screen, (0, 0, 0), bouton_pluie, 3)
        pygame.draw.rect(screen, (0, 0, 0), bouton_orage, 3)
        pygame.draw.rect(screen, (0, 0, 0), bouton_neige, 3)
        pygame.draw.rect(screen, (0, 0, 0), bouton_printemps, 3)
        pygame.draw.rect(screen, (0, 0, 0), bouton_ete, 3)
        pygame.draw.rect(screen, (0, 0, 0), bouton_automne, 3)
        pygame.draw.rect(screen, (0, 0, 0), bouton_hiver, 3)
        # Affiche le titre, les instructions et les textes des boutons/surfaces
        screen.blit(titre, titre_rect)
        screen.blit(instruction, instruction_rect)
        screen.blit(texte_reinitialiser, texte_reinitialiser_rect)
        screen.blit(texte_biome, texte_biome_rect)
        screen.blit(texte_meteo, texte_meteo_rect)
        screen.blit(texte_saison, texte_saison_rect)
        screen.blit(texte_plaine, texte_plaine_rect)
        screen.blit(texte_foret, texte_foret_rect)
        screen.blit(texte_desert, texte_desert_rect)
        screen.blit(texte_toundra, texte_toundra_rect)
        screen.blit(texte_soleil, texte_soleil_rect)
        screen.blit(texte_pluie, texte_pluie_rect)
        screen.blit(texte_orage, texte_orage_rect)
        screen.blit(texte_neige, texte_neige_rect)
        screen.blit(texte_printemps, texte_printemps_rect)
        screen.blit(texte_ete, texte_ete_rect)
        screen.blit(texte_automne, texte_automne_rect)
        screen.blit(texte_hiver, texte_hiver_rect)

        affichage_nb_entites()
        if display.affichage_graphique and display.surface_graphique is not None:
            screen.blit(display.surface_graphique, (0, 0))
        affichage_boutons_permanents()

    # Gestion des événements utilisateur (clavier, souris, redimensionnement, fermeture)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Fermeture de la fenêtre
            running = False
            pygame.quit()
            sys.exit()  # ferme le programme une fois la fenêtre fermée
        elif event.type == pygame.KEYDOWN:
            # Touche F pour basculer en plein écran ou revenir en mode fenêtré
            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode(
                        (config.LARGEUR, config.HAUTEUR), pygame.RESIZABLE
                    )
        elif event.type == pygame.VIDEORESIZE:
            # Redimensionnement de la fenêtre, on adapte la taille dans config
            config.LARGEUR, config.HAUTEUR = event.w, event.h
            if not fullscreen:
                screen = pygame.display.set_mode(
                    (config.LARGEUR, config.HAUTEUR), pygame.RESIZABLE
                )
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Gestion des clics sur les boutons
            if bouton_demarrer.collidepoint(event.pos):
                if display.pause:
                    if not display.start:
                        display.demarrage(
                            screen,
                            temps,
                            config.NOMBRE_INITIAL_PLANTES,
                            config.NOMBRE_INITIAL_HERBIVORES,
                            config.NOMBRE_INITIAL_CARNIVORES,
                        )
                    else:
                        display.pause = False
                else:
                    display.pause = True
            elif bouton_reinitialiser.collidepoint(event.pos):
                display.reinitialiser()
            elif bouton_graphique.collidepoint(event.pos):
                display.affichage_graphique = not display.affichage_graphique
            # conditions pour les collisions des boutons de changement de biome
            if bouton_plaine.collidepoint(event.pos):
                display.reinitialiser()
                display.biome.plaine()
            elif bouton_foret.collidepoint(event.pos):
                display.reinitialiser()
                display.biome.foret()
            elif bouton_desert.collidepoint(event.pos):
                display.reinitialiser()
                display.biome.desert()
            elif bouton_toundra.collidepoint(event.pos):
                display.reinitialiser()
                display.biome.toundra()
            # conditions pour les collisions des boutons de changement de météo
            if bouton_soleil.collidepoint(event.pos):
                display.meteo.soleil()
            elif bouton_pluie.collidepoint(event.pos):
                display.meteo.pluie()
            elif bouton_orage.collidepoint(event.pos):
                display.meteo.orage()
            elif bouton_neige.collidepoint(event.pos):
                display.meteo.neige()
            # conditions pour les conditions des boutons de changement de saison
            if bouton_printemps.collidepoint(event.pos):
                display.saison.printemps()
            elif bouton_ete.collidepoint(event.pos):
                display.saison.ete()
            elif bouton_automne.collidepoint(event.pos):
                display.saison.automne()
            elif bouton_hiver.collidepoint(event.pos):
                display.saison.hiver()

    # Rafraîchit l'affichage à chaque itération de la boucle
    pygame.display.flip()
