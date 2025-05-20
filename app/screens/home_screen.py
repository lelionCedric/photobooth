from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QScrollArea, QGridLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap
import os
import glob

class HomeScreen(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        # Configuration de fond transparent pour permettre au fond du parent de s'afficher
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: transparent;")

        # Layout principal horizontal pour diviser l'écran en deux parties
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)  # Espace entre les deux moitiés

        # PARTIE GAUCHE - Galerie de photos
        right_widget = QWidget()
        right_widget.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        right_layout = QVBoxLayout(right_widget)
        
        # Titre pour la galerie
        #gallery_title = QLabel("Photos récentes")
        #gallery_title.setStyleSheet("font-size: 24px; color: white; font-weight: bold; background-color: transparent;")
        #gallery_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #right_layout.addWidget(gallery_title)
        
        # Zone défilante pour les photos
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: transparent; border: none;")
        
        # Widget contenant la grille de photos
        photos_widget = QWidget()
        photos_widget.setStyleSheet("background-color: transparent;")
        self.photos_grid = QGridLayout(photos_widget)
        self.photos_grid.setSpacing(10)
        
        scroll_area.setWidget(photos_widget)
        right_layout.addWidget(scroll_area)
        
        # PARTIE DROITE - Bouton pour prendre une photo
        left_widget = QWidget()
        left_widget.setStyleSheet("background-color: transparent;")
        left_layout = QVBoxLayout(left_widget)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        button = QPushButton("Faire une photo")
        button.setStyleSheet(f"""
            font-size: 30px;
            background-color: rgba(0, 0, 0, 0);
            color: white;
            min-width: 300px;
            min-height: 100px;
            height: {self.router.screen_height};
            width: {self.router.screen_width/2};
        """)
        button.clicked.connect(lambda: self.router.go_to("choice"))
        
        left_layout.addWidget(button, 0, Qt.AlignmentFlag.AlignCenter)
        
        # Ajouter les deux moitiés au layout principal
        main_layout.addWidget(left_widget, 1)  # Partie gauche
        main_layout.addWidget(right_widget, 1)  # Partie droite
        
        self.setLayout(main_layout)

    def on_enter(self, **kwargs):
        """Appelé lorsque l'écran devient actif - chargement des photos récentes"""
        # Effacer la grille de photos existante
        self._clear_photos_grid()
        
        # Charger les photos récentes du dossier photos
        self._load_recent_photos()
    
    def _clear_photos_grid(self):
        """Efface toutes les photos de la grille"""
        while self.photos_grid.count():
            item = self.photos_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def _load_recent_photos(self):
        """Charge les photos récentes du dossier photos"""
        # Obtenir la liste des fichiers jpg dans le dossier photos
        photo_dir = "photos"
        if not os.path.exists(photo_dir):
            os.makedirs(photo_dir, exist_ok=True)
            return
            
        # Trouver tous les fichiers jpg
        photo_files = glob.glob(os.path.join(photo_dir, "*.jpg"))
        
        # Trier par date de modification (la plus récente d'abord)
        photo_files.sort(key=os.path.getmtime, reverse=True)
        
        # Limiter à 12 photos maximum pour la performance
        photo_files = photo_files[:12]
        
        # Taille des miniatures
        thumbnail_size = 150
        
        # Ajouter les photos à la grille
        for i, photo_file in enumerate(photo_files):
            row = i // 3  # 3 photos par ligne
            col = i % 3
            
            photo_label = QLabel()
            photo_label.setFixedSize(QSize(thumbnail_size, thumbnail_size))
            photo_label.setStyleSheet("border: 2px solid white; border-radius: 5px;")
            photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            pixmap = QPixmap(photo_file)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(
                    thumbnail_size, thumbnail_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                photo_label.setPixmap(pixmap)
            else:
                # Si l'image ne peut pas être chargée
                photo_label.setText("?")
                photo_label.setStyleSheet("color: white; border: 2px solid white; border-radius: 5px;")
            
            self.photos_grid.addWidget(photo_label, row, col, Qt.AlignmentFlag.AlignCenter)