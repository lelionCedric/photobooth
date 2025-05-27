from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtCore import Qt, QTimer

class FontUtils():
    def __init__(self):
        super().__init__()

        font_id = QFontDatabase.addApplicationFont("assets/fonts/Amatic-Bold.ttf")
        # Récupérer le nom de la famille de police
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        font_family = font_families[0]
        self.custom_font = QFont(font_family)
        