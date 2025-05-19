from PyQt5.QtWidgets import QApplication
from app.router import Router
import sys
import traceback

def exception_hook(exctype, value, tb):
    """Gestionnaire d'exceptions global pour enregistrer les erreurs non capturées"""
    print(''.join(traceback.format_exception(exctype, value, tb)))
    sys.__excepthook__(exctype, value, tb)

def main():
    # Installer le hook d'exception global
    sys.excepthook = exception_hook
    
    # Créer l'application Qt
    app = QApplication(sys.argv)
    
    # Créer et afficher le routeur principal
    router = Router()
    router.show()
    
    # Exécuter la boucle d'événements
    exit_code = app.exec()
    
    # Avant de quitter, s'assurer que les ressources sont libérées
    if hasattr(router.preview, 'camera_manager'):
        router.preview.camera_manager.close()
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()