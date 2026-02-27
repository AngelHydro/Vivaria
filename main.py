# Projet : Vivaria
# Auteurs : Benjamin MICHALAK, Angel SANCHEZ, Augustin MINOT

"""
Lance la simulation avec l'interface graphique.
"""

import sys  # Pour quitter le programme

import pygame

import config
from display import Display

# Initialisation de Pygame et de la fenêtre principale
pygame.init()

clock = pygame.time.Clock()
pygame.display.set_caption("Vivaria")
# Création de la fenêtre redimensionnable avec la taille définie dans config
screen = pygame.display.set_mode((config.LARGEUR, config.HAUTEUR), pygame.RESIZABLE)


def draw_background():
    # Dessine un fond vert sur toute la surface de la fenêtre
    pygame.draw.rect(screen, (0, 255, 0), (0, 0, config.LARGEUR, config.HAUTEUR))


# Instancie la classe Display qui gère toutes les entités et interactions
display = Display(screen)

# Préparation des surfaces de texte et des boutons (affichage statique)
titre_font = pygame.font.Font(None, 20)
titre = titre_font.render("Écosystème - Forêt", True, (255, 255, 255))
instruction_font = pygame.font.Font(None, 14)
instruction = instruction_font.render(
    "Cliquez sur les contrôles pour intéragir", True, (255, 255, 255)
)
# Définition du bouton "Démarrer"
bouton_demarrer = pygame.Rect(
    config.LARGEUR * 83 / 100,
    config.HAUTEUR * 65 / 100,
    config.LARGEUR * 15 / 100,
    config.HAUTEUR * 7 / 100,
)
texte_demarrer_font = pygame.font.Font(None, 12)
texte_demarrer = texte_demarrer_font.render("Démarrer", True, (0, 0, 0))
texte_demarrer_rect = texte_demarrer.get_rect(center=bouton_demarrer.center)

# Positionnement du bouton "Réinitialiser"
bouton_reinitialiser = pygame.Rect(
    config.LARGEUR * 83 / 100,
    config.HAUTEUR * 75 / 100,
    config.LARGEUR * 15 / 100,
    config.HAUTEUR * 7 / 100,
)
texte_reinitialiser_font = pygame.font.Font(None, 12)
texte_reinitialiser = texte_reinitialiser_font.render("Réinitialiser", True, (0, 0, 0))
texte_reinitialiser_rect = texte_reinitialiser.get_rect(
    center=bouton_reinitialiser.center
)

# Positionnement des surfaces affichant les compteurs d'entités
surface_nb_plantes = pygame.Rect(
    config.LARGEUR * 2 / 100,
    config.HAUTEUR * 3 / 100,
    config.LARGEUR * 15 / 100,
    config.HAUTEUR * 7 / 100,
)
surface_nb_herbivores = pygame.Rect(
    config.LARGEUR * 2 / 100,
    config.HAUTEUR * 13 / 100,
    config.LARGEUR * 15 / 100,
    config.HAUTEUR * 7 / 100,
)
surface_nb_carnivores = pygame.Rect(
    config.LARGEUR * 2 / 100,
    config.HAUTEUR * 23 / 100,
    config.LARGEUR * 15 / 100,
    config.HAUTEUR * 7 / 100,
)

# Placeholders pour les boutons de sélection de biome (à remplacer par de vrais boutons plus tard)
bouton_plaine = pygame.Rect(
    0,
    config.HAUTEUR * 3 / 100,
    config.LARGEUR * 15 / 100,
    config.HAUTEUR * 7 / 100,
) 
bouton_foret = pygame.Rect(
    0,
    config.HAUTEUR * 3 / 100,
    config.LARGEUR * 15 / 100,
    config.HAUTEUR * 7 / 100,
)
bouton_desert = pygame.Rect(
    0,
    config.HAUTEUR * 3 / 100,
    config.LARGEUR * 15 / 100,
    config.HAUTEUR * 7 / 100,
)
bouton_toundra = pygame.Rect(
    0,
    config.HAUTEUR * 3 / 100,
    config.LARGEUR * 15 / 100,
    config.HAUTEUR * 7 / 100,
)

texte_plaine_font = pygame.font.Font(None, 12)
texte_plaine = texte_plaine_font.render("Plaine", True, (0, 0, 0))
texte_foret_font = pygame.font.Font(None, 12)
texte_foret = texte_foret_font.render("Forêt", True, (0, 0, 0))
texte_desert_font = pygame.font.Font(None, 12)
texte_desert = texte_desert_font.render("Désert", True, (0, 0, 0))
texte_toundra_font = pygame.font.Font(None, 12)
texte_toundra = texte_toundra_font.render("Toundra", True, (0, 0, 0))

running = True
fullscreen = False

# Boucle principale du jeu
while running:
    draw_background()
    # Limite la boucle à 60 FPS et récupère le temps écoulé depuis la dernière frame
    temps = clock.tick(60)

    # Génère dynamiquement les textes des compteurs d'entités à chaque frame
    texte_nb_plantes_font = pygame.font.Font(None, 15)
    texte_nb_plantes = texte_nb_plantes_font.render(
        f"{display.nb_plantes} plantes", True, (0, 0, 0)
    )
    texte_nb_herbivores_font = pygame.font.Font(None, 15)
    texte_nb_herbivores = texte_nb_herbivores_font.render(
        f"{display.nb_herbivores} herbivores", True, (0, 0, 0)
    )
    texte_nb_carnivores_font = pygame.font.Font(None, 15)
    texte_nb_carnivores = texte_nb_carnivores_font.render(
        f"{display.nb_carnivores} carnivores", True, (0, 0, 0)
    )

    # Appliquer les effets cumulés de biome, météo et saison à chaque frame
    # (décommenter si la logique d'environnement est activée)
    """environment.appliquer_effets_environnement(
        display,
        display.biome if hasattr(display, "biome") else None,
        display.meteo if hasattr(display, "meteo") else None,
        display.saisons if hasattr(display, "saisons") else None,
    )"""

    # Affichage des boutons et compteurs sur la fenêtre
    pygame.draw.rect(screen, (0, 0, 0), bouton_demarrer, 3)
    screen.blit(texte_demarrer, texte_demarrer_rect)

    texte_nb_plantes_rect = texte_nb_plantes.get_rect(center=surface_nb_plantes.center)
    pygame.draw.rect(screen, (0, 0, 0), surface_nb_plantes, 3)
    screen.blit(texte_nb_plantes, texte_nb_plantes_rect)

    texte_nb_herbivores_rect = texte_nb_herbivores.get_rect(
        center=surface_nb_herbivores.center
    )
    pygame.draw.rect(screen, (0, 0, 0), surface_nb_herbivores, 3)
    screen.blit(texte_nb_herbivores, texte_nb_herbivores_rect)

    texte_nb_carnivores_rect = texte_nb_carnivores.get_rect(
        center=surface_nb_carnivores.center
    )
    pygame.draw.rect(screen, (0, 0, 0), surface_nb_carnivores, 3)
    screen.blit(texte_nb_carnivores, texte_nb_carnivores_rect)

    # Si la simulation est en cours et non en pause, on met à jour les entités
    if display.is_playing and not display.pause:
        display.mise_a_jour(screen)
    else:
        # Sinon, on affiche le titre, les instructions et le bouton réinitialiser
        # (utile lors de la pause ou avant le démarrage)
        titre_rect = titre.get_rect(center=(config.LARGEUR // 2, config.HAUTEUR // 2))
        instruction_rect = instruction.get_rect(
            center=(config.LARGEUR // 2, config.HAUTEUR // 2 + 20)
        )

        pygame.draw.rect(screen, (0, 0, 0), bouton_reinitialiser, 3)
        screen.blit(titre, titre_rect)
        screen.blit(instruction, instruction_rect)
        screen.blit(texte_reinitialiser, texte_reinitialiser_rect)

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
                    screen = pygame.display.set_mode(
                        (config.LARGEUR, config.HAUTEUR), pygame.FULLSCREEN
                    )
                else:
                    screen = pygame.display.set_mode(
                        (config.LARGEUR, config.HAUTEUR), pygame.RESIZABLE
                    )
        elif event.type == pygame.VIDEORESIZE:
            # Redimensionnement de la fenêtre, on adapte la taille dans config
            config.LARGEUR, config.HAUTEUR = event.w, event.h
            screen = pygame.display.set_mode(
                (config.LARGEUR, config.HAUTEUR), pygame.RESIZABLE
            )
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Gestion des clics sur les boutons
            if bouton_demarrer.collidepoint(event.pos):
                if display.pause:
                    if not display.start:
                        display.demarrage(screen, temps, 5)
                    else:
                        display.pause = False
                else:
                    display.pause = True
            elif bouton_reinitialiser.collidepoint(event.pos):
                display.reinitialiser()
            if bouton_plaine.collidepoint(event.pos):
                display.biome.plaine()
            elif bouton_foret.collidepoint(event.pos):
                display.biome.foret()
            elif bouton_desert.collidepoint(event.pos):
                display.biome.desert()
            elif bouton_toundra.collidepoint(event.pos):
                display.biome.toundra()

    # Rafraîchit l'affichage à chaque itération de la boucle
    pygame.display.flip()
