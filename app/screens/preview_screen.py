from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap, QImage
from app.camera import get_preview, capture_photo

class PreviewScreen(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router
        self.count = 1
        self.preview_label = QLabel("Chargement...")
        self.preview_label.setAlignment(Qt.AlignmentFlag(13))

        self.countdown_label = QLabel("")
        self.countdown_label.setStyleSheet("font-size: 50px; color: red;")
        self.countdown_label.setAlignment(Qt.AlignmentFlag(13))

        layout = QVBoxLayout()
        layout.addWidget(self.preview_label)
        layout.addWidget(self.countdown_label)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_preview)

        self.countdown = 5
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)

    def on_enter(self, count=1):
        self.count = count
        self.countdown = 5
        self.countdown_label.setText("")
        self.timer.start(1500)
        QTimer.singleShot(1000, self.start_countdown)

    def update_preview(self):
        image = get_preview()
        if image:
            pixmap = QPixmap.fromImage(image)
            self.preview_label.setPixmap(pixmap.scaled(
                self.preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.preview_label.setText("📸 Appareil non connecté")

    def start_countdown(self):
        self.countdown_timer.start(1000)

    def update_countdown(self):
        if self.countdown > 0:
            self.countdown_label.setText(str(self.countdown))
            self.countdown -= 1
        else:
            self.timer.stop()
            self.countdown_timer.stop()
            filenames = [capture_photo() for _ in range(self.count)]
            self.router.go_to("display", photos=filenames)
