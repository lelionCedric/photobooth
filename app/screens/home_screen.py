from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class HomeScreen(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel("📸 Photobooth")
        label.setStyleSheet("font-size: 30px;")
        button = QPushButton("Faire une photo")
        button.setStyleSheet("font-size: 20px; padding: 20px;")
        button.clicked.connect(lambda: self.router.go_to("choice"))

        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)

    def on_enter(self, **kwargs):
        pass
