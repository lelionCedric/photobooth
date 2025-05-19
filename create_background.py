#!/usr/bin/env python3

import os
from PIL import Image, ImageDraw, ImageFilter

def create_default_background():
    """Crée une image d'arrière-plan par défaut si elle n'existe pas déjà"""
    
    # Créer le dossier assets s'il n'existe pas
    os.makedirs("assets", exist_ok=True)
    
    background_path = "assets/background.jpg"
    
    # Vérifier si l'image existe déjà
    if os.path.exists(background_path):
        print(f"L'image d'arrière-plan existe déjà à {background_path}")
        return
    
    # Créer une nouvelle image
    width, height = 1200, 800
    image = Image.new("RGB", (width, height), (30, 30, 50))
    
    # Créer un objet de dessin
    draw = ImageDraw.Draw(image)
    
    # Dessiner quelques formes aléatoires pour créer un fond intéressant
    # Cercles et rectangles semi-transparents
    for i in range(50):
        x = i * width // 40
        y = (i % 10) * height // 10
        size = (width + height) // 10
        color = (
            100 + (i * 3) % 155,
            80 + (i * 5) % 175,
            150 + (i * 7) % 105,
            100  # alpha
        )
        draw.ellipse([x, y, x + size, y + size], fill=color)
    
    # Ajouter un flou pour adoucir l'arrière-plan
    image = image.filter(ImageFilter.GaussianBlur(radius=15))
    
    # Assombrir l'image pour un meilleur contraste avec le texte blanc
    darkness = Image.new("RGBA", image.size, (0, 0, 0, 80))
    image = Image.alpha_composite(image.convert("RGBA"), darkness)
    
    # Enregistrer l'image
    image.convert("RGB").save(background_path, "JPEG", quality=90)
    print(f"Image d'arrière-plan créée avec succès à {background_path}")

if __name__ == "__main__":
    create_default_background()