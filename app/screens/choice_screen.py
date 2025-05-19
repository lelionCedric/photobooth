from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QTimer

class ChoiceScreen(QWidget):
    def __init__(self, router):
        super().__init__()
        self.router = router

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel("Combien de photos ?")
        label.setStyleSheet("font-size: 40px; color: white; font-weight: bold;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        btn1 = QPushButton("1 photo")
        btn4 = QPushButton("4 photos")
        
        for btn in [btn1, btn4]:
            btn.setStyleSheet("""
                font-size: 28px; 
                padding: 20px; 
                background-color: rgba(255, 255, 255, 0.8);
                border-radius: 10px;
                min-width: 200px;
                margin: 10px;
            """)

        btn1.clicked.connect(lambda: self.router.go_to("preview", count=1))
        btn4.clicked.connect(lambda: self.router.go_to("preview", count=4))

        layout.addWidget(label)
        layout.addWidget(btn1)
        layout.addWidget(btn4)
        self.setLayout(layout)
        
        # Timer pour revenir à l'écran d'accueil après 30 secondes
        self.inactivity_timer = QTimer()
        self.inactivity_timer.setSingleShot(True)
        self.inactivity_timer.timeout.connect(self.return_to_home)
        
        # Appliquer le style de fond
        self.setStyleSheet("background-image: url(assets/background.jpg); background-position: center; background-repeat: no-repeat; background-size: cover;")

    def on_enter(self, **kwargs):
        # Démarrer le timer d'inactivité
        self.inactivity_timer.start(30000)  # 30 secondes

    def return_to_home(self):
        """Retourne à l'écran d'accueil après inactivité"""
        self.router.go_to("home")
        
    def mousePressEvent(self, event):
        """Réinitialise le timer à chaque interaction avec l'écran"""
        super().mousePressEvent(event)
        self.inactivity_timer.start(30000)