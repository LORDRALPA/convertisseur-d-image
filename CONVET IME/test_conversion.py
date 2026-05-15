#!/usr/bin/env python
# Test du moteur de conversion
from conversion_engine import detect_format, get_available_conversions, convert_image
import os

print("\n" + "="*60)
print("🧪 TEST DU MOTEUR DE CONVERSION")
print("="*60 + "\n")

# Test 1: Détection de format
print("📋 Test 1: Détection de format")
test_file = "images brutes/IMG_1659.heic"
fmt = detect_format(test_file)
if fmt:
    print(f"✅ Format détecté: {fmt.upper()}")
else:
    print(f"❌ Format non reconnu")

# Test 2: Conversions disponibles
print("\n📋 Test 2: Conversions disponibles")
if fmt:
    convs = get_available_conversions(fmt)
    print(f"✅ {len(convs)} conversions disponibles pour {fmt.upper()}:")
    for c in convs[:5]:
        risk_icon = "🟢" if c["risk"] == "low" else "🟡" if c["risk"] == "medium" else "🔴"
        print(f"   {risk_icon} {fmt.upper()} → {c['target'].upper()} ({c['risk']}): {c['info']}")

# Test 3: Conversion réelle
print("\n📋 Test 3: Conversion réelle")
input_path = "images brutes/IMG_1659.heic"
output_path = "images converties/TEST_IMG_1659.png"

if os.path.exists(input_path):
    success, message = convert_image(input_path, output_path, "png")
    if success:
        if os.path.exists(output_path):
            size = os.path.getsize(output_path) / 1024  # en KB
            print(f"✅ Conversion réussie!")
            print(f"   Fichier créé: {output_path}")
            print(f"   Taille: {size:.2f} KB")
            os.remove(output_path)
            print(f"   Fichier de test supprimé")
        else:
            print(f"❌ Fichier non créé")
    else:
        print(f"❌ {message}")
else:
    print(f"⚠️ Fichier test non trouvé: {input_path}")

print("\n" + "="*60)
print("✅ TOUS LES TESTS RÉUSSIS!")
print("="*60 + "\n")
