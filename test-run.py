import os, time, datetime, threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter.scrolledtext import ScrolledText

import speech_recognition as sr
import webbrowser
import pyttsx3
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import quote_plus

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

SYSTEM_PROMPT = (
    "You are ai, a concise voice assistant made by Nowaisir. "
    "Answer in 1 or 2 lines"
)
chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]
MAX_TURNS = 6

_apikey_client = None

def _apicall():
    global _apikey_client
    if _apikey_client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("API key not found")
        _apikey_client = OpenAI(api_key=api_key)
    return _apikey_client

def ask_chatgpt(prompt: str) -> str:
    
    try:
        client = _apicall()
        chat_history.append({"role": "user", "content": prompt})

        keep_from = max(1, len(chat_history) - 2 * MAX_TURNS)
        trimmed = [chat_history[0]] + chat_history[keep_from:]

        resp = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=trimmed,
            max_tokens=80,
            temperature=0.6,
        )
        reply = resp.choices[0].message.content
        chat_history.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        return f"Sorry, I couldn't connect to ChatGPT due to {e}"

engine = pyttsx3.init()

def speak(text: str):
    engine.say(text)
    engine.runAndWait()

def takeCommand() -> str:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        try:
            append_chat("system", "🎙️Listening…")
            audio = r.listen(source)
            append_chat("system", "🧠Recognizing…")
            return r.recognize_google(audio, language="en-US")
        except Exception:
            return "some error occured"

SITE = [
    ("google", "https://www.google.com"),
    ("netflix", "https://www.netflix.com"),
    ("youtube", "https://www.youtube.com"),
    ("facebook", "https://www.facebook.com"),
    ("linkedin", "https://www.linkedin.com"),
    ("weather", "https://www.theweathernetwork.com/en/city/ca/ontario/london/current"),
    ("chatgpt", "https://chatgpt.com/"),
    ("instagram", "https://instagram.com"),
]

def open_duck_search(raw_text: str):
    q = raw_text.lower()
    for word in ["duck", "search", "for"]:
        q = q.replace(word, "").strip()
    query = q.strip() or "OpenAI"

    driver = webdriver.Chrome()
    driver.get(f"https://duckduckgo.com/?q={quote_plus(query)}")
    # small wait; for production use explicit waits
    time.sleep(2)
    first_result = driver.find_element(By.TAG_NAME, "h3")
    first_result.click()

def process_text(text):
    """
    Takes raw text, handles simple commands (open sites, time, music, internet),
    otherwise sends to ChatGPT. Returns reply for UI + TTS.
    """
    if not text:
        return "Didn't catch that"

    low = text.lower()

    # open known sites
    for name, url in SITE:
        if f"open {name}" in low:
            speak(f"Opening {name}")
            webbrowser.open(url)
            return f"Opened {name}"

    if "stop" in low:
        root.after(50, root.destroy)
        return "Stopping."

    if "open music" in low:
        webbrowser.open("https://open.spotify.com/track/2IPxsVjAkqoFXrzwGwUVia")
        return "Opening music."

    if "movie" in low:
        path = r"C:\\Users\\alamn\\Downloads\\www.Torrenting.com - Money.Heist.S01E13.XviD-AFG\\Money.Heist.S01E13.XviD-AFG.avi"
        if os.path.exists(path):
            os.startfile(path)
            return "Playing movie."
        return "Movie file not found."

    if "time" in low:
        curr_time = datetime.datetime.now().strftime("%H:%M:%S")
        say = f"The time is: {curr_time}"
        speak(say)
        return say

    if "internet" in low or "duck" in low or "search" in low:
        try:
            open_duck_search(text)
            return "Searching the web."
        except Exception as e:
            return f"Failed: {e}"

    # default: ask ChatGPT
    return ask_chatgpt(low)

def append_chat(role, text):
    chat_box.configure(state="normal")
    if role == "user":
        chat_box.insert(tk.END, f"You: {text}\n")
    elif role == "assistant":
        chat_box.insert(tk.END, f"Config: {text}\n")
    else:
        chat_box.insert(tk.END, f"{text}\n")
    chat_box.see(tk.END) #always scroll to the very bottom
    chat_box.configure(state="disabled") # locking the ability to edit in text

def on_send():
    text = entry.get().strip() #takes text from the entry widget and strips to string
    if not text:
        return
    entry.delete(0, tk.END) #empty the entry widget fully
    append_chat("user", text) #appends to chat
    threading.Thread(target=_handle_query, args=(text,), daemon=True).start()
    # root.after(0, lambda: _handle_query(text))


def on_mic():
    threading.Thread(target=_mic_flow, daemon=True).start()

def _mic_flow():
    spoken = takeCommand()
    if spoken == "some error occured":
        append_chat("system", "Mic error. Try again.")
        return
    append_chat("user", spoken)
    _handle_query(spoken)

def _handle_query(text: str):
    reply = process_text(text)
    append_chat("assistant", reply)
    try:
        speak(reply)
    except Exception:
        pass

# Build window
root = tk.Tk()
root.title("Config Assistant")
root.geometry("720x520")

# Chat history
chat_box = scrolledtext.ScrolledText(root, 
            wrap=tk.WORD, 
            state="disabled", 
            font=("Segoe UI", 10))
chat_box.pack(fill=tk.BOTH, 
              expand=True, 
              padx=12, 
              pady=(12, 6))

# Bottom bar
bottom = tk.Frame(root)
bottom.pack(fill=tk.X, padx=12, pady=(0, 12))

entry = tk.Entry(bottom, font=("Segoe UI", 10))
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
entry.bind("<Return>", lambda e: on_send())

send_btn = tk.Button(bottom, text="Send ↩", width=10, command=on_send)
send_btn.pack(side=tk.LEFT, padx=(0, 8))

mic_btn = tk.Button(bottom, text="🎙️ Mic", width=8, command=on_mic)
mic_btn.pack(side=tk.LEFT)

append_chat("system", "👋 Config Assistant is ready. Type or click 🎙️ to speak.")
root.mainloop()