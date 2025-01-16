import os
import io
import logging
import configparser
from PIL import Image
from time import sleep
from openai import OpenAI
from selenium import webdriver
import speech_recognition as sr
import google.generativeai as genai
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoAlertPresentException, TimeoutException

class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    END = '\033[0m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    MAGENTA = '\033[95m'

class OnlineQuizSolver:
    def __init__(self, student_name, room_name):
        self.student_name = student_name
        self.room_name = room_name
        self.load_config()
        self.client = None
        self.driver = self.setDriver()
        self.login_url = "https://b.socrative.com/login/student/"
        self.recognizer = sr.Recognizer()
        
    def load_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        gemini_key = config['DEFAULT']['GEMINI_API_KEY']
        genai.configure(api_key=gemini_key)
        self.ai = genai.GenerativeModel('gemini-1.5-flash')
        prompt = "Only say Hello I'm Gemini"
        response = self.ai.generate_content(prompt)
        if response: print(response.text)
            
    def setDriver(self):
        logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.WARNING)
        print("Setting up driver...")
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
        print("Driver set up successfully!")
        return self.driver      
    
    def enter_quiz(self):
        self.driver.get(self.login_url)
        sleep(5)
        self.driver.find_element(By.ID, 'studentRoomName').send_keys(self.room_name)
        sleep(0.2)
        self.driver.find_element(By.ID, 'studentLoginButton').click()
        sleep(5)
        self.driver.find_element(By.ID, 'student-name-input').send_keys(self.student_name)
        sleep(0.2)
        self.driver.find_element(By.ID, 'submit-name-button').click()
        print("Entered the quiz room!")
        
    def solve_quiz(self):
        try:
            question_element = self.driver.find_element(By.CLASS_NAME, 'question-text')
            question_text = question_element.text
            img = self.driver.get_screenshot_as_png()
            img = Image.open(io.BytesIO(img))
            print(f"{Color.RED}Question: {question_text}")
            response = self.ai.generate_content(["What is the answer this question? (Only one sentence that answer)", img])
            answer = response.text
            print(f"{Color.GREEN}Answer: {answer}")
            input(Color.RED + "Press Enter to continue...")
        except Exception as e: print(f"Hata: {e}")
                
    def listen_question(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening for the question...")
            audio = recognizer.listen(source)

        try:
            question = recognizer.recognize_google(audio)
            print(f"{Color.RED}Question: {question}")
            response = self.ai.generate_content(["What is the answer to this question? (Only one sentence that answers)", question])
            answer = response.text
            print(f"{Color.GREEN}Answer: {answer}")
            input(Color.RED + "Press Enter to continue...")
        except sr.UnknownValueError:
            print("Could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"Hata: {e}")
    
    
        
        
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

BANNER = Color.RED + """
 _____  ____   _   _            _     _  __ _  __  ____  
| ____||  _ \\ | \\ | |          / \\   | |/ /| |/ / / ___| 
|  _|  | |_) ||  \\| | _____   / _ \\  | ' / | ' / | |     
| |___ |  _ < | |\\  ||_____| / ___ \\ | . \\ | . \\ | |___  
|_____||_| \\_\\|_| \\_|       /_/   \\_\\|_|\\_\\|_|\\_\\ \\____| 

1- Enter Quiz
2- Solve Quiz


----> """
configs = configparser.ConfigParser().read('config.ini')
configs = configs['DEFAULT']
student_name = configs['student_name']
room_name = configs['room_name']

App = OnlineQuizSolver(student_name, room_name)
App.clear()
while True:
    try:
        choice = input(BANNER)
        if choice == "1":
            App.enter_quiz()
        elif choice == "2":
            App.solve_quiz()
        else:
            print("Invalid choice!")
            
        App.clear()
    except Exception as e:
        print(f"Hata: {e}")
        App.clear()
        