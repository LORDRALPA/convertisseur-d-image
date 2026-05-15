# Convertisseur d'images

## Description
Ce projet permet de convertir des images en format JPEG. Les images brutes doivent être placées dans le dossier `images brutes`, et les images converties seront enregistrées dans le dossier `images converties`.

## Structure du projet
- `convert_images.py` : Script Python pour la conversion des images.
- `run_converter.bat` : Lanceur pour exécuter le script Python.
- `images brutes/` : Dossier contenant les images à convertir.
- `images converties/` : Dossier où les images converties seront enregistrées.

## Instructions

### Prérequis
- Python 3.x doit être installé.
- Le module `Pillow` doit être installé. Pour l'installer, exécutez :
  ```bash
  pip install pillow
  ```

### Utilisation
1. Placez vos images dans le dossier `images brutes`.
2. Double-cliquez sur `run_converter.bat` pour lancer la conversion.
3. Les images converties seront disponibles dans le dossier `images converties`.

### Sécurité
- Assurez-vous que seuls les fichiers d'image sont placés dans le dossier `images brutes`.
- Utilisez un environnement virtuel Python pour isoler les dépendances :
  ```bash
  python -m venv env
  .\env\Scripts\activate
  pip install pillow
  ```