from PyQt5.QtWidgets import QStackedWidget, QDesktopWidget
from PyQt5.QtGui import QPalette, QColor
from app.screens.home_screen import HomeScreen
from app.screens.choice_screen import ChoiceScreen
from app.screens.preview_screen import PreviewScreen
from app.screens.display_screen import DisplayScreen

class Router(QStackedWidget):
    def __init__(self):
        super().__init__()

        screen_rect = QDesktopWidget().screenGeometry()
        self.screen_width = screen_rect.width()
        self.screen_height = screen_rect.height()

        self.setFixedSize(self.screen_width, self.screen_height)
        self.showFullScreen()
        
        # Supprimer les marges internes
        self.setContentsMargins(0, 0, 0, 0)
        
        # Définir la feuille de style globale pour tous les widgets
        # Utilisation correcte de background-image et background-size
        self.setStyleSheet("""
            QStackedWidget {
                background-color: #282828;
                background-image: url('assets/background.jpg');  /* Remplacez par le chemin de votre image */
                background-position: center;
                background-repeat: no-repeat;
                background-size: cover;  /* Utilisez "cover" pour couvrir tout l'espace */
                margin: 0;
                padding: 0;
                border: none;
            }
            
            QWidget {
                color: white;
                margin: 0;
                padding: 0;
                border: none;
            }
            
            QPushButton {
                background-color: #3498db;
                border: none;
                border-radius: 5px;
                padding: 10px;
                color: white;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #2980b9;
            }
            
            QLabel {
                background-color: transparent;  /* Important pour que les labels n'aient pas de fond */
            }
        """)

        self.home = HomeScreen(self)
        self.choice = ChoiceScreen(self)
        self.preview = PreviewScreen(self)
        self.display = DisplayScreen(self)

        self.addWidget(self.home)
        self.addWidget(self.choice)
        self.addWidget(self.preview)
        self.addWidget(self.display)

        self.setCurrentWidget(self.home)
        
        # Stockage des références pour la fermeture propre
        self._active_screen = self.home

    def go_to(self, screen_name, **kwargs):
        """Change l'écran actif et appelle sa méthode on_enter"""
        old_screen = self._active_screen
        
        # Si nous quittons l'écran de prévisualisation, assurons-nous de fermer proprement les ressources
        if old_screen == self.preview and screen_name != "preview":
            if hasattr(self.preview, 'camera_manager'):
                self.preview.camera_manager.stop_preview()
                
        screen = getattr(self, screen_name)
        self._active_screen = screen
        screen.on_enter(**kwargs)
        self.setCurrentWidget(screen)
        
    def closeEvent(self, event):
        """Gère la fermeture propre de l'application"""
        # Fermer la connexion à la caméra si elle est ouverte
        if hasattr(self.preview, 'camera_manager'):
            self.preview.camera_manager.close()
        super().closeEvent(event)