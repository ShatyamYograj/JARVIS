import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import datetime
import sys
import pyjokes


    #   Recognizer object:- helps in reconize the speech
recogniser = sr.Recognizer()       
engine = pyttsx3.init()             # object creation
newsapi ="743d017430e84cc1886c7b3d58947f11"


    # CHANGE VOICE BETWEEN MALE AND FEMALE

voices = engine.getProperty('voices')       #getting details of current voice
# engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female



def speak(text):
    engine.say(text)
    engine.runAndWait()

# wish function
def wish():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good morning sir")
    
    elif hour>=12 and hour<17:
        speak("Good afternoon sir")
    
    else:
        speak("Good Evening sir")
  
    speak("i am jarvis. please tell me how can i help you ")


def processCommand(c):

    if "open google" in c.lower():
        speak("Sir, what should I search on Google?")
        try:
            with sr.Microphone() as source:
                recognizer = sr.Recognizer()
                recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                search_query = recognizer.recognize_google(audio)
                speak(f"Searching for {search_query} on Google.")
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
        except Exception as e:
            speak("Sorry, I could not understand your search request.")
            print(f"Error: {e}")
    

    elif"open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    
    elif"open instagram " in c.lower():
        webbrowser.open("https://instagram.com")
    
    elif"open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")

    elif "open youtube" in c.lower():
        speak("Sir, what should I search on YouTube?")
        try:
            with sr.Microphone() as source:
                recognizer = sr.Recognizer()
                recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                search_query = recognizer.recognize_google(audio)
                speak(f"Searching for {search_query} on YouTube.")
                webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        except Exception as e:
            speak("Sorry, I could not understand your search request.")
            print(f"Error: {e}")
        
    elif"open twitter" in c.lower():
        webbrowser.open("https://x.com")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link) 

    elif "news" in c.lower():
        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey=743d017430e84cc1886c7b3d58947f11")
        if r.status_code ==200:
            # parse the JSON response
            data =r.json()

        # extract the article
        articles = data.get('articles', [])

        # print the headlines
        for article in articles:
            speak(article['title'])  

    elif "tell me a joke" in c.lower():
        joke= pyjokes.get_joke()
        speak(joke) 

    else:
        speak("I'm sorry, I didn't understand that command.")

    # Ask if the user needs anything else before system "EXIT".
    speak("All systems operational, sir. Anything else?")
    try:
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            response = recognizer.recognize_google(audio).lower()
            if "no thanks" in response or "no" in response:
                speak("Thanks for using me, sir. Have a great day!")
                sys.exit()  # Exit the program gracefully
    except Exception as e:
        speak("Sorry, I didn't catch that. Let me know if you need anything else.")

    

if __name__=="__main__":
    speak("Initializing Jarvis....")
    wish()
    while True:
        # Listen For the wake word "JARVIS"
        # obtain audio from the microphone
        r = sr.Recognizer()

        # recognize speech using google
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)

            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("yes sir?")
                # listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active....")
                    audio = r.listen(source)
                    command= r.recognize_google(audio)

                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))

