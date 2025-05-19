from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage
from app.camera import CameraManager

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

        self.countdown_label = QLabel("")
        self.countdown_label.setStyleSheet("font-size: 50px; color: red;")
        self.countdown_label.setAlignment(Qt.AlignmentFlag(13))  # Center

        layout = QVBoxLayout()
        layout.addWidget(self.preview_label)
        layout.addWidget(self.countdown_label)
        self.setLayout(layout)

        # Timer pour le décompte
        self.countdown = 5
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        
        # Connecter les signaux de la caméra
        self.camera_manager.preview_ready.connect(self.on_preview_image)
        self.camera_manager.capture_ready.connect(self.on_photo_captured)
        self.camera_manager.capture_error.connect(self.on_capture_error)

    def on_enter(self, count=1):
        """Appelé lorsque l'écran devient actif"""
        self.count = count
        self.countdown = 5
        self.countdown_label.setText("")
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
            self.countdown_label.setText(str(self.countdown))
            self.countdown -= 1
        else:
            self.countdown_timer.stop()
            self.camera_manager.stop_preview()
            self.countdown_label.setText("📸")
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
        pixmap = QPixmap.fromImage(image)
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
        self.countdown_label.setText("Erreur")
        self.preview_label.setText(f"Erreur de capture: {error_message}")
        # Retourner à l'écran d'accueil après un délai
        QTimer.singleShot(3000, lambda: self.router.go_to("home"))