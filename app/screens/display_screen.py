from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer

class DisplayScreen(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag(13))
        self.setLayout(self.layout)

    def on_enter(self, photos=[]):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()

        for path in photos:
            label = QLabel()
            pixmap = QPixmap(path)
            label.setPixmap(pixmap.scaled(400, 300, Qt.KeepAspectRatio))
            self.layout.addWidget(label)

        QTimer.singleShot(5000, lambda: self.router.go_to("home"))
