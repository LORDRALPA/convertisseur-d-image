"""
Convertisseur d'Images Pro — Moteur de conversion
Copyright (c) 2026 Théophile TOKRE
Licence : MIT License — voir fichier LICENSE

Fourni « tel quel », sans garantie d'aucune sorte.
"""
import base64
import io
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

try:
    from pillow_heif import register_heif_opener

    register_heif_opener()
except ImportError:
    pass


def _imagemagick_cmd():
    """Retourne le chemin vers la commande ImageMagick, ou None si absent."""
    for cmd in ("magick", "convert"):
        path = shutil.which(cmd)
        if path:
            return cmd
    # Chemins d'installation Windows courants
    for pattern in (
        r"C:\Program Files\ImageMagick*",
    ):
        import glob
        matches = glob.glob(pattern)
        for m in matches:
            candidate = os.path.join(m, "magick.exe")
            if os.path.isfile(candidate):
                return candidate
    return None


def _convert_with_imagemagick(input_path, output_path):
    """Lance ImageMagick pour convertir input_path vers output_path."""
    cmd = _imagemagick_cmd()
    if cmd is None:
        return False, "ImageMagick non trouvé sur ce système"
    try:
        result = subprocess.run(
            [cmd, str(input_path), str(output_path)],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0 and Path(output_path).exists():
            return True, "Conversion réussie (ImageMagick)"
        return False, f"ImageMagick erreur: {result.stderr.strip() or 'inconnue'}"
    except subprocess.TimeoutExpired:
        return False, "ImageMagick timeout"
    except Exception as e:
        return False, f"ImageMagick exception: {e}"

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

RASTER_FORMATS = {fmt for fmt, info in FORMAT_INFO.items() if info["type"] == "raster"}
VECTOR_FORMATS = {fmt for fmt, info in FORMAT_INFO.items() if info["type"] == "vector"}


def _build_conversion_matrix():
    """Construit une matrice complète de conversions (hors identité)."""
    matrix = {}
    for src, src_info in FORMAT_INFO.items():
        for dst, dst_info in FORMAT_INFO.items():
            if src == dst:
                continue

            src_type = src_info["type"]
            dst_type = dst_info["type"]

            risk = "medium"
            info = "Conversion standard"

            if src_type == "raster" and dst_type == "raster":
                risk = "low"
                info = "Conversion raster directe"
                if dst in {"jpg", "webp", "heic", "avif"}:
                    risk = "medium"
                    info = "Compression avec perte possible"
                if src in {"png", "gif", "webp", "ico"} and dst == "jpg":
                    risk = "medium"
                    info = "La transparence sera perdue"
            elif src_type == "vector" and dst_type == "raster":
                risk = "medium"
                info = "Rasterisation du fichier vectoriel"
            elif src_type == "raster" and dst_type == "vector":
                risk = "high"
                info = "Encapsulation raster ou vectorisation simplifiée"
            elif src_type == "vector" and dst_type == "vector":
                risk = "medium"
                info = "Conversion vectorielle via pipeline intermédiaire"
                if src == "pdf" and dst == "svg":
                    risk = "high"
                    info = "Reconstruction SVG approximative"
                if dst == "ai":
                    risk = "high"
                    info = "Export de compatibilité Illustrator (PDF interne)"

            matrix[(src, dst)] = {"possible": True, "risk": risk, "info": info}

    # Overrides métiers plus précis
    matrix[("png", "webp")] = {"possible": True, "risk": "low", "info": "Excellent pour le web"}
    matrix[("jpg", "webp")] = {"possible": True, "risk": "low", "info": "Compression très efficace"}
    matrix[("gif", "webp")] = {"possible": True, "risk": "low", "info": "Animation GIF figée sur la première image"}
    matrix[("heic", "jpg")] = {"possible": True, "risk": "low", "info": "Format Apple converti facilement"}
    matrix[("heic", "png")] = {"possible": True, "risk": "low", "info": "Format Apple converti facilement"}
    matrix[("svg", "pdf")] = {"possible": True, "risk": "low", "info": "Conversion vectorielle directe"}
    matrix[("pdf", "svg")] = {"possible": True, "risk": "high", "info": "SVG reconstruit à partir d'un rendu raster"}
    return matrix


CONVERSION_MATRIX = _build_conversion_matrix()

def detect_format(file_path):
    """Détecte le format d'un fichier."""
    ext = Path(file_path).suffix.lower()
    for fmt, info in FORMAT_INFO.items():
        if ext in info["extensions"]:
            return fmt
    return None

def get_available_conversions(source_format):
    """Retourne les conversions possibles pour un format source."""
    source_format = (source_format or "").lower()
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
        target_format = target_format.lower()

        if target_format in {"jpg", "jpeg", "heic", "avif", "bmp"}:
            # Les formats sans alpha nécessitent un fond opaque.
            if img.mode in ("RGBA", "LA", "P"):
                rgba = img.convert("RGBA")
                bg = Image.new("RGB", rgba.size, (255, 255, 255))
                bg.paste(rgba, mask=rgba.split()[-1])
                img = bg
            else:
                img = img.convert("RGB")

        if target_format == "jpg":
            img.save(output_path, "JPEG", quality=90)
        elif target_format == "png":
            img.save(output_path, "PNG")
        elif target_format == "gif":
            img.convert("P", palette=Image.ADAPTIVE).save(output_path, "GIF")
        elif target_format == "webp":
            img.save(output_path, "WEBP", quality=90)
        elif target_format == "bmp":
            img.save(output_path, "BMP")
        elif target_format == "tiff":
            img.save(output_path, "TIFF")
        elif target_format == "ico":
            icon = img.copy()
            icon.thumbnail((256, 256))
            icon.save(output_path, "ICO")
        elif target_format == "heic":
            img.save(output_path, format="HEIF", quality=90)
        elif target_format == "avif":
            img.save(output_path, format="AVIF", quality=80)
        elif target_format == "psd":
            # Pillow ne sait pas écrire le PSD → fallback ImageMagick
            ok, msg = _convert_with_imagemagick(input_path, output_path)
            if not ok:
                return False, f"Export PSD indisponible ({msg}). Installez ImageMagick pour activer ce format."
            return True, "Conversion réussie (ImageMagick)"
        else:
            return False, f"Format raster cible non géré: {target_format}"

        return True, "Conversion réussie"
    except Exception as e:
        return False, f"Erreur: {str(e)}"


def _svg_wrapper_from_image(img):
    """Construit un SVG contenant une image PNG encodée en base64."""
    png_buffer = io.BytesIO()
    img.save(png_buffer, format="PNG")
    encoded = base64.b64encode(png_buffer.getvalue()).decode("ascii")
    width, height = img.size
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
        f'<image href="data:image/png;base64,{encoded}" width="{width}" height="{height}"/>'
        "</svg>"
    )


def convert_raster_to_vector(input_path, output_path, source_format, target_format):
    """Convertit un raster vers un format vectoriel (encapsulation ou export)."""
    try:
        img = Image.open(input_path)
        target_format = target_format.lower()

        if target_format == "pdf":
            rgb = img.convert("RGB")
            rgb.save(output_path, "PDF", resolution=150.0)
            return True, "Conversion réussie"

        if target_format == "eps":
            rgb = img.convert("RGB")
            rgb.save(output_path, "EPS")
            return True, "Conversion réussie"

        if target_format == "svg":
            svg_content = _svg_wrapper_from_image(img)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(svg_content)
            return True, "Conversion réussie (SVG encapsulé)"

        if target_format == "ai":
            # Fichier AI de compatibilité: on écrit un PDF dans une extension .ai.
            rgb = img.convert("RGB")
            rgb.save(output_path, "PDF", resolution=150.0)
            return True, "Conversion réussie (AI de compatibilité PDF)"

        return False, f"Format vectoriel cible non géré: {target_format}"
    except Exception as e:
        return False, f"Erreur: {str(e)}"

def _extract_png_from_svg_wrapper(svg_path):
    """Extrait le PNG base64 d'un SVG encapsulé (format produit par ce moteur).
    Retourne les données PNG bytes ou None si ce n'est pas un SVG wrapper."""
    import re
    try:
        with open(svg_path, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.search(r'href="data:image/[^;]+;base64,([^"]+)"', content)
        if match:
            return base64.b64decode(match.group(1))
    except Exception:
        pass
    return None


def _rasterize_via_imagemagick(input_path, output_png_path):
    """Utilise ImageMagick pour convertir un vecteur (PDF/EPS/AI/SVG) en PNG."""
    cmd = _imagemagick_cmd()
    if cmd is None:
        return False, "ImageMagick non trouvé"
    try:
        # [0] = première page pour les multi-pages (PDF)
        src = f"{input_path}[0]"
        result = subprocess.run(
            [cmd, "-density", "150", src, output_png_path],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0 and Path(output_png_path).exists():
            return True, "Rendu via ImageMagick"
        return False, f"ImageMagick erreur: {result.stderr.strip() or 'inconnue'}"
    except subprocess.TimeoutExpired:
        return False, "ImageMagick timeout"
    except Exception as e:
        return False, f"ImageMagick exception: {e}"


def convert_vector_to_raster(input_path, output_path, target_format):
    """Convertit une image vectorielle en raster."""
    try:
        source_format = detect_format(input_path)

        # Chemin commun : on travaille sur un PNG intermédiaire
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_png:
            tmp_png_path = tmp_png.name

        try:
            if source_format == "svg":
                # 1) Essayer d'extraire le PNG base64 de notre propre format encapsulé
                png_data = _extract_png_from_svg_wrapper(input_path)
                if png_data is not None:
                    with open(tmp_png_path, "wb") as f:
                        f.write(png_data)
                else:
                    # 2) Essayer cairosvg (nécessite libcairo-2.dll sur Windows)
                    try:
                        import cairosvg
                        cairosvg.svg2png(url=str(input_path), write_to=tmp_png_path)
                    except Exception:
                        # 3) Fallback ImageMagick
                        ok, msg = _rasterize_via_imagemagick(input_path, tmp_png_path)
                        if not ok:
                            return False, f"Impossible de lire le SVG ({msg}). Installez le runtime GTK ou ImageMagick."
            else:
                # PDF, EPS, AI → on essaie dans l'ordre de préférence
                rasterized = False

                # 1) PyMuPDF : gère PDF et AI (= PDF interne) sans Ghostscript
                if source_format in ("pdf", "ai"):
                    try:
                        import fitz  # PyMuPDF
                        doc = fitz.open(str(input_path))
                        page = doc[0]
                        mat = fitz.Matrix(2.0, 2.0)  # 2× zoom = ~150 dpi
                        pix = page.get_pixmap(matrix=mat, alpha=False)
                        pix.save(tmp_png_path)
                        doc.close()
                        rasterized = True
                    except Exception:
                        pass

                # 2) ImageMagick (avec Ghostscript si disponible)
                if not rasterized:
                    ok, msg = _rasterize_via_imagemagick(input_path, tmp_png_path)
                    if ok:
                        rasterized = True

                # 3) Pillow comme dernier recours (EPS + Ghostscript)
                if not rasterized:
                    gs_found = shutil.which("gswin64c") or shutil.which("gswin32c") or shutil.which("gs")
                    if source_format in ("eps", "ai") and not gs_found:
                        return False, (
                            f"Impossible de lire ce fichier {source_format.upper()} : "
                            "ni PyMuPDF, ni ImageMagick+Ghostscript ne sont disponibles. "
                            "Installez Ghostscript (https://ghostscript.com) pour activer ce format."
                        )
                    try:
                        with Image.open(input_path) as img:
                            img.load()
                            rgba = img.convert("RGBA") if img.mode != "RGBA" else img
                            rgba.save(tmp_png_path, "PNG")
                        rasterized = True
                    except Exception as e:
                        return False, f"Impossible de lire la source ({source_format}): {e}"

            if target_format == "png":
                import shutil as _shutil
                _shutil.copy2(tmp_png_path, output_path)
                return True, "Conversion réussie"
            return convert_raster_to_raster(tmp_png_path, output_path, target_format)

        finally:
            if os.path.exists(tmp_png_path):
                os.remove(tmp_png_path)
    except Exception as e:
        return False, f"Erreur: {str(e)}"


def convert_vector_to_vector(input_path, output_path, source_format, target_format):
    """Convertit un format vectoriel vers un autre via chemins directs/fallback."""
    try:
        if source_format == "svg" and target_format == "pdf":
            try:
                import cairosvg
                cairosvg.svg2pdf(url=str(input_path), write_to=str(output_path))
                return True, "Conversion réussie"
            except Exception:
                pass  # cairosvg indisponible → chemin universel ci-dessous

        # Chemin universel: vector → raster (png) → vector cible.
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_png:
            tmp_png_path = tmp_png.name
        try:
            success, message = convert_vector_to_raster(input_path, tmp_png_path, "png")
            if not success:
                return False, message
            return convert_raster_to_vector(tmp_png_path, output_path, "png", target_format)
        finally:
            if os.path.exists(tmp_png_path):
                os.remove(tmp_png_path)
    except Exception as e:
        return False, f"Erreur: {str(e)}"

CREDITS_AUTHOR = "Théophile TOKRE"
CREDITS_SOFTWARE = "Convertisseur d'Images Pro"


def _embed_credits_metadata(output_path, target_format):
    """Injecte la date de conversion et les crédits dans les métadonnées du fichier."""
    from datetime import datetime
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comment = f"Converti le {date_str} | Auteur: {CREDITS_AUTHOR} | Logiciel: {CREDITS_SOFTWARE}"
    fmt = target_format.lower()

    try:
        if fmt in ("jpg", "jpeg", "tiff", "webp"):
            img = Image.open(output_path)
            exif = img.getexif()
            exif[0x010E] = comment          # ImageDescription
            exif[0x013B] = CREDITS_AUTHOR   # Artist
            exif[0x0131] = CREDITS_SOFTWARE  # Software
            exif_bytes = exif.tobytes()
            save_kwargs = {"exif": exif_bytes}
            if fmt in ("jpg", "jpeg"):
                save_kwargs["quality"] = 90
                img.save(output_path, "JPEG", **save_kwargs)
            elif fmt == "tiff":
                img.save(output_path, "TIFF", **save_kwargs)
            elif fmt == "webp":
                save_kwargs["quality"] = 90
                img.save(output_path, "WEBP", **save_kwargs)

        elif fmt == "png":
            from PIL.PngImagePlugin import PngInfo
            img = Image.open(output_path)
            meta = PngInfo()
            meta.add_text("Author", CREDITS_AUTHOR)
            meta.add_text("Software", CREDITS_SOFTWARE)
            meta.add_text("Comment", comment)
            meta.add_text("Creation Time", date_str)
            img.save(output_path, "PNG", pnginfo=meta)

        elif fmt == "svg":
            import re
            with open(output_path, "r", encoding="utf-8") as f:
                content = f.read()
            meta_block = (
                f'\n  <metadata>'
                f'<dc:creator xmlns:dc="http://purl.org/dc/elements/1.1/">{CREDITS_AUTHOR}</dc:creator>'
                f'<dc:date xmlns:dc="http://purl.org/dc/elements/1.1/">{date_str}</dc:date>'
                f'<dc:description xmlns:dc="http://purl.org/dc/elements/1.1/">{CREDITS_SOFTWARE}</dc:description>'
                f'</metadata>\n'
            )
            content = re.sub(r'(<svg[^>]*>)', r'\1' + meta_block, content, count=1)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)

        elif fmt in ("eps", "ai"):
            try:
                with open(output_path, "r", encoding="latin-1") as f:
                    content = f.read()
                lines = content.split("\n", 1)
                ps_comment = f"%% {comment}\n"
                content = lines[0] + "\n" + ps_comment + (lines[1] if len(lines) > 1 else "")
                with open(output_path, "w", encoding="latin-1") as f:
                    f.write(content)
            except Exception:
                pass  # Fichier binaire ou encodage non lisible

    except Exception:
        pass  # Ne jamais bloquer la conversion pour les métadonnées


def convert_image(input_path, output_path, target_format):
    """Convertit une image en détectant automatiquement le type."""
    source_format = detect_format(input_path)
    target_format = (target_format or "").lower()
    
    if not source_format:
        return False, "Format source non reconnu"
    if target_format not in FORMAT_INFO:
        return False, f"Format cible non reconnu: {target_format}"
    if source_format == target_format:
        with open(input_path, "rb") as src_f:
            with open(output_path, "wb") as dst_f:
                dst_f.write(src_f.read())
        return True, "Conversion réussie"

    conversion_rule = CONVERSION_MATRIX.get((source_format, target_format))
    if not conversion_rule or not conversion_rule.get("possible"):
        return False, f"Conversion {source_format} -> {target_format} non autorisée"
    
    source_type = FORMAT_INFO[source_format]["type"]
    target_type = FORMAT_INFO[target_format]["type"]
    
    # Conversions raster → raster
    if source_type == "raster" and target_type == "raster":
        success, message = convert_raster_to_raster(input_path, output_path, target_format)

    # Conversions raster -> vectoriel
    elif source_type == "raster" and target_type == "vector":
        success, message = convert_raster_to_vector(input_path, output_path, source_format, target_format)

    # Conversions vectoriel → raster
    elif source_type == "vector" and target_type == "raster":
        success, message = convert_vector_to_raster(input_path, output_path, target_format)

    # Conversions vectoriel -> vectoriel
    elif source_type == "vector" and target_type == "vector":
        success, message = convert_vector_to_vector(input_path, output_path, source_format, target_format)

    else:
        return False, f"Conversion de {source_type} à {target_type} non supportée"

    if success:
        _embed_credits_metadata(output_path, target_format)
    return success, message
