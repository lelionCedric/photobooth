from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class HomeScreen(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        # Configuration de fond transparent pour permettre au fond du parent de s'afficher
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: transparent;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Supprimer les marges du layout pour éviter les bords blancs
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)  # Espace entre les widgets
       
        button = QPushButton("Faire une photo")
        button.setStyleSheet(f"""
            font-size: 30px;
            background-color: rgba(0,0,0,0);
            color: white;
            border: none;
            height: {self.router.screen_height}px;
            width: {self.router.screen_width}px;
        """)
        button.clicked.connect(lambda: self.router.go_to("choice"))
        
        layout.addWidget(button)
        self.setLayout(layout)

    def on_enter(self, **kwargs):
        pass