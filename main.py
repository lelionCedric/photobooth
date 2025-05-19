from PyQt6.QtWidgets import QApplication
from app.router import Router
import sys

app = QApplication(sys.argv)
router = Router()
router.show()
sys.exit(app.exec())