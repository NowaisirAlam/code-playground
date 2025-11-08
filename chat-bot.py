import speech_recognition as sr 
import webbrowser,os
import pyttsx3 #converts text into speech
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
from openai import OpenAI
import time
from urllib.parse import quote_plus # it actually attaches find me as https....find+me which makes the search possible

from dotenv import load_dotenv #COMMAND TO OPEN THE env
import os
load_dotenv()

SYSTEM_PROMPT = (
    "You are config ai, a concise voice assistant made by Nowaisir. "
    "Answer in 1 or 2 lines and start conversation with config"
)
chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]
MAX_TURNS = 6 

_apikey = None

old_conv = ''

# def memory(text):
#     global old_conv
#     print(old_conv)
#     old_conv+= f'You: {text} \n AI: '
#     client =_apicall()
#     response = client.chat.completions.create(
#             model="gpt-4.1-mini",   # you can also use gpt-4.1, gpt-4o, gpt-5
#             messages=[{"role": "user", "content": old_conv}],
#             max_tokens=80,
#             temperature=0.6,
#         )
#     speak(response.choices[0].message.content)
#     old_conv += response.choices[0].message.content

#     return response.choices[0].message.content



def _apicall():

    global _apikey #This helps modify _openai_client

    if _apikey is None:
        api_key=os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError('API key not found') #Note: raise is used here

        _apikey = OpenAI(api_key=api_key)
    return _apikey

def ask_chatgpt(prompt):
    try:
        client = _apicall()

        chat_history.append({"role": "user", "content": prompt})

        keep_from = max(1, len(chat_history) - 2 * MAX_TURNS)
        trimmed = [chat_history[0]] + chat_history[keep_from:]

        response = client.chat.completions.create(
            model="gpt-4.1-mini",   # you can also use gpt-4.1, gpt-4o, gpt-5
            messages=[{"role": "user", "content": prompt}],
            max_tokens=80,
            temperature=0.6,
        )
        reply = response.choices[0].message.content
        
        chat_history.append({"role": "assistant", "content": reply})
        return reply

    except Exception as e:
        return f"Sorry, I couldn't connect to ChatGPT due to {e}"

engine = pyttsx3.init() # calls init class and creates a new engine instance

def speak(text):
    engine.say(text) #adds text to the queue
    engine.runAndWait() #actually runs the queue until fininshes

def takeCommand():
    r = sr.Recognizer() 
    with sr.Microphone() as source: #takes source as a file input
        r.pause_threshold = 1 # time to listen before recognizing, default is at 0.8
        print('Listening...') #differentiating when it is actually listening
        try:
            audio = r.listen(source)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-US')
            print(query)
            return query 
        except Exception as e:
            return 'some error occured'


site = [['google', 'https://www.google.com'],
        ['netflix', 'https://www.netflix.com'],
        ['youtube','https://www.youtube.com'],
        ['facebook','https://www.facebook.com'],
        ['linkedin','https://www.linkedin.com'],
        ['weather','https://www.theweathernetwork.com/en/city/ca/ontario/london/current'],
        ['chatgpt','https://chatgpt.com/'],
        ['instagram','https://instagram.com']]

def open_duck_search(raw_text):
    q = raw_text.lower()
    for word in ["duck", "search", "for"]:
        q = q.replace(word, "").strip()

    query = q.strip() or "OpenAI"  

    # Open browser
    driver = webdriver.Chrome()
    
    driver.get(f"https://duckduckgo.com/?q={quote_plus(query)}")
    time.sleep(2)  # give results time to load

    first_result = driver.find_element(By.TAG_NAME, "h3")
    first_result.click()
    


if __name__ == '__main__':
    while True:
        text = takeCommand()
        # if not text or text == 'some error occured':
        #     continue

        time.sleep(1)
        for i in site: 
            if f'open {i[0]}' in text.lower():
                speak(f'Opening the {i[0]}')
                webbrowser.open(i[1])
        for name, url in site:
            if f'open {name}' in text.lower():
                speak(f'Opening {name}')
                webbrowser.open(url)
        if 'stop' in text.lower():
            exit()
        elif 'open music' in text.lower(): #opening spotify via browser
            webbrowser.open('https://open.spotify.com/track/2IPxsVjAkqoFXrzwGwUVia')
        elif 'movie' in text.lower(): #searching files in pc
            path = r"C:\\Users\\alamn\\Downloads\\www.Torrenting.com - Money.Heist.S01E13.XviD-AFG\\Money.Heist.S01E13.XviD-AFG.avi"

            if os.path.exists(path):
                os.startfile(path)
            else:
                speak("Movie file not found.")

        elif 'time' in text:
            curr_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f'The time is: {curr_time}')
            continue 

        elif 'internet' in text.lower():
            try:
                open_duck_search(text)
            except Exception as e:
                speak(f'Failed: {e}')
            continue

        else:
            gpt = ask_chatgpt(text.lower())
            print(f'human {text.lower()} \n gpt: {gpt}')
            speak(gpt)