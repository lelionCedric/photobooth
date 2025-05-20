from PyQt5.QtWidgets import QStackedWidget, QDesktopWidget
from PyQt5.QtGui import QPalette, QColor, QPixmap, QPainter
from PyQt5.QtCore import Qt, QSize
from app.screens.home_screen import HomeScreen
from app.screens.choice_screen import ChoiceScreen
from app.screens.preview_screen import PreviewScreen
from app.screens.display_screen import DisplayScreen

import os

class Router(QStackedWidget):
    def __init__(self):
        super().__init__()

        screen_rect = QDesktopWidget().screenGeometry()
        self.screen_width = screen_rect.width()
        self.screen_height = screen_rect.height()

        self.setFixedSize(self.screen_width, self.screen_height)
        self.showFullScreen()
        
        # Charger et redimensionner l'image de fond
        self._setup_background()

        # Supprimer les marges internes
        self.setContentsMargins(0, 0, 0, 0)
        
        # Définir la feuille de style globale pour tous les widgets
        # Utilisation correcte de background-image et background-size
        self.setStyleSheet("""            
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

    def _setup_background(self):
        """Charge et redimensionne l'image de fond à la taille exacte de l'écran"""
        background_path = './assets/background.jpg'
        
        if not os.path.exists(background_path):
            # Si l'image n'existe pas, utiliser un fond noir simple
            self.setStyleSheet("QStackedWidget { background-color: #000000; }")
            return
            
        # Charger l'image et la redimensionner à la taille exacte de l'écran
        background = QPixmap(background_path)
        if background.isNull():
            self.setStyleSheet("QStackedWidget { background-color: #000000; }")
            return
            
        # Redimensionner l'image à la taille exacte de l'écran
        self.scaled_background = background.scaled(
            QSize(self.screen_width, self.screen_height),
            Qt.AspectRatioMode.IgnoreAspectRatio,  # Pour remplir tout l'écran
            Qt.TransformationMode.SmoothTransformation  # Pour une meilleure qualité
        )
    
    def paintEvent(self, event):
        """Dessine l'image de fond redimensionnée"""
        if hasattr(self, 'scaled_background'):
            painter = QPainter(self)
            painter.drawPixmap(0, 0, self.scaled_background)
        super().paintEvent(event)

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