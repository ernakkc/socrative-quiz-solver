import os
import io
import logging
import configparser
from PIL import Image
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
import google.generativeai as genai
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit, QHBoxLayout, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QTextCharFormat, QColor, QFont, QPalette
from PyQt5.QtCore import Qt

class OnlineQuizSolver(QWidget):
    def __init__(self):
        super().__init__()
        
        self.student_name = ""
        self.room_name = ""
        self.init_ui()
        self.load_config()
        self.login_url = "https://b.socrative.com/login/student/"
        self.driver = None
        
    def init_ui(self):
        self.setWindowTitle("Online Quiz Solver")
        
        # Dark mode ve hacker tarzı görünüm için stil ayarları
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #00ff00;
                font-family: 'Courier New', Courier, monospace;
            }
            QLineEdit, QPushButton, QTextEdit {
                background-color: #2e2e2e;
                border: 1px solid #00ff00;
                color: #00ff00;
            }
            QLineEdit:focus, QPushButton:focus, QTextEdit:focus {
                border: 2px solid #00ff00;
            }
            QPushButton {
                padding: 10px;
                font-size: 14px;
            }
        """)
        
        # Banner
        self.banner = QLabel(r"""
    _____  ____   _   _            _     _  __ _  __  ____  
    | ____||  _ \ | \ | |          / \   | |/ /| |/ / / ___| 
    |  _|  | |_) ||  \| | _____   / _ \  | ' / | ' / | |     
    | |___ |  _ < | |\  ||_____| / ___ \ | . \ | . \ | |___  
    |_____||_| \_\|_| \_|       /_/   \_\|_|\_\|_|\_\ \____| 
        """)
        self.banner.setStyleSheet("color: #00ff00; font-size: 16px; font-family: 'Consolas', monospace;")
        self.banner.setAlignment(Qt.AlignCenter)
        
        # Inputs
        self.room_name_input = QLineEdit(self)
        self.room_name_input.setPlaceholderText("Enter room name")
        self.room_name_input.setFixedHeight(50)
        
        self.student_name_input = QLineEdit(self)
        self.student_name_input.setPlaceholderText("Enter student name")
        self.student_name_input.setFixedHeight(50)
        
        # Buttons
        self.set_room_button = QPushButton("Set Room Name", self)
        self.set_room_button.clicked.connect(self.set_room_name)
        
        self.set_student_button = QPushButton("Set Student Name", self)
        self.set_student_button.clicked.connect(self.set_student_name)
        
        self.enter_quiz_button = QPushButton("Enter Quiz", self)
        self.enter_quiz_button.clicked.connect(self.enter_quiz)
        
        self.solve_quiz_button = QPushButton("Solve Quiz", self)
        self.solve_quiz_button.clicked.connect(self.solve_quiz)
        
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.clicked.connect(self.close)
        
        # Output
        self.output = QTextEdit(self)
        self.output.setReadOnly(True)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.banner)
        
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.room_name_input)
        input_layout.addWidget(self.set_room_button)
        input_layout.addWidget(self.student_name_input)
        input_layout.addWidget(self.set_student_button)
        input_layout.setSpacing(10)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.enter_quiz_button)
        button_layout.addWidget(self.solve_quiz_button)
        button_layout.setSpacing(20)
        
        layout.addLayout(input_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.output)
        layout.addWidget(self.exit_button)
        
        self.setLayout(layout)
        self.setGeometry(300, 300, 800, 600)
        
    def load_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        gemini_key = config['DEFAULT']['GEMINI_API_KEY']
        genai.configure(api_key=gemini_key)
        self.ai = genai.GenerativeModel('gemini-1.5-flash')
        prompt = "Only say Hello I'm Gemini"
        response = self.ai.generate_content(prompt)
        if response:
            self.print_output(response.text, "blue")

    def set_room_name(self):
        self.room_name = self.room_name_input.text()
        self.print_output(f"Room name set as {self.room_name}", "green")
        
    def set_student_name(self):
        self.student_name = self.student_name_input.text()
        self.print_output(f"Student name set as {self.student_name}", "green")
        
    def setDriver(self):
        logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.WARNING)
        self.print_output("Setting up driver...", "blue")
        
        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option('excludeSwitches', ['disable-popup-blocking'])
        options.add_argument("--user-data-dir={}".format(os.path.abspath("user_data")))
        prefs = {
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.media_stream_mic": 1}
        options.add_experimental_option("prefs", prefs)
        
        self.driver = webdriver.Chrome(options=options)
        self.print_output("Driver set up successfully!", "green")
        return self.driver      
        
    def enter_quiz(self):
        if not self.driver:
            self.driver = self.setDriver()
        self.driver.get(self.login_url)
        sleep(5)
        self.driver.find_element(By.ID, 'studentRoomName').send_keys(self.room_name)
        sleep(0.2)
        self.driver.find_element(By.ID, 'studentLoginButton').click()
        sleep(5)
        self.driver.find_element(By.ID, 'student-name-input').send_keys(self.student_name)
        sleep(0.2)
        self.driver.find_element(By.ID, 'submit-name-button').click()
        self.print_output("Entered the quiz room!", "green")
        
    def solve_quiz(self):
        try:
            question_element = self.driver.find_element(By.CLASS_NAME, 'question-text')
            question_text = question_element.text
            # website screenshot
            img = self.driver.get_screenshot_as_png()
            img = Image.open(io.BytesIO(img))
            self.print_output(f"Question: {question_text}", "blue")
            response = self.ai.generate_content(["What is the answer this question?", img])
            answer = response.text
            self.print_output(f"Answer: {answer}", "green")
                
            sleep(10)  # 10 saniye bekleyin, gerekirse arttırabilirsiniz
        except Exception as e:
            self.print_output(f"Hata: {e}", "red")
            
    def print_output(self, text, color):
        format = QTextCharFormat()
        if color == "red":
            format.setForeground(QColor("red"))
        elif color == "green":
            format.setForeground(QColor("green"))
        elif color == "blue":
            format.setForeground(QColor("blue"))
        else:
            format.setForeground(QColor("black"))
        
        cursor = self.output.textCursor()
        cursor.mergeCharFormat(format)
        cursor.insertText(text + '\n')
        
    def closeEvent(self, event):
        if self.driver:
            self.driver.quit()
        event.accept()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = OnlineQuizSolver()
    window.show()
    sys.exit(app.exec_())
