![logo](data/img/logo.png)

Simulateur écologique interactif en Python permettant d'observer l'évolution d'un écosystème (plantes, herbivores, carnivores) en temps réel et d'expérimenter l'impact de différents paramètres sur l'équilibre naturel.

---
## À propos

**Vivaria** est un projet développé dans le cadre des **Trophées NSI 2026** par trois élèves de Terminale NSI du Lycée Polyvalent Clos Maire, sous la direction du professeur Chaddai Fouché & Christophe GUENEAU.

### Problématique
Comment **modéliser et visualiser** de manière interactive les **dynamiques d'équilibre et de déséquilibre** au sein d'un écosystème ?

### Objectif
Permettre à l'utilisateur d'**observer en temps réel** l'évolution des populations (plantes, herbivores, carnivores) et de **comprendre comment les modifications de paramètres environnementaux** (météo, saisons, biomes) impactent l'équilibre naturel.

---
## Fonctionnalités
### Simulation écologique
- **3 types d'entités** : Plantes, Herbivores, Carnivores
- **Comportements intelligents** : Les herbivores fuient les carnivores, les carnivores chassent les herbivores
- **Système d'énergie** : Manger = gain, vivre = perte, 0 énergie = mort
- **Vieillissement** et mort naturelle
- **Reproduction** (à venir)

### Environnement dynamique (à venir)
- **4 biomes** : Forêt, Plaine, Désert, Toundra
- **4 météos** : Soleil, Pluie, Orage, Neige
- **4 saisons** : Printemps, Été, Automne, Hiver
- Chaque paramètre impacte la croissance, reproduction et survie

### Interface (à venir)
- Affichage temps réel des populations
- Contrôle de la vitesse de simulation (x1, x2, x5, x10)
- Graphiques d'évolution
- Boutons interactifs pour modifier l'environnement

---
## Comment jouer
### Prérequis
- Python 3.x
- Pygame 3.6.2

### Installation
```bash
# Cloner le projet
git clone [votre-repo]
cd vivaria

# Installer les dépendances
pip install -r requirements.txt
```

### Lancement
```bash
python main.py
```

### Contrôles
- **Clic** sur "Démarrer" pour lancer la simulation
- **F** : Basculer en plein écran
- (Plus de contrôles à venir)

---
## Technologies utilisées

- **Python 3.x** : Langage principal
- **Pygame 3.6.2** : Moteur graphique et gestion des sprites
- **Programmation Orientée Objet** : Architecture modulaire

### Structure du projet
```
vivaria/
├── main.py           # Point d'entrée
├── ecosystem.py      # Logique des entités (Plantes, Herbivores, Carnivores)
├── display.py        # Gestion de l'affichage et des interactions
├── environment.py    # Système de biomes, météo et saisons
├── config.py         # Paramètres de configuration
└── data/            # Assets graphiques
```

---
## Équipe

**Angel SANCHEZ**  
Développement technique - Classes et fonctionnalités de simulation

**Augustin MINOT**  
Direction artistique - Textures, sprites et design visuel

**Benjamin MICHALAK**  
Interface utilisateur - Intégration visuelle et tests de simulation

---
## Projet scolaire

**Cadre :** Trophées NSI 2026  
**Établissement :** Lycée Polyvalent Clos Maire  
**Classe :** Terminale NSI  
**Encadrant :** Chaddai FOUCHE & Christophe GUENEAU(Professeurs de NSI)  
**Thème :** Nature
