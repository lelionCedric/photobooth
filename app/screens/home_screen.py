from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
import os
import glob

class HomeScreen(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Zone titre et bouton
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Titre
        self.title_label = QLabel("Faire une photo")
        self.title_label.setStyleSheet("font-size: 40px; color: white; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Bouton invisible qui couvre toute la fenêtre
        self.invisible_button = QPushButton()
        self.invisible_button.setFlat(True)
        self.invisible_button.setStyleSheet("background-color: transparent; border: none;")
        self.invisible_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.invisible_button.clicked.connect(lambda: self.router.go_to("choice"))
        
        header_layout.addWidget(self.title_label)
        
        # Zone de diaporama
        self.slideshow_label = QLabel()
        self.slideshow_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.slideshow_label.setMinimumSize(600, 400)
        
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.slideshow_label)
        
        # Layout global qui contient le bouton invisible et le contenu principal
        global_layout = QHBoxLayout()
        global_layout.addLayout(main_layout)
        
        self.setLayout(global_layout)
        
        # Timer pour le diaporama
        self.slideshow_timer = QTimer()
        self.slideshow_timer.timeout.connect(self.next_slide)
        self.photo_index = 0
        self.photos = []
        
        # Appliquer le style de fond
        self.setStyleSheet("background-image: url(assets/background.jpg); background-position: center; background-repeat: no-repeat; background-size: cover;")

    def on_enter(self, **kwargs):
        # Rechercher toutes les photos dans le dossier "photos"
        self.photos = self.get_photo_list()
        
        # S'il y a des photos, démarrer le diaporama
        if self.photos:
            self.photo_index = 0
            self.show_current_photo()
            self.slideshow_timer.start(5000)  # 5 secondes par photo
        else:
            self.slideshow_label.clear()
            
        # S'assurer que le bouton invisible couvre toute la fenêtre
        self.invisible_button.setParent(None)  # Retirer d'abord
        self.invisible_button.setFixedSize(self.size())
        self.invisible_button.raise_()  # Mettre au premier plan
        self.invisible_button.show()

    def get_photo_list(self):
        """Récupère la liste des photos dans le dossier photos"""
        # Créer le dossier s'il n'existe pas
        os.makedirs("photos", exist_ok=True)
        
        # Rechercher tous les fichiers jpg
        photos = glob.glob("photos/*.jpg")
        # Trier par date de modification (le plus récent d'abord)
        photos.sort(key=os.path.getmtime, reverse=True)
        return photos

    def next_slide(self):
        """Passe à la diapositive suivante"""
        if not self.photos:
            return
            
        self.photo_index = (self.photo_index + 1) % len(self.photos)
        self.show_current_photo()

    def show_current_photo(self):
        """Affiche la photo actuelle"""
        if not self.photos or self.photo_index >= len(self.photos):
            self.slideshow_label.clear()
            return
            
        photo_path = self.photos[self.photo_index]
        pixmap = QPixmap(photo_path)
        
        if not pixmap.isNull():
            self.slideshow_label.setPixmap(pixmap.scaled(
                self.slideshow_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        else:
            self.slideshow_label.setText("Erreur de chargement de l'image")
            
    def resizeEvent(self, event):
        """Gère le redimensionnement de la fenêtre"""
        super().resizeEvent(event)
        # Redimensionner le bouton invisible pour couvrir toute la fenêtre
        self.invisible_button.setFixedSize(self.size())