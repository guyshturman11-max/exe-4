
import sys
import os
import subprocess
import platform

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
    QFileDialog, QMessageBox, QHeaderView
)
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import Qt

from about_window import AboutWindow    


class GradesWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ''
        self.header_line = ''

        self.about_window = AboutWindow()    
        self.initUI()

   
    def initUI(self):
        self.setWindowTitle("Grades Corrector")
        self.resize(600, 700)

        main_layout = QVBoxLayout()

        top_row = QHBoxLayout()
        self.load_button = QPushButton("Load Students File")
        self.load_button.clicked.connect(self.load_file)
        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.show_about)
        top_row.addWidget(self.load_button)
        top_row.addStretch()
        top_row.addWidget(self.about_button)
        main_layout.addLayout(top_row)

        self.table = QTableWidget(50, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Original Grades", "Corrected Grades"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        main_layout.addWidget(self.table)

        bonus_row = QHBoxLayout()
        bonus_row.addWidget(QLabel("Bonus points (press Enter):"))
        self.bonus_input = QLineEdit()
        self.bonus_input.setValidator(QIntValidator(0, 100)) 
        self.bonus_input.setPlaceholderText("e.g. 5")
        self.bonus_input.returnPressed.connect(self.apply_bonus)   
        bonus_row.addWidget(self.bonus_input)
        main_layout.addLayout(bonus_row)

        self.update_button = QPushButton("Update File")
        self.update_button.setObjectName("updateButton")
        self.update_button.clicked.connect(self.update_file)
        main_layout.addWidget(self.update_button)

        self.setLayout(main_layout)

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select students file", "", "CSV Files (*.csv);;All Files (*)")
        if not file_name:          
            return

        self.selected_file = file_name

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []

        with open(self.selected_file, 'r') as f:
            self.header_line = next(f).strip()    
            for line in f:
                parts = line.strip().split(',')    
                if len(parts) < 2:                 
                    continue
                self.student_ids.append(parts[0])           
                self.original_grades.append(int(parts[1])) 
                self.corrected_grades.append(int(parts[1])) 

        self.update_table()

    
    def update_table(self):
        self.table.clearContents()
        for row in range(len(self.student_ids)):
            values = [self.student_ids[row],
                      str(self.original_grades[row]),
                      str(self.corrected_grades[row])]
            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)

    
    def apply_bonus(self):
        text = self.bonus_input.text()
        if text == '':
            return
        bonus = int(text)

        for i in range(len(self.original_grades)):
            new_grade = self.original_grades[i] + bonus
            if new_grade > 100:
                new_grade = 100
            self.corrected_grades[i] = new_grade

        self.update_table()

    
    def update_file(self):
        if self.selected_file == '':
            QMessageBox.warning(self, "No file", "Please load a file first.")
            return
        try:
            with open(self.selected_file, 'w') as f:
                f.write(self.header_line + '\n')
                for i in range(len(self.student_ids)):
                    f.write(f'{self.student_ids[i]},{self.corrected_grades[i]}\n')
        except PermissionError:
            QMessageBox.warning(self, "File is locked",
                                "The file is open in another program (Excel?).\n"
                                "Close it and try again.")
            return
        self.open_file_in_default_app(self.selected_file)

    @staticmethod
    def open_file_in_default_app(path):
        system = platform.system()
        if system == "Windows":
            os.startfile(path)                       
        elif system == "Darwin":                    
            subprocess.call(["open", path])
        else:                                        
            subprocess.call(["xdg-open", path])

   
    def show_about(self):
        self.about_window.show()     


if __name__ == "__main__":
    app = QApplication()
    qss_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.qss")
    with open(qss_path) as f:
        app.setStyleSheet(f.read())
    window = GradesWindow()
    window.show()
    app.exec()
