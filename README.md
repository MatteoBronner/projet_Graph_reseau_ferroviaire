# Planificateur de trajets ferroviaires

## Présentation de l’élève
- **Nom / Prénom** : Mattéo BRONNER
- **Année / Formation** : BUT Informatique, 2ᵉ année  (S2A2)
- **Objectif du projet** : Mettre en pratique la programmation orientée objet, la gestion de graphes et la création d’une interface graphique avec PyQt6.

---

## Présentation du projet
Ce projet consiste en un **planificateur de trajets ferroviaires** simulant un réseau TER et TGV.

### Pourquoi se projet :
Moi-même Mulhousien, et utilisateur régulier du TER entre Wittelsheim et Belfort, je trouvais l'idée de faire un projet basé sur un reseau férroviaire très amusant. De plus, ce projet m'a permis de travaillier sur plusieurs notions des graphiques.

### Objectifs :
- Permettre à un utilisateur de rechercher des trajets entre deux gares.
- Afficher **tous les trajets possibles**, ainsi que le **trajet le plus rapide** et le **trajet le moins cher**.
- Fournir une interface graphique (GUI) avec visualisation du réseau, survol des arêtes, et détails des trajets.

### Fonctionnement :
- Le projet utilise la librairie **NetworkX** pour gérer le réseau comme un graphe avec des arêtes multiples (TER et TGV).  
- L’algorithme de **Dijkstra** est utilisé pour calculer le plus court chemin selon le critère sélectionné (temps ou prix).  
- L’interface graphique est réalisée avec **PyQt6** et **Matplotlib** pour afficher le réseau et les trajets.  
- Les trajets sont affichés dans la GUI avec leurs détails et mis en évidence sur la carte.

---

## Installation et lancement

### Pré-requis
- Python 3.10 ou supérieur  
- Bibliothèques Python nécessaires :
```bash
pip install networkx matplotlib PyQt6
```

### Lancer le projet
1. Cloner le dépôt :
```bash
git clone https://github.com/MatteoBronner/projet_Graph_reseau_ferroviaire.git
```
2. Se placer dans le dossier `src` :
```bash
cd src
```
3. Rendre le script exécutable :
```bash
chmod +x run.sh
```
4. Lancer l’application :
```bash
./run.sh
```
5. Optionnel : utiliser le fichier `.desktop` fourni pour un lancement direct depuis la racine du projet.

---

## Utilisation
1. Sélectionner la **gare de départ** et la **gare d’arrivée**.  
2. Choisir le type de train (TER / TGV).  
3. Cliquer sur **Rechercher trajets** pour afficher la liste des trajets.  
4. Cliquer sur un trajet dans la liste pour voir **le détail par segment**, le **temps total** et le **prix total**.  
5. La carte affiche le réseau ferroviaire, avec le trajet sélectionné en rouge et le reste du réseau en gris.

---

## Concepts et notions utilisées du cours

| Concept                     | Description                                                                                   | Diapo du cours             |
|-----------------------------|-----------------------------------------------------------------------------------------------|----------------------------|
| Graphe et sous-graph        | Le réseau ferroviaire est représenté comme un graphe. Filtrage par type de train = sous-graph | Diapos 9-10                |
| Dijkstra                    | Calcul du plus court chemin selon un critère (temps/prix)                                     | Diapos 15-18               |
| MultiGraph                  | Permet plusieurs arêtes entre deux mêmes gares (TER et TGV)                                   | Diapo 11                   |
| Reconstruction des segments | Pour afficher les détails de chaque liaison                                                   | Diapo 17-18                |
| PyQt6 / GUI                 | Interface graphique pour sélectionner les gares et afficher le réseau                         | TP3 / Diapos GUI           |
| Matplotlib                  | Visualisation du graphe dans la GUI                                                           | TP3 / Diapos Graphes + GUI |

---

## Structure du projet
```
/src
 ├─ graph.py                 # Définition des classes Gare et ReseauFerroviaire
 ├─ main.py                  # Initialisation du réseau ferroviaire (utilisé pour tester le code avec affichage dans la console)
 ├─ gui.py                   # Interface graphique avec PyQt6
 ├─ run.sh                   # Script de lancement
 ├─ icone.png                # Icône pour le .desktop
 planFerroviaire.desktop     # Lancement depuis la racine du projet
 README.md                   # Ce fichier
```

---

## Améliorations futures possibles
- Ajouter la possibilité de **filtrer par lignes spécifiques** ou **par durée maximale**.  
- Intégrer une carte réelle avec **coordonnées GPS** des gares.  
- Ajouter la **prise en compte des correspondances** et horaires réels.  
- Ajouter un export des trajets vers **PDF ou CSV**.

---

## Remarques
- Ce projet est un outil pédagogique pour comprendre la gestion de graphes et les algorithmes de plus court chemin.  
- Il peut être amélioré pour un usage réel avec des données ferroviaires complètes.

