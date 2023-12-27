# CommentRatio

## Description
CommentRatio est un outil en ligne de commande conçu pour analyser les fichiers de code source et calculer le pourcentage de commentaires. Ce script prend en charge plusieurs langages de programmation et gère à la fois les commentaires de ligne et les commentaires de bloc.

## Fonctionnalités
- Prise en charge de n'importe quel langage disposant d'une syntax de commentaire unique 
- Fichier de configuration JSON, permettant d'ajouter / modifier les langages pris en charge et leurs symboles de commentaires.
- Les langages de base inclus dans la configuration sont C, C++, Python, HTML, CSS, JavaScript, et SQL.
- Analyse des commentaires de ligne et de bloc.
- Calcul du pourcentage global de commentaires dans un dossier ou un projet spécifié.
- Affichage du pourcentage de commentaires par fichier.

## Prérequis
- Python 3.x
  - argparse
  - colorama

## Utilisation
Pour exécuter le script, utilisez la ligne de commande en naviguant vers le dossier contenant le script `CommentRatio.py` et exécutez la commande suivante :

python CommentRatio.py **--path** &lt;chemin_du_dossier&gt; **--ratio** &lt;ratio_minimum&gt;[**--include-ext** &lt;extensions&gt;] [**--exclude-ext** &lt;extensions&gt;] [**--exclude-dir** &lt;regex&gt;]

Options :
- `--path` : Chemin vers le dossier à analyser. Si non spécifié, le script analysera le dossier courant.
- `--ratio` : Pourcentage minimum de commentaires accepté. Par défaut à 30 si non spécifié.
- `--include-ext` : Inclure seulement les fichiers avec les extensions spécifiées. Si non spécifié, aucun filtre d'extension n'est appliqué.
- `--exclude-ext` : Exclure les fichiers avec les extensions spécifiées. Si non spécifié, aucun filtre d'exclusion n'est appliqué.
- `--exclude-dir` : Exclure des dossiers spécifiques basés sur des regex. Si non spécifié, aucun dossier n'est exclu.


## Contribution
Les contributions pour ajouter de nouvelles fonctionnalités, améliorer la prise en charge des langages ou corriger des bugs sont toujours les bienvenues.

# To-Do List

## Améliorations à apporter

### Exclusion Sélective
- **Objectif :** Ajouter une option pour exclure certains types de fichiers ou dossiers via des expressions régulières (regex). Cela permettra une analyse plus ciblée.

#### Sous-Tâches :
  - Ajouter un argument pour exclure des extensions de fichier spécifiques.
  - Ajouter un argument pour exclure des dossiers ou fichiers spécifiques.

### Sélection Spécifique
- **Objectif :** Permettre à l'utilisateur de spécifier des extensions, des dossiers ou des fichiers particuliers à analyser, au lieu de l'ensemble du dossier.

#### Sous-Tâches :
  - Ajouter un argument pour inclure uniquement certaines extensions de fichier.
  - Ajouter un argument pour analyser uniquement certains dossiers ou fichiers spécifiés.

### Documentation et Aide
- **Objectif :** Mettre à jour la documentation et l'aide intégrée au script pour refléter les nouvelles fonctionnalités et options.

#### Sous-Tâches :
  - Mettre à jour le README pour inclure les nouvelles options et arguments.
  - Ajouter des instructions d'utilisation détaillées pour les nouvelles fonctionnalités.

