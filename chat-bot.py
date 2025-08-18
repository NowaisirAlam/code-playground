import speech_recognition as sr 
import webbrowser,os
import pyttsx3 #converts text into speech
import webdriver
import datetime,openai
from openai import OpenAI
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def ask_chatgpt(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",   # you can also use gpt-4.1, gpt-4o, gpt-5
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Sorry, I couldn't connect to ChatGPT."

engine = pyttsx3.init() # calls init class and creates a new engine instance

def speak(text):
    engine.say(text) #adds text to the queue
    engine.runAndWait() #actually runs the queue until fininshes
def takeCommand():
    r = sr.Recognizer() 
    with sr.Microphone() as source: #takes source as a file input
        r.pause_threshold = 1 # if 1s of silence then stop listening
        print('Listening...') #differentiating when it is actually listening
        try:
            audio = r.listen(source)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-US')
            print(query)
            return query 
        except Exception as e:
            return 'some error occured'


site = [['google', 'https://www.google.com'],['netflix', 'https://www.netflix.com'],['youtube','https://www.youtube.com'],['facebook','https://www.facebook.com'],['linkedin','https://www.linkedin.com']]
if __name__ == '__main__':
    while True:
        text = takeCommand()
        speak(text)
        # time.sleep(1)
        if 'stop' in text.lower():
            break
        # for i in site: 
        #     if f'open {i[0]}' in text.lower():
        #         speak(f'Opening the {i[0]}')
        #         webbrowser.open(i[1])
        for name, url in site:
            if f'open {name}' in text.lower():
                speak(f'Opening {name}')
                webbrowser.open(url)
        if 'open music' in text.lower(): #opening spotify via browser
            webbrowser.open('https://open.spotify.com/track/2IPxsVjAkqoFXrzwGwUVia')
        if os.path.exists(path):
            os.startfile(path)
        else:
            speak("Movie file not found.")
        if 'movie' in text.lower(): #searching files in pc
            path = "C:\\Users\\alamn\\Downloads\\(PlayHD.ooo) Money Heist Season 1 Complete English HD 720p\\(PlayHD.ooo) Money Heist S01E08 English HD 720p x264 AAC.mp4"
            os.startfile(path)

        if 'time' in text:
            curr_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f'The time is: {curr_time}')
        if 'chatgpt' in text.lower():
            response=ask_chatgpt(text)
            speak(response)


#Add more functions
