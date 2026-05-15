# ⚡ Convertisseur d'Images Pro

> **Le convertisseur d'images open source le plus complet, portable et sexy.**

![Hero banner](https://user-images.githubusercontent.com/placeholder/banner-convertpro.png)

- **14 formats** : JPG, PNG, WEBP, BMP, GIF, TIFF, ICO, PSD, HEIC, AVIF, SVG, PDF, AI, EPS
- **546 combinaisons** source→cible
- **Standalone** : un dossier à zipper, un double-clic, c'est prêt
- **100% local** : aucune image n'est envoyée sur le cloud
- **Licence MIT** : gratuit, open source, réutilisable

---

## 🚀 Fonctionnalités principales

- Conversion multi-fichiers ultra-rapide (thread séparé)
- Interface graphique PyQt5 moderne et intuitive
- Indicateur de risque pour chaque conversion (vert/orange/rouge)
- Métadonnées et crédits injectés dans chaque fichier produit
- Dialogue « À propos » avec licence et mentions légales
- Test automatique à l'installation (standalone)
- Portabilité totale (aucun chemin fixe, aucun setup admin)

---

## 🎨 Formats supportés

| Raster         | Pro              | Vectoriel      |
|----------------|------------------|----------------|
| JPG, PNG, WEBP | PSD, HEIC, AVIF  | SVG, PDF, AI, EPS |
| BMP, GIF, TIFF, ICO |              |                |

---

## 🛠️ Stack technique

- **Python 3.8+**
- **PyQt5 5.15.11**
- **Pillow ≥ 9.0**
- **pillow-heif** (HEIC/AVIF)
- **PyMuPDF** (PDF/AI)
- **ImageMagick** (PSD/EPS/PDF fallback)
- **cairosvg** (optionnel, SVG)

---

## 📦 Version standalone

1. **Téléchargez** le dossier ou le zip
2. **Double-cliquez** sur `LANCER.bat`
3. L'application vérifie l'environnement, installe les dépendances si besoin, effectue un test automatique, puis démarre l'interface graphique

> **Aucune installation, aucun droit admin requis.**

---

## 📊 Métriques clés

| Formats | Combinaisons | Tests OK | Lignes de code | Taille distrib | Licence |
|---------|--------------|----------|----------------|---------------|---------|
| 14      | 546          | 182/195  | 1191           | 270 Ko        | MIT     |

---

## 🔥 Démo visuelle

> Pour une présentation sexy et interactive, consultez la [landing page HTML](CONVET%20IME/presentation.html) (à héberger sur GitHub Pages pour un rendu optimal).

---

## 📄 Rapport technique

- [Rapport de développement complet (.docx)](CONVET%20IME/RAPPORT_DEVELOPPEMENT.docx)

---

## 👨‍💻 Auteur

- Théophile TOKRE — [GitHub](https://github.com/LORDRALPA)

---

## 🌐 GitHub Pages

> La page de présentation sexy sera bientôt disponible ici :
> https://lordralpa.github.io/convertisseur-d-image/presentation.html

---

## Licence

MIT — libre, open source, réutilisable sans restriction.
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