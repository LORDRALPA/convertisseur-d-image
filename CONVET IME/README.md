# Convertisseur d'images

## Description
Application professionnelle pour convertir des images en différents formats. Supporte les formats raster (JPG, PNG, GIF, WebP, etc.) et vectoriels (SVG, PDF).

## Structure du projet
- `converter_gui.py` : Interface graphique principale de l'application.
- `conversion_engine.py` : Moteur de conversion avec support multi-formats.
- `convert_images.py` : Script en ligne de commande pour conversion par dossier.
- `run_converter.bat` : Lanceur pour l'application GUI.
- `Lancer_Convertisseur.vbs` : Lanceur sans fenêtre de console (recommandé).
- `images brutes/` : Dossier contenant les images à convertir.
- `images converties/` : Dossier où les images converties seront enregistrées.

## Installation

### Prérequis
- Python 3.8+ doit être installé.
- Les dépendances nécessaires sont listées ci-dessous.

### Dépendances
- `pillow` : Traitement des images raster
- `pillow-heif` : Support des fichiers HEIC (Apple)
- `PyQt5` : Interface graphique
- `cairosvg` : Conversion SVG vers raster
- `reportlab` : Support PDF

Elles sont déjà installées dans l'environnement virtuel du projet.

## Utilisation

### Interface graphique (recommandée)
1. Double-cliquez sur `Lancer_Convertisseur.vbs` pour lancer l'application.
2. Cliquez sur "📁 Ajouter des images" pour sélectionner les fichiers à convertir.
3. Choisissez le format cible dans le menu déroulant.
4. Consultez les informations et risques de conversion.
5. Cliquez sur "🚀 Convertir" et sélectionnez le dossier de destination.

### Ligne de commande
Pour convertir les images du dossier `images brutes` :
```bash
python convert_images.py
```

## Formats supportés

### Formats raster
- JPG, PNG, GIF, WebP, AVIF, BMP, TIFF, HEIC

### Formats vectoriels
- SVG, PDF, EPS, AI (Adobe Illustrator)

### Formats mixtes
- PSD (Photoshop), ICO

## Types de conversion

### Raster → Raster ✅
Conversion presque toujours possible entre formats image standards.
- **Risque faible** : JPG ↔ PNG, WebP, etc.
- **Risque moyen** : Certaines compressions peuvent causer des pertes

### Vectoriel → Raster ✅
Toujours possible via export ou rendu en haute résolution.
- **Risque faible** : SVG → PNG/JPG
- **Risque moyen** : Formats propriétaires (AI) → PNG/JPG

### Vectoriel ↔ Vectoriel ⚠️
Possible mais avec pertes possibles.
- **Risque moyen** : AI ↔ SVG, EPS ↔ PDF
- Certains effets et polices peuvent être perdus

### Raster → Vectoriel ⚠️
Possible mais complexe, nécessite vectorisation.
- **Risque élevé** : PNG/JPG → SVG
- Fonctionne bien uniquement pour logos simples et icônes

## Informations sur les risques

L'application affiche des indicateurs de risque pour chaque conversion :
- 🟢 **Risque faible** : Conversion standard sans problème majeur
- 🟡 **Risque moyen** : Quelques pertes possibles mais généralement acceptable
- 🔴 **Risque élevé** : Pertes significatives possibles, vérifier le résultat

## Conseils

### Qualité des conversions
- **JPG** : Format avec compression, bon pour photos
- **PNG** : Format sans compression avec transparence, bon pour web
- **WebP** : Excellent compromis pour le web (compression efficace)
- **TIFF** : Préservation maximale de la qualité

### Formats spécifiques
- **HEIC** : Utiliser JPG/PNG pour compatibilité universelle
- **SVG** : Conserver le format vectoriel pour scalabilité
- **PDF** : Bon pour documents, accepte les pages multiples

## Sécurité
- L'application fonctionne dans un environnement virtuel isolé
- Les fichiers source ne sont pas modifiés
- Les conversions sont reversibles (reconvertir au format original)

## Support
Pour les problèmes ou demandes de nouvelles fonctionnalités, consultez la documentation ou créez une issue.