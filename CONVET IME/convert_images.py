import os
from PIL import Image

try:
    from pillow_heif import register_heif_opener
except ImportError:
    register_heif_opener = None

def convert_images_to_jpeg(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if register_heif_opener is not None:
        register_heif_opener()

    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)

        if os.path.isfile(input_path):
            try:
                with Image.open(input_path) as img:
                    output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.jpeg")
                    img.convert("RGB").save(output_path, "JPEG")
                    print(f"Converted: {filename} -> {output_path}")
            except Exception as e:
                print(f"Failed to convert {filename}: {e}")

if __name__ == "__main__":
    input_folder = "D:\\DEV\\CONVET IME\\images brutes"
    output_folder = "D:\\DEV\\CONVET IME\\images converties"
    convert_images_to_jpeg(input_folder, output_folder)