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

```
python CommentRatio.py --path <chemin_du_dossier> --ratio <ratio_minimum> [--include-ext <extensions>] [--exclude-ext <extensions>] [--exclude-dir <regex>]
```

Options :
- `--path` : Chemin vers le dossier à analyser. Si non spécifié, le script analysera le dossier courant.
- `--ratio` : Pourcentage minimum de commentaires accepté.
- `--include-ext` : Inclure seulement les fichiers avec les extensions spécifiées.
- `--exclude-ext` : Exclure les fichiers avec les extensions spécifiées.
- `--exclude-dir` : Exclure des dossiers spécifiques basés sur des regex.


## Contribution
Les contributions pour ajouter de nouvelles fonctionnalités, améliorer la prise en charge des langages ou corriger des bugs sont toujours les bienvenues.

## Améliorations à apporter


- **Prise en charge de multiples syntaxes de commentaires** : Étendre le script pour reconnaître et analyser diverses syntaxes de commentaires en fonction des langages de programmation.

- **Optimisation des performances** : Améliorer l'efficacité du script, en particulier pour les grands projets avec de nombreux fichiers.

- **Documentation détaillée** : Bien que bénéfique, la mise à jour exhaustive de la documentation n'est pas une priorité immédiate.
- **Interface utilisateur graphique** : Une interface graphique rendrait le script plus accessible, mais n'est pas prioritaire pour l'instant.
- **Rapports exportables** : La possibilité d'exporter des rapports serait utile, mais peut être mise en attente pour l'instant.


