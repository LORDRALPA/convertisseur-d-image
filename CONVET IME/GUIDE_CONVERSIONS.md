# Guide Complet des Conversions d'Images

## 1️⃣ Conversions Raster ↔ Raster (Facile) ✅

### Formats supportés
- **Lossy (compression avec pertes)** : JPG, WebP, AVIF
- **Lossless (sans compression)** : PNG, GIF, TIFF, BMP, HEIC

### Matrice de compatibilité

| De | Vers | Risk | Remarque |
|---|---|---|---|
| JPG | PNG | 🟡 Moyen | Pas de transparence récupérée |
| PNG | JPG | 🟡 Moyen | Transparence perdue |
| PNG | WebP | 🟢 Faible | Très bon pour web |
| JPG | WebP | 🟢 Faible | Compression efficace |
| WebP | PNG/JPG | 🟢 Faible | Conversion directe |
| GIF | WebP | 🟢 Faible | Meilleur pour animations |
| HEIC | JPG/PNG | 🟢 Faible | Format Apple |
| TIFF | JPG | 🟡 Moyen | Perte de qualité possible |

### Conseils
- **JPG** : Utilisez pour les photos (compression équilibrée)
- **PNG** : Utilisez pour web avec transparence
- **WebP** : Meilleur choix pour web (compression optimale)
- **TIFF** : Archivage de qualité (fichiers lourds)

---

## 2️⃣ Vectoriel → Raster (Toujours possible) ✅

### Formats supportés en input
- SVG, PDF, EPS, AI (Adobe Illustrator)

### Formats supportés en output
- PNG, JPG, GIF, BMP, TIFF

### Matrice de compatibilité

| De | Vers | Risk | Remarque |
|---|---|---|---|
| SVG | PNG | 🟢 Faible | Export simple en haute résolution |
| SVG | JPG | 🟢 Faible | Export simple |
| PDF | PNG | 🟢 Faible | Rendu page par page |
| PDF | JPG | 🟢 Faible | Rendu page par page |
| EPS | PNG | 🟡 Moyen | Peut nécessiter conversion intermédiaire |
| AI | PNG | 🔴 Élevé | Format propriétaire Adobe |
| PSD | PNG | 🟡 Moyen | Les calques seront fusionnés |

### Avantages
- ✅ Rendu en haute résolution
- ✅ Contrôle de la qualité
- ✅ Scalabilité jusqu'à conversion

### Désavantages
- ⚠️ Perte de scalabilité après conversion
- ⚠️ Augmentation de la taille de fichier
- ⚠️ Format propriétaire peut poser problème

---

## 3️⃣ Vectoriel ↔ Vectoriel (Souvent possible) ⚠️

### Formats supportés
- SVG, PDF, EPS, AI

### Matrice de compatibilité

| De | Vers | Risk | Remarque |
|---|---|---|---|
| SVG | PDF | 🟡 Moyen | Certains effets perdus |
| PDF | SVG | 🔴 Élevé | Vectorisation imparfaite |
| EPS | SVG | 🟡 Moyen | Pertes possibles d'effets |
| AI | SVG | 🟡 Moyen | Polices peuvent ne pas être intégrées |
| PDF | EPS | 🟡 Moyen | Compatible mais parfois imparfait |

### Risques courants
- 🔴 **Polices non intégrées** : Le texte peut ne pas s'afficher correctement
- 🔴 **Effets Illustrator** : Dégradés, ombres, etc. peuvent disparaître
- 🔴 **Transparences** : Peuvent être modifiées
- 🔴 **Calques** : Peuvent être fusionnés

### Bonnes pratiques
1. Convertir PDF → SVG
   - Utiliser Adobe Illustrator si résultat crucial
   - Vectoriser manuellement si possible
   
2. Convertir SVG → PDF
   - Incorporer les polices si possible
   - Exporter en PDF haute résolution
   
3. Convertir AI → SVG
   - Exporter les calques vectoriels uniquement
   - Incorporer les polices

---

## 4️⃣ Raster → Vectoriel (Complexe) ⚠️⚠️⚠️

### Formats supportés en input
- PNG, JPG, GIF, BMP, TIFF

### Formats supportés en output
- SVG, PDF, EPS

### Processus
1. **Automatique** (simple mais imparfait)
   - Utilise l'algorithme de vectorisation
   - Rapide mais qualité variable
   - Bon pour logos simples

2. **Manuel** (complexe mais précis)
   - Tracer les contours manuellement
   - Utiliser des outils comme Illustrator
   - Résultat plus propre

### Matrice de compatibilité

| De | Vers | Risk | Remarque |
|---|---|---|---|
| PNG | SVG | 🔴 Élevé | Nécessite vectorisation |
| JPG | SVG | 🔴 Élevé | Nécessite vectorisation |
| GIF | SVG | 🔴 Élevé | Nécessite vectorisation |

### Cas d'usage
✅ **Fonctionne bien pour :**
- Logos simples
- Icônes
- Dessins avec peu de couleurs
- Schémas simples

🚫 **Mauvais pour :**
- Photos
- Images détaillées
- Gradients complexes
- Scans de documents

---

## 5️⃣ Formats Spéciaux

### RAW (Fichiers appareil photo)
```
CR2, NEF, ARW → JPG, PNG, TIFF, DNG (avec développement)
```
- Nécessite Adobe Lightroom, Photoshop, ou RawTherapee
- Développement recommandé avant conversion

### ICO (Icônes Windows)
```
PNG/JPG → ICO (facile)
ICO → PNG (possible)
```
- Format petit (généralement 16x16, 32x32, 64x64)
- PNG recommandé pour source

### HEIC (Apple)
```
HEIC → JPG/PNG (facile) ✅
JPG → HEIC (possible mais peu utilisé)
```
- Format moderne mais pas universellement supporté
- Convertir en JPG/PNG pour compatibilité

---

## Tableau Récapitulatif par Cas d'Usage

### 📱 Pour le Web
```
Source → PNG/WebP (recommandé)
- Compression : WebP > PNG > JPG
- Transparence : PNG ou WebP
- Animations : WebP > GIF
```

### 🖨️ Pour l'Impression
```
Source → TIFF/PDF en haute résolution
- Couleurs : CMYK si possible
- Résolution : 300 DPI minimum
- Format : PDF pour mise en page
```

### 🎨 Pour le Design
```
Source → SVG (vectoriel préservé)
- Scalabilité infinie
- Éditable dans Illustrator/Inkscape
- Léger
```

### 📱 Pour les Réseaux Sociaux
```
Source → JPG/PNG compressé
- Facebook : JPG
- Instagram : JPG ou PNG
- Twitter : JPG
- LinkedIn : PNG de préférence
```

### 🎯 Pour l'Archivage
```
Source → TIFF ou PDF
- Qualité maximale
- Longévité du format
- Taille considérable
```

---

## ⚠️ Checklist de Conversion

Avant de convertir, vérifiez :

- [ ] Format source reconnu
- [ ] Format cible supporté
- [ ] Niveau de risque acceptable
- [ ] Résolution suffisante (raster)
- [ ] Couleurs appropriées (CMYK vs RGB)
- [ ] Transparence gérée (si nécessaire)
- [ ] Polices intégrées (si vectoriel)
- [ ] Espace disque suffisant

---

## 🚀 Conseils Avancés

### Optimisation de la taille
```
PNG → WebP : -30% à -50% plus petit
JPG → WebP : -25% à -35% plus petit
GIF → WebP : -60% à -80% plus petit
```

### Qualité maximale
```
Raster → Toujours convertir PNG/TIFF en dernier
Vectoriel → Convertir en vecteur si possible
Mixed → Rester en format mixte (PSD)
```

### Reversibilité
```
⚠️ JPG → PNG : Information perdue (non reversible)
✅ PNG → JPG → PNG : Reversible mais dégradation
✅ SVG → PNG → SVG : Possible mais imparfait
```

---

## Support et Erreurs

### Erreurs courantes

1. **"Polices manquantes"** (vectoriel)
   - Incorporer les polices avant conversion
   - Utiliser polices système seulement

2. **"Transparence perdue"** (raster)
   - PNG → JPG : Normal et irréversible
   - Utiliser PNG pour transparence

3. **"Qualité dégradée"** (raster)
   - Vérifier compression JPG
   - Augmenter résolution source
   - Utiliser PNG lossless

4. **"Format non supporté"**
   - Convertir d'abord en format intermédiaire
   - Ou utiliser logiciel spécialisé (Adobe)
