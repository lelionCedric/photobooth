from PyQt5.QtWidgets import QApplication
from app.router import Router
import sys
import traceback
import os
from pathlib import Path

def exception_hook(exctype, value, tb):
    """Gestionnaire d'exceptions global pour enregistrer les erreurs non capturées"""
    print(''.join(traceback.format_exception(exctype, value, tb)))
    sys.__excepthook__(exctype, value, tb)

def ensure_assets_exist():
    """S'assurer que les dossiers et fichiers nécessaires existent"""
    # Créer les dossiers nécessaires
    os.makedirs("assets", exist_ok=True)
    os.makedirs("photos", exist_ok=True)
    
    # Vérifier si l'image d'arrière-plan existe
    background_path = "./assets/background.jpg"
    if not os.path.exists(background_path):
        try:
            # Essayer d'importer et d'exécuter le script de création de fond
            from create_background import create_default_background
            create_default_background()
        except ImportError:
            print("Script de création de fond introuvable. Veuillez créer manuellement une image à assets/background.jpg")
        except Exception as e:
            print(f"Erreur lors de la création du fond: {e}")
            print("Veuillez créer manuellement une image à assets/background.jpg")

def main():
    # Installer le hook d'exception global
    sys.excepthook = exception_hook
    
    # S'assurer que les ressources nécessaires existent
    ensure_assets_exist()
    
    # Créer l'application Qt
    app = QApplication(sys.argv)
    
    # Créer et afficher le routeur principal
    router = Router()
    router.setWindowTitle("Photobooth")
    router.show()
    
    # Exécuter la boucle d'événements
    exit_code = app.exec()
    
    # Avant de quitter, s'assurer que les ressources sont libérées
    if hasattr(router.preview, 'camera_manager'):
        router.preview.camera_manager.close()
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()