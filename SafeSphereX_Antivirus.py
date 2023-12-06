import os
import sys
import threading
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QSizePolicy, QProgressBar
from PyQt6.QtCore import Qt, pyqtSignal, QObject

class FileSearcher(QObject):
    update_progress = pyqtSignal(int)
    completed = pyqtSignal()

    def __init__(self, directory):
        super().__init__()
        self.directory = directory

    def run(self):
        total_dirs = sum([len(dirs) for _, dirs, _ in os.walk(self.directory)])
        processed_dirs = 0

        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file.endswith('.scpt'):
                    print(os.path.join(root, file))
            processed_dirs += 1
            progress = int((processed_dirs / total_dirs) * 100)
            self.update_progress.emit(progress)

        self.completed.emit()

class VirusCheckWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Virus Check")
        self.setGeometry(200, 200, 300, 200)
        layout = QVBoxLayout(self)

        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximum(100)
        layout.addWidget(self.progressBar)

        self.file_searcher = FileSearcher(os.path.expanduser('~'))
        self.file_searcher.update_progress.connect(self.update_progress_bar)
        self.file_searcher.completed.connect(self.search_completed)

        self.start_search()

    def start_search(self):
        threading.Thread(target=self.file_searcher.run).start()

    def update_progress_bar(self, value):
        self.progressBar.setValue(value)

    def search_completed(self):
        # Here you can add code to handle what happens when the search is completed
        pass
    
    
    

class SafeSphereX(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("SafeSphere X")
        #self.setGeometry(100, 100, 400, 300)  # x, y, width, height
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-image: url('/Users/qingchen.deng/GitHub/SafeSphereX/assets/img/menubg.png');")  # Update with your image path

        # Central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Title Label
        title = QLabel("SafeSphere X", self)
        title.setStyleSheet("font-family: Arial; font-size: 40px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Menu buttons
        self.add_button(layout, "Check For Virus", self.open_virus_check_window)
        self.add_button(layout, "Whitelist", self.open_whitelist_window)
        self.add_button(layout, "About", self.open_about_window)
        self.add_button(layout, "Settings", self.open_settings_window)

#    def add_button(self, layout, text, callback):
#        button = QPushButton(text, self)
#        button.clicked.connect(callback)
#        button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
#        layout.addWidget(button)
    def add_button(self, layout, text, callback):
        button = QPushButton(text, self)
        button.clicked.connect(callback)

        # Set the font size to 20px
        font = button.font()
        font.setPointSize(20)
        font.setBold(True)
        button.setFont(font)
        button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        layout.addWidget(button)

    def open_virus_check_window(self):

        self.virus_check_window = VirusCheckWindow()
        self.virus_check_window.show()

        

    def open_whitelist_window(self):
        self.whitelist_window = CustomWindow("Whitelist")
        self.whitelist_window.show()

    def open_about_window(self):
        self.about_window = CustomWindow("About")
        self.about_window.show()

    def open_settings_window(self):
        self.settings_window = CustomWindow("Settings")
        self.settings_window.show()

class CustomWindow(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(200, 200, 300, 200)  # x, y, width, height

        layout = QVBoxLayout(self)
        label = QLabel(f"This is the {title} page.", self)
        layout.addWidget(label)
        # Additional widgets for each page can be added here

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SafeSphereX()
    window.show()
    sys.exit(app.exec())
