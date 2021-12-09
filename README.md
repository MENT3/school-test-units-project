# YNOV 2021 - Projet tests unitaires

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/fixed-bugs.svg)](https://forthebadge.com)

<br>

## Liens
Rapport locust: https://ment3.github.io/school-test-units-project/locust_report.html

Rapport de couverture: https://ment3.github.io/school-test-units-project

<br>


## Installation
---

1. Install `python >= 3.0`
2. Clone projetct
  ```bash
  $ git clone git@github.com:MENT3/school-test-units-project.git
  ```
3. Install dépendencies
```bash
# Se déplacer à la racine du projet
$ cd school-test-units-project

# Installation des dépendences depuis le fichier requirements.txt
$ pip3 install -r requirements.txt
```

<br>

## Utilisation
---
### Lancement du serveur
```bash
# Se déplacer à la racine du projet
$ cd school-test-units-project

$ python3 server.py
```

<br>

### Lancement des tests
```bash
# Se déplacer à la racine du projet
$ cd school-test-units-project

$ python3 -m pytest
```

<br>

### Voir la couverture des tests
```bash
# Se déplacer à la racine du projet
$ cd school-test-units-project

$ python3 -m coverage run --source=. -m pytest
$ python3 -m coverage report
```

<br>

### Générer un rapport de couverture des tests
```bash
# Se déplacer à la racine du projet
$ cd school-test-units-project

$ python3 -m coverage run --source=. -m pytest
$ python3 -m coverage html

# Attention: commande disponible seulement sur mac
$ open dists/index.html
```

<br>

### Lancer locust
Il faut lancer lancer le serveur : `Lancement du serveur`

Dans un autre terminal
```bash
# Se déplacer à la racine du projet
$ cd school-test-units-project

$ python3 -m locust -f tests/locustfile.py
```
