Config Assistant — Python Voice Assistant

Config Assistant is a simple AI-powered voice assistant built with Python.
It supports text + voice input, ChatGPT replies, website automation, and a Tkinter chat interface.

🚀 Features

ChatGPT Integration (GPT-4.1-mini with trimmed chat history)

Voice Commands using speech_recognition

Text-to-Speech with pyttsx3

Open Websites (Google, YouTube, Netflix, Instagram, etc.)

DuckDuckGo Search with Selenium

Show Time, Play Music, Open Local Movie

Clean Tkinter GUI (Send button + Mic button)

Multithreading for smooth UI

🛠️ Tech Stack

Python

Tkinter

OpenAI API

SpeechRecognition

pyttsx3

Selenium

dotenv

📦 Installation
git clone https://github.com/your-user/your-repo
cd your-repo
pip install -r requirements.txt


Create a .env file:

OPENAI_API_KEY=your_api_key_here


Install ChromeDriver for Selenium (must match your Chrome version).

▶️ Run
python main.py


GUI will open.
You can type, click Send, or press 🎙️ Mic to speak.

🧩 Commands

“Open Google/YouTube/Netflix…”

“Search for …” → DuckDuckGo

“What time is it?”

“Open music”

“Play movie”

Anything else → Answered by ChatGPT

📁 File Example (requirements.txt)
pyttsx3
speechrecognition
selenium
python-dotenv
openai
tk
pyaudio
