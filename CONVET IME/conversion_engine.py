"""
Moteur de conversion d'images avec support pour formats raster et vectoriels.
"""
import os
from pathlib import Path
from PIL import Image

try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass

# Dictionnaire des formats supportés et leurs caractéristiques
FORMAT_INFO = {
    # Formats raster
    "jpg": {"type": "raster", "name": "JPEG", "extensions": [".jpg", ".jpeg"]},
    "png": {"type": "raster", "name": "PNG", "extensions": [".png"]},
    "gif": {"type": "raster", "name": "GIF", "extensions": [".gif"]},
    "webp": {"type": "raster", "name": "WebP", "extensions": [".webp"]},
    "bmp": {"type": "raster", "name": "BMP", "extensions": [".bmp"]},
    "tiff": {"type": "raster", "name": "TIFF", "extensions": [".tiff", ".tif"]},
    "heic": {"type": "raster", "name": "HEIC", "extensions": [".heic"]},
    "avif": {"type": "raster", "name": "AVIF", "extensions": [".avif"]},
    
    # Formats vectoriels
    "svg": {"type": "vector", "name": "SVG", "extensions": [".svg"]},
    "pdf": {"type": "vector", "name": "PDF", "extensions": [".pdf"]},
    "eps": {"type": "vector", "name": "EPS", "extensions": [".eps"]},
    "ai": {"type": "vector", "name": "Adobe Illustrator", "extensions": [".ai"]},
    
    # Formats mixtes
    "psd": {"type": "raster", "name": "Photoshop", "extensions": [".psd"]},
    "ico": {"type": "raster", "name": "ICO", "extensions": [".ico"]},
}

# Informations sur les conversions et leurs risques
CONVERSION_MATRIX = {
    # Raster → Raster
    ("jpg", "png"): {"possible": True, "risk": "medium", "info": "La transparence sera perdue"},
    ("png", "jpg"): {"possible": True, "risk": "medium", "info": "La transparence sera perdue"},
    ("png", "webp"): {"possible": True, "risk": "low", "info": "Excellent pour le web"},
    ("jpg", "webp"): {"possible": True, "risk": "low", "info": "Compression très efficace"},
    ("webp", "png"): {"possible": True, "risk": "low", "info": "Conversion directe"},
    ("webp", "jpg"): {"possible": True, "risk": "low", "info": "Conversion directe"},
    ("gif", "webp"): {"possible": True, "risk": "low", "info": "Meilleur format pour animations"},
    ("gif", "png"): {"possible": True, "risk": "low", "info": "Animation perdue"},
    ("heic", "jpg"): {"possible": True, "risk": "low", "info": "Format Apple converti facilement"},
    ("heic", "png"): {"possible": True, "risk": "low", "info": "Format Apple converti facilement"},
    ("bmp", "png"): {"possible": True, "risk": "low", "info": "Compression meilleure"},
    ("tiff", "jpg"): {"possible": True, "risk": "medium", "info": "Perte de qualité possible"},
    ("jpg", "tiff"): {"possible": True, "risk": "low", "info": "Préservation meilleure"},
    
    # Vectoriel → Raster
    ("svg", "png"): {"possible": True, "risk": "low", "info": "Export simple"},
    ("svg", "jpg"): {"possible": True, "risk": "low", "info": "Export simple"},
    ("pdf", "png"): {"possible": True, "risk": "low", "info": "Rendu page par page"},
    ("pdf", "jpg"): {"possible": True, "risk": "low", "info": "Rendu page par page"},
    ("eps", "png"): {"possible": True, "risk": "medium", "info": "Peut nécessiter conversion intermédiaire"},
    ("eps", "jpg"): {"possible": True, "risk": "medium", "info": "Peut nécessiter conversion intermédiaire"},
    ("ai", "png"): {"possible": True, "risk": "high", "info": "Format propriétaire Adobe"},
    ("ai", "jpg"): {"possible": True, "risk": "high", "info": "Format propriétaire Adobe"},
    ("psd", "png"): {"possible": True, "risk": "medium", "info": "Les calques seront fusionnés"},
    ("psd", "jpg"): {"possible": True, "risk": "medium", "info": "Les calques seront fusionnés"},
    
    # Vectoriel → Vectoriel
    ("svg", "pdf"): {"possible": True, "risk": "medium", "info": "Certains effets peuvent être perdus"},
    ("pdf", "svg"): {"possible": True, "risk": "high", "info": "Vectorisation peut être imparfaite"},
    ("eps", "svg"): {"possible": True, "risk": "medium", "info": "Pertes possibles d'effets"},
    ("ai", "svg"): {"possible": True, "risk": "medium", "info": "Polices peuvent ne pas être intégrées"},
    
    # Raster → Vectoriel (difficile)
    ("png", "svg"): {"possible": True, "risk": "high", "info": "Nécessite vectorisation (résultat variable)"},
    ("jpg", "svg"): {"possible": True, "risk": "high", "info": "Nécessite vectorisation (résultat variable)"},
    ("gif", "svg"): {"possible": True, "risk": "high", "info": "Nécessite vectorisation (résultat variable)"},
    
    # Autres conversions
    ("ico", "png"): {"possible": True, "risk": "low", "info": "Conversion directe"},
    ("png", "ico"): {"possible": True, "risk": "low", "info": "Petite résolution recommandée"},
    ("avif", "jpg"): {"possible": True, "risk": "low", "info": "Format moderne converti"},
}

def detect_format(file_path):
    """Détecte le format d'un fichier."""
    ext = Path(file_path).suffix.lower()
    for fmt, info in FORMAT_INFO.items():
        if ext in info["extensions"]:
            return fmt
    return None

def get_available_conversions(source_format):
    """Retourne les conversions possibles pour un format source."""
    conversions = []
    for (src, dst), info in CONVERSION_MATRIX.items():
        if src == source_format and info["possible"]:
            conversions.append({
                "target": dst,
                "name": FORMAT_INFO[dst]["name"],
                "risk": info["risk"],
                "info": info["info"]
            })
    return conversions

def convert_raster_to_raster(input_path, output_path, target_format):
    """Convertit une image raster en un autre format raster."""
    try:
        img = Image.open(input_path)
        
        # Conversion RGB pour JPEG si nécessaire
        if target_format == "jpg":
            if img.mode in ("RGBA", "LA", "P"):
                rgb_img = Image.new("RGB", img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
                rgb_img.save(output_path, "JPEG", quality=90)
            else:
                img.save(output_path, "JPEG", quality=90)
        else:
            img.save(output_path, FORMAT_INFO[target_format]["name"])
        
        return True, "Conversion réussie"
    except Exception as e:
        return False, f"Erreur: {str(e)}"

def convert_vector_to_raster(input_path, output_path, target_format):
    """Convertit une image vectorielle en raster."""
    try:
        if input_path.lower().endswith(".svg"):
            import cairosvg
            if target_format == "png":
                cairosvg.svg2png(url=input_path, write_to=output_path)
            elif target_format == "jpg":
                temp_png = output_path.replace(".jpg", "_temp.png")
                cairosvg.svg2png(url=input_path, write_to=temp_png)
                img = Image.open(temp_png)
                rgb_img = Image.new("RGB", img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
                rgb_img.save(output_path, "JPEG", quality=90)
                os.remove(temp_png)
        else:
            return False, "Format vectoriel non supporté directement"
        
        return True, "Conversion réussie"
    except Exception as e:
        return False, f"Erreur: {str(e)}"

def convert_image(input_path, output_path, target_format):
    """Convertit une image en détectant automatiquement le type."""
    source_format = detect_format(input_path)
    
    if not source_format:
        return False, "Format source non reconnu"
    
    source_type = FORMAT_INFO[source_format]["type"]
    target_type = FORMAT_INFO[target_format]["type"]
    
    # Conversions raster → raster
    if source_type == "raster" and target_type == "raster":
        return convert_raster_to_raster(input_path, output_path, target_format)
    
    # Conversions vectoriel → raster
    elif source_type == "vector" and target_type == "raster":
        return convert_vector_to_raster(input_path, output_path, target_format)
    
    # Autres conversions
    else:
        return False, f"Conversion de {source_type} à {target_type} non supportée"
