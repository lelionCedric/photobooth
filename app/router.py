from PyQt6.QtWidgets import QStackedWidget
from app.screens.home_screen import HomeScreen
from app.screens.choice_screen import ChoiceScreen
from app.screens.preview_screen import PreviewScreen
from app.screens.display_screen import DisplayScreen

class Router(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 600)

        self.home = HomeScreen(self)
        self.choice = ChoiceScreen(self)
        self.preview = PreviewScreen(self)
        self.display = DisplayScreen(self)

        self.addWidget(self.home)
        self.addWidget(self.choice)
        self.addWidget(self.preview)
        self.addWidget(self.display)

        self.setCurrentWidget(self.home)

    def go_to(self, screen_name, **kwargs):
        screen = getattr(self, screen_name)
        screen.on_enter(**kwargs)
        self.setCurrentWidget(screen)