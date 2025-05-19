from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer, Qt, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage, QPainter, QFont, QColor, QPen
from app.camera import CameraManager
import os

class PreviewScreen(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router
        self.count = 1
        self.camera_manager = CameraManager()
        
        # Configuration de l'interface utilisateur
        self.preview_label = QLabel("Chargement...")
        self.preview_label.setAlignment(Qt.AlignmentFlag(13))  # Center
        self.preview_label.setMinimumSize(600, 400)

        layout = QVBoxLayout()
        layout.addWidget(self.preview_label)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Timer pour le décompte
        self.countdown = 5
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        
        # Connecter les signaux de la caméra
        self.camera_manager.preview_ready.connect(self.on_preview_image)
        self.camera_manager.capture_ready.connect(self.on_photo_captured)
        self.camera_manager.capture_error.connect(self.on_capture_error)
        
        # Appliquer le style de fond
        self.setStyleSheet("background-image: url(assets/background.jpg); background-position: center; background-repeat: no-repeat; background-size: cover;")

    def on_enter(self, count=1):
        """Appelé lorsque l'écran devient actif"""
        self.count = count
        self.countdown = 5
        self.preview_label.setText("Chargement de l'aperçu...")
        
        # Démarrer l'aperçu en continu
        self.camera_manager.start_preview(300)  # Rafraîchissement rapide pour une expérience fluide
        QTimer.singleShot(1000, self.start_countdown)

    def start_countdown(self):
        """Démarre le compte à rebours"""
        self.countdown_timer.start(1000)

    def update_countdown(self):
        """Met à jour le compte à rebours et capture une photo à la fin"""
        if self.countdown > 0:
            self.countdown -= 1
        else:
            self.countdown_timer.stop()
            self.camera_manager.stop_preview()
            self.capture_photos()

    def capture_photos(self):
        """Capture le nombre demandé de photos"""
        self.filenames = []
        self.remaining_captures = self.count
        self.capture_next_photo()

    def capture_next_photo(self):
        """Capture la prochaine photo dans la séquence"""
        if self.remaining_captures > 0:
            self.camera_manager.capture_photo()
        
    @pyqtSlot(QImage)
    def on_preview_image(self, image):
        """Appelé lorsqu'une image d'aperçu est disponible"""
        # Créer une copie de l'image pour pouvoir y dessiner
        preview_image = QImage(image)
        
        # Créer un peintre pour dessiner sur l'image
        painter = QPainter(preview_image)
        
        # Configurer la police pour le texte du décompte
        font = QFont("Arial", 120, QFont.Weight.Bold)
        painter.setFont(font)
        
        # Dessiner le texte du décompte avec une ombre pour meilleure lisibilité
        # D'abord l'ombre
        painter.setPen(QPen(QColor(0, 0, 0, 180)))
        painter.drawText(preview_image.rect().adjusted(4, 4, 4, 4), Qt.AlignmentFlag.AlignCenter, str(self.countdown + 1 if self.countdown_timer.isActive() else ""))
        
        # Ensuite le texte en blanc
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.drawText(preview_image.rect(), Qt.AlignmentFlag.AlignCenter, str(self.countdown + 1 if self.countdown_timer.isActive() else ""))
        
        # Terminer la peinture
        painter.end()
        
        # Afficher l'image modifiée
        pixmap = QPixmap.fromImage(preview_image)
        self.preview_label.setPixmap(pixmap.scaled(
            self.preview_label.size(), 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation))

    @pyqtSlot(str)
    def on_photo_captured(self, filename):
        """Appelé lorsqu'une photo est capturée avec succès"""
        self.filenames.append(filename)
        self.remaining_captures -= 1
        
        if self.remaining_captures > 0:
            # S'il reste des photos à prendre, attendre un moment puis prendre la suivante
            QTimer.singleShot(500, self.capture_next_photo)
        else:
            # Toutes les photos ont été prises, passer à l'écran d'affichage
            self.router.go_to("display", photos=self.filenames)

    @pyqtSlot(str)
    def on_capture_error(self, error_message):
        """Gère les erreurs de capture"""
        self.preview_label.setText(f"Erreur de capture: {error_message}")
        # Retourner à l'écran d'accueil après un délai
        QTimer.singleShot(3000, lambda: self.router.go_to("home"))