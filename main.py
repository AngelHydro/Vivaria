# Projet : Vivaria
# Auteurs : Benjamin MICHALAK, Angel SANCHEZ, Augustin MINOT

"""
Lance la simulation avec l'interface graphique.
"""

import sys  # Pour quitter le programme

import pygame

import config
from display import Display

pygame.init()

clock = pygame.time.Clock()
pygame.display.set_caption("Vivaria")
screen = pygame.display.set_mode((config.LARGEUR, config.HAUTEUR), pygame.RESIZABLE)


def draw_background():
    pygame.draw.rect(screen, (0, 255, 0), (0, 0, config.LARGEUR, config.HAUTEUR))


# Prépare les surfaces de texte (le rendu ne dépend pas de la taille de la fenêtre)
titre_font = pygame.font.Font(None, 20)
titre = titre_font.render("Écosystème - Forêt", True, (255, 255, 255))
instruction_font = pygame.font.Font(None, 14)
instruction = instruction_font.render(
    "Cliquez sur les contrôles pour intéragir", True, (255, 255, 255)
)
bouton_demarrer = pygame.Rect(
    config.LARGEUR * 83 / 100,
    config.HAUTEUR * 65 / 100,
    config.LARGEUR * 15 / 100,
    config.HAUTEUR * 7 / 100,
)
texte_demarrer_font = pygame.font.Font(None, 12)
texte_demarrer = texte_demarrer_font.render("Démarrer", True, (0, 0, 0))
texte_demarrer_rect = texte_demarrer.get_rect(center=bouton_demarrer.center)

running = True
fullscreen = False
display = Display()

while running:
    draw_background()
    temps = clock.tick(60)

    if display.is_playing:
        display.mise_a_jour(screen)
    else:
        # Calcul des rectangles de texte à chaque frame, selon la taille actuelle
        titre_rect = titre.get_rect(center=(config.LARGEUR // 2, config.HAUTEUR // 2))
        instruction_rect = instruction.get_rect(
            center=(config.LARGEUR // 2, config.HAUTEUR // 2 + 20)
        )
        pygame.draw.rect(screen, (0, 0, 0), bouton_demarrer, 3)

        screen.blit(titre, titre_rect)
        screen.blit(instruction, instruction_rect)
        screen.blit(texte_demarrer, texte_demarrer_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()  # ferme le programme une fois la fenêtre fermée
        elif event.type == pygame.KEYDOWN:
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
            config.LARGEUR, config.HAUTEUR = event.w, event.h
            screen = pygame.display.set_mode(
                (config.LARGEUR, config.HAUTEUR), pygame.RESIZABLE
            )
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if bouton_demarrer.collidepoint(event.pos):
                display.demarrage(screen, temps)

    pygame.display.flip()
