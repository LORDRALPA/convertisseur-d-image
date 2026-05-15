"""
Test de conversion exhaustif — Champ des possibles
Convertit chaque fichier source vers tous les formats supportés.
Résultats organisés par format cible dans :
  D:/DEV/CONVET IME/test images/champ des possibles/{format}/
"""
import os
import sys
from pathlib import Path

# S'assurer que le moteur est importable depuis ce dossier
sys.path.insert(0, str(Path(__file__).parent))

from conversion_engine import detect_format, get_available_conversions, convert_image, FORMAT_INFO

SOURCE_DIR = Path("D:/DEV/CONVET IME/test images")
OUTPUT_ROOT = Path("D:/DEV/CONVET IME/test images/champ des possibles")

# Créer les sous-dossiers par format cible
for fmt in FORMAT_INFO:
    (OUTPUT_ROOT / fmt).mkdir(parents=True, exist_ok=True)

# Collecter les fichiers sources (hors sous-dossiers)
source_files = [f for f in SOURCE_DIR.iterdir() if f.is_file()]
source_files.sort()

print(f"=== CHAMP DES POSSIBLES ===")
print(f"Sources trouvées : {len(source_files)} fichier(s)")
print(f"Dossier de sortie : {OUTPUT_ROOT}\n")

ok_count = 0
fail_count = 0
skip_count = 0
failures = []

for src_file in source_files:
    src_format = detect_format(str(src_file))
    if not src_format:
        print(f"[SKIP] {src_file.name} — format non reconnu")
        skip_count += 1
        continue

    conversions = get_available_conversions(src_format)
    targets = [c["target"] for c in conversions]

    print(f"\n{'─'*60}")
    print(f"SOURCE : {src_file.name}  ({src_format.upper()}) → {len(targets)} cibles")
    print(f"{'─'*60}")

    for target_fmt in sorted(targets):
        ext = FORMAT_INFO[target_fmt]["extensions"][0]
        out_name = f"{src_file.stem}__{src_format}_vers_{target_fmt}{ext}"
        out_path = OUTPUT_ROOT / target_fmt / out_name

        success, message = convert_image(str(src_file), str(out_path), target_fmt)

        size_str = ""
        if success and out_path.exists():
            size_kb = round(out_path.stat().st_size / 1024, 1)
            size_str = f"({size_kb} KB)"

        status = "OK  " if success else "FAIL"
        print(f"  [{status}] → {target_fmt.upper():<6} {size_str:<14} {message if not success else ''}")

        if success:
            ok_count += 1
        else:
            fail_count += 1
            failures.append((src_file.name, target_fmt, message))

print(f"\n{'='*60}")
print(f"RÉSULTAT FINAL")
print(f"{'='*60}")
print(f"  ✅ Réussies : {ok_count}")
print(f"  ❌ Échouées : {fail_count}")
print(f"  ⏭  Ignorées : {skip_count}")
print(f"  Total      : {ok_count + fail_count + skip_count}")

if failures:
    print(f"\nÉCHECS DÉTAILLÉS :")
    for src, tgt, msg in failures:
        print(f"  {src} → {tgt.upper()} : {msg}")

print(f"\nFichiers organisés dans : {OUTPUT_ROOT}")
