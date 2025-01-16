# Socrative Quiz Solver

## Description
This repository contains a Python-based tool designed to assist with solving quizzes on the Socrative platform. The tool leverages web automation and artificial intelligence to provide quick and accurate solutions for multiple-choice and true/false quizzes.

---

## Features

1. **Automated Quiz Interaction:**
   - Uses Selenium WebDriver to interact with the Socrative web interface automatically.
   - Supports automatic login, navigation, and question-solving.

2. **AI-Powered Answer Retrieval:**
   - Integrates with OpenAI and Google Generative AI APIs to suggest accurate answers for complex questions.

3. **Customizable Settings:**
   - Supports configuration via `config.ini` for user credentials, browser preferences, and API keys.

4. **Multimedia Support:**
   - Includes tools for image recognition (using Pillow) and text extraction from screenshots for quizzes containing images.

5. **Cross-Platform Compatibility:**
   - Designed to work on major operating systems including Windows, macOS, and Linux.

---

## Technologies Used

- **Languages:** Python
- **Libraries:**
  - Selenium (for web automation)
  - PyQt5 (for graphical user interface)
  - Pillow (for image processing)
  - Google Generative AI and OpenAI APIs (for natural language understanding)
  - SoundDevice and SpeechRecognition (for audio-based question solving)

---

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/socrative-quiz-solver.git
   cd socrative-quiz-solver
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure `config.ini`:**
   - Update the `config.ini` file with your personal API keys, Socrative student name, and room name.
   - Example `config.ini` file:
     ```ini
     [DEFAULT]
     OPENAI_API_KEY = your-openai-api-key
     GEMINI_API_KEY = your-gemini-api-key

     [USER]
     student_name = John Doe
     room_name = ROOMNAME
     ```
   - Replace `your-openai-api-key` and `your-gemini-api-key` with your actual API keys.
   - Set your **student name** and **room name** for the Socrative session.

4. **Run the tool:**
   ```bash
   python main.py
   ```

---

## Disclaimer
This tool is intended for educational and ethical purposes only. Misuse of the tool to violate Socrative's terms of service or academic integrity policies is strictly discouraged.

---

Feel free to contribute or report issues! 😊
