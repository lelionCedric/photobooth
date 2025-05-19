from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt

class ChoiceScreen(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel("Combien de photos ?")
        label.setStyleSheet("font-size: 24px;")
        btn1 = QPushButton("1 photo")
        btn4 = QPushButton("4 photos")
        for btn in [btn1, btn4]:
            btn.setStyleSheet("font-size: 20px; padding: 20px;")

        btn1.clicked.connect(lambda: self.router.go_to("preview", count=1))
        btn4.clicked.connect(lambda: self.router.go_to("preview", count=4))

        layout.addWidget(label)
        layout.addWidget(btn1)
        layout.addWidget(btn4)
        self.setLayout(layout)

    def on_enter(self, **kwargs):
        pass
