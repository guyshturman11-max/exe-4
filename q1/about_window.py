
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

GITHUB_URL = "https://github.com/YOUR_USERNAME/YOUR_REPO"   

class AboutWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("About")
        self.resize(380, 180)

        layout = QVBoxLayout()

        self.title_label = QLabel("Grades Corrector")
        self.title_label.setObjectName("aboutTitle")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.info_label = QLabel("Version 1.0\nWritten by: Guy Shturman")
        self.info_label.setAlignment(Qt.AlignCenter)

        
        self.github_label = QLabel(f'GitHub: <a href="{GITHUB_URL}">{GITHUB_URL}</a>')
        self.github_label.setOpenExternalLinks(True)
        self.github_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.title_label)
        layout.addWidget(self.info_label)
        layout.addWidget(self.github_label)
        self.setLayout(layout)
