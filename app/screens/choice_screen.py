from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QTimer

class ChoiceScreen(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        # Configuration de fond transparent pour permettre au fond du parent de s'afficher
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: transparent;")

        # Timer pour revenir à l'écran d'accueil après 30 secondes
        self.inactivity_timer = QTimer()
        self.inactivity_timer.setSingleShot(True)
        self.inactivity_timer.timeout.connect(self.return_to_home)

        # Layout principal horizontal pour diviser l'écran en deux parties
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)  # Espace entre les deux moitiés

        #LEFT
        left_widget = QWidget()
        left_widget.setStyleSheet(f"""
            background-color: transparent;
            height: {self.router.screen_height};
            width: {self.router.screen_width/2};
        """)
        left_layout = QVBoxLayout(left_widget)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        btn_left = QPushButton("1 photo")
        btn_left.setStyleSheet("background-color: rgba(0, 0, 0, 0); font-size: 15px")
        btn_left.setFont(router.fontUtils.custom_font)
        btn_left.clicked.connect(lambda: self.router.go_to("preview", count=1))
        
        left_layout.addWidget(btn_left, 0, Qt.AlignmentFlag.AlignCenter)

        #RIGHT

        right_widget = QWidget()
        right_widget.setStyleSheet(f"""
            background-color: transparent;
            height: {self.router.screen_height};
            width: {self.router.screen_width/2};
        """)
        right_layout = QVBoxLayout(right_widget)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        btn_right = QPushButton("4 photos")
        btn_right.setFont(router.fontUtils.custom_font)
        btn_right.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        btn_right.clicked.connect(lambda: self.router.go_to("preview", count=4))
        
        right_layout.addWidget(btn_right, 0, Qt.AlignmentFlag.AlignCenter)
        
        # Ajouter les deux moitiés au layout principal
        main_layout.addWidget(left_widget, 1)  # Partie gauche
        main_layout.addWidget(right_widget, 1)  # Partie droite        
        
        self.setLayout(main_layout)

    def on_enter(self, **kwargs):
        # Démarrer le timer d'inactivité
        self.inactivity_timer.start(30000)  # 30 secondes

    def return_to_home(self):
        """Retourne à l'écran d'accueil après inactivité"""
        self.router.go_to("home")
        
    def mousePressEvent(self, event):
        """Réinitialise le timer à chaque interaction avec l'écran"""
        super().mousePressEvent(event)
        self.inactivity_timer.start(300)