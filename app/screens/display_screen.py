from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

class DisplayScreen(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # Layout pour les photos
        self.photo_grid = QGridLayout()
        self.photo_grid.setSpacing(20)
        
        self.layout.addLayout(self.photo_grid)
        self.setLayout(self.layout)
        
        # Appliquer le style de fond
        self.setStyleSheet("background-image: url(assets/background.jpg); background-position: center; background-repeat: no-repeat; background-size: cover;")

    def on_enter(self, photos=[]):
        # Effacer toutes les photos précédentes
        for i in reversed(range(self.photo_grid.count())):
            item = self.photo_grid.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()
        
        # Afficher les nouvelles photos
        if len(photos) == 1:
            # Une seule photo -> Affichage grand format
            label = QLabel()
            pixmap = QPixmap(photos[0])
            
            if not pixmap.isNull():
                label.setPixmap(pixmap.scaled(
                    600, 450,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                ))
                self.photo_grid.addWidget(label, 0, 0, Qt.AlignmentFlag.AlignCenter)
        else:
            # Multiple photos -> Grille 2x2
            rows = 2
            cols = 2
            for i, path in enumerate(photos):
                row = i // cols
                col = i % cols
                
                label = QLabel()
                pixmap = QPixmap(path)
                
                if not pixmap.isNull():
                    label.setPixmap(pixmap.scaled(
                        300, 225,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    ))
                    self.photo_grid.addWidget(label, row, col, Qt.AlignmentFlag.AlignCenter)

        # Retour à l'accueil après 5 secondes
        QTimer.singleShot(5000, lambda: self.router.go_to("home"))