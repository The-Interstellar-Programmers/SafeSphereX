import os
import sys
import threading
from time import gmtime, strftime, time
from PyQt6.QtCore import Qt, pyqtSignal, QObject, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QSizePolicy, QProgressBar, QMessageBox, QTextEdit




#OLD PERCENT PROGRESSBAR CODE

#class FileSearcher(QObject):
#    update_progress = pyqtSignal(int) # Create the signals
#    completed = pyqtSignal() # Create the signals
#    
#    def __init__(self, directory):
#        super().__init__() # Call the parent constructor
#        self.directory = directory # Set the directory to search

    #def run(self):
    #    total_dirs = sum([len(dirs) for _, dirs, _ in os.walk(self.directory)]) # Total Directories
    #    processed_dirs = 0 # Inital Number of processed directories
    

    #    for root, dirs, files in os.walk(self.directory): # Walk through all the directories
    #        for file in files: # For each file in the directory
    #            if file.endswith('.scpt' and '.py'): # Change this to the file extension you want to search for, in this case: .scpt .py .app
    #                print(os.path.join(root, file)) # Print the path of the file
    #                filepath_logdate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    #                f = open("filepaths.txt", "a")
    #                f.write("\n" + filepath_logdate + " " + os.path.join(root, file) + "\n") # Write the path of the file to a text file
    #                f.close()
    #                
    #        processed_dirs += 1 # Increment the number of processed directories
    #        progress = int((processed_dirs / total_dirs) * 100) # Calculate the progress
    #        self.update_progress.emit(progress) # Emit the progress signal

    #   self.completed.emit() # Emit the completed signal
    
    
    
    
    
    
#class FileCheckWindow(QWidget):
#    def __init__(self):
#        super().__init__()
#        self.setGeometry(200, 200, 300, 200)
#        layout = QVBoxLayout(self)
#
#        self.progressBar = QProgressBar(self)
#        self.progressBar.setMaximum(100)
#        layout.addWidget(self.progressBar)
#
#
#        self.file_searcher = FileSearcher(os.path.expanduser('~/')) # Change this to the directory you want to search
#        self.file_searcher.update_progress.connect(self.update_progress_bar) # Connect the signals to the slots
#        self.file_searcher.completed.connect(self.search_completed) # Connect the signals to the slots
#
#        self.start_search()
#
#    def start_search(self):
#        threading.Thread(target=self.file_searcher.run).start() # Start the search in a new thread
#
#    def update_progress_bar(self, value):
#        self.progressBar.setValue(value) # Update the progress bar
#
#    def search_completed(self):
#        # Here you can add code to handle what happens when the search is completed
#        pass

# END OF OLD PERCENT PROGRESSBAR CODE
 
 
class FileSearcher(QObject):
    completed = pyqtSignal()
    error = pyqtSignal(str)
    found_file = pyqtSignal(str)  # New signal for when a file is found

    def __init__(self, directory):
        super().__init__()
        self.directory = directory

#    def run(self):
#        for root, dirs, files in os.walk(self.directory):
#            for file in files:
#                if file.endswith('.scpt') or file.endswith('.py'):
##                    try:
#                        with open(os.path.join(root, file), 'r') as f:
#                            pass
#                    except Exception as e:
#                        self.error.emit(f"Access denied: {os.path.join(root, file)}")
#                        continue

        self.completed.emit()
        
    def run(self):
        total_dirs = sum([len(dirs) for _, dirs, _ in os.walk(self.directory)]) # Total Directories
        processed_dirs = 0 # Inital Number of processed directories
    

        for root, dirs, files in os.walk(self.directory): # Walk through all the directories
            for file in files: # For each file in the directory
                if file.endswith('.scpt' and '.py'): # Change this to the file extension you want to search for, in this case: .scpt .py .app
                    print(os.path.join(root, file)) # Print the path of the file
                    file_paths = os.path.join(root, file)
                    self.found_file.emit(file_paths)  
                    filepath_logdate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    f = open("filepaths.txt", "a")
                    f.write("\n" + filepath_logdate + " " + os.path.join(root, file) + "\n") # Write the path of the file to a text file
                    f.close()
                    

        self.completed.emit() # Emit the completed signal

class FileCheckWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Check")
        self.setFixedSize(550, 400)
        layout = QVBoxLayout(self)

        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 0)  # Indeterminate mode
        layout.addWidget(self.progressBar)

        self.timerLabel = QLabel("Scanning Files...\nElapsed Time: 00:00:00", self)
        layout.addWidget(self.timerLabel)
        self.startTime = time()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        
        self.file_list = QTextEdit(self)
        self.file_list.setReadOnly(True)  # Make the text edit read-only
        layout.addWidget(self.file_list)


        self.file_searcher = FileSearcher(os.path.expanduser('~'))
        self.file_searcher.found_file.connect(self.add_file_path)
        self.file_searcher.completed.connect(self.search_completed)
        self.file_searcher.error.connect(self.show_error_message)

        self.start_search()
        
        
    def add_file_path(self, file_path):
        self.file_list.append(file_path)  # Add the file path to the text box

    def start_search(self):
        self.startTime = time()
        self.timer.start(1000)  # Update timer every second
        threading.Thread(target=self.file_searcher.run, daemon=True).start()

    def update_timer(self):
        elapsedTime = int(time() - self.startTime)
        self.timerLabel.setText("Scanning Files...\nElapsed Time: {:02d}:{:02d}:{:02d}".format(
            elapsedTime // 3600, (elapsedTime % 3600 // 60), elapsedTime % 60))

    def search_completed(self):
        self.timer.stop()
        self.progressBar.setRange(0, 1)
        self.progressBar.setValue(1)
        QMessageBox.information(self, "Search Results", "File Scan Completed!\nNow Scanning Viruses...")
        FileCheckWindow.hide()
        class VirusCheckWindow(QWidget):
            def __init__(self):
                super().__init__()
                self.setWindowTitle("Virus Check")
                self.setFixedSize(550, 400)
                layout = QVBoxLayout(self)

                self.progressBar = QProgressBar(self)
                self.progressBar.setRange(0, 0)
        
        pass
        

    def show_error_message(self, file_path):
        QMessageBox.critical(self, "Error", file_path)

        
        
    
    
    

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

        self.virus_check_window = FileCheckWindow()
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
