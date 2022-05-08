"""
Project Name: Personal Voice Assistant using Python
Date Created: 8th May 2022
Author: Abhimanyu Sangitrao
Purpose: This project was created in order to build a python based Voice Assistant (like Siri) that can be 
         used to automate some common tasks like Sending Emails, Playing Music, Opening apps, launching Websites, etc.
         This is a prototype version of the application. More features shall be added in the future.
"""
# -------------------------------------------------- Imports ----------------------------------------------------------- #
from datetime import datetime
import datetime
import pyttsx3 # Used for Text to Speech functionality (TTS) in Python
import speech_recognition as sr #speech recognition feautres for python
import wikipedia #to surf wikipedia using python
import random
import webbrowser #For surfing the web through python
import os
import json
import smtplib #This module will be used to send Emails through python
from email.message import EmailMessage #This module contains useful functions to prepare email content and body
# --------------------------------------------------------------------------------------------------------------------- #

# loading the secrets.json file to fetch the credentials
with open('secrets.json','r') as f:
    secrets = json.load(f) #Python dict with all the credentials

# Creating a Text to Speech engine in order to take text commands from the user and convert it to audio
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices') #in-built/stored voices provided by Microsoft or Mac
# print(voices)

#Selecting a voice for the assistant from the available selection of voices.
engine.setProperty('voice',voices[1].id) # Voices can be found on your System WIndows or Mac.
engine.setProperty('rate', 160) #Set the rate at which the assistant speaks. (slow or fast)

def speak(audio):
    '''
    This function takes input the text to be converted to speech and returns the speech 
    output using the set Vooice assistant.
    '''
    engine.say(audio)
    engine.runAndWait()

def wishme():
    '''
    This function can be used to greet the user with the help of Voice Assistant 
    just to make it sound like more natural.
    '''
    hour = int(datetime.datetime.now().hour)
    if hour > 0 and hour <12:
        speak("Good Morning Sir!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir")
    else:
        speak("Good Evening Sir!")
    speak("I am Zira. How may I assist you?")

def takeCommand():
    '''
    This function takes microphone input from the user and returns string output of the speech
    '''
    r = sr.Recognizer() #sr is the Speech Recognition module installed using pip
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1 # so that the assistant waits for 1 second (instead of default 0.8) before considering the phrase to be complete
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio,language='en-in') #Uses Google to convert speech to text
            print(f"User said: {query}\n") # String that contains the speech coverted to text
        except Exception as e:
            print(f"Error is: {e}")
            speak("I did not understand that, please speak again")
            query = "None"
    return query

def sendEmail(sender_email, sender_password,receiver_email,email_subject,email_body):
    '''
    This function is used to send an email through Gmail from one account to another with a subject and a body.
    Remember, the email can be sent only when the option of "less secure apps" is enabled from Gmail app
    for the sender email ID.
    '''
    try:
        # Preparing various parts of the email like Subject, from, to and body/content
        msg = EmailMessage()
        msg.set_content(email_body)

        msg['Subject'] = email_subject
        msg['From'] = sender_email
        msg['To'] = receiver_email

        # Send the message via our own SMTP server.
        # server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        speak("Your Email has been sent successfully!")
    except Exception as e:
        print("Exception in sendEmail Function:",e)
        speak("Sorry, the email could not be sent due to some exception. Please try later!")

if __name__ == '__main__':
    wishme()
    assistant_listen = True
    
    # Start a loop to make the assistant take orders unless told to stop by the user
    while assistant_listen == True:
        query = takeCommand().lower()
        print(f"Query from main: {query}")
        
        #Now, based on the query, make your assistant perform some tasks
        # Task 1: Search wikipedia for the input query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace('wikipedia', '')
            results = wikipedia.summary(query,sentences=2) # Just fetch first two sentences from wikipedia page
            # Choose some random phrases to make it look natural speech
            phrases = ['According to Wikipedia:','I looked on wikipedia, and it says:',"As given on Wikipedia:"]
            print(results)
            speak(phrases[random.randint(0,len(phrases))])
            speak(results)
        
        #Task 2: Make your assistant open youtube
        elif 'open youtube' in query or 'youtube open' in query:
            print(f"query from task 2: {query}")
            webbrowser.open('youtube.com')
        
        #Task 3: Make your assistant open Google
        elif 'open google' in query or 'google open' in query:
            webbrowser.open('google.com')
        
        #Task 4: Make your assistant play music stored on your system by providing the path
        elif 'play music' in query or 'music play' in query:
            music_dir = 'F:\\Music'
            songs = os.listdir(music_dir)
            print(f"available songs: {songs}")
            os.startfile(os.path.join(music_dir,songs[0]))
        
        #Task 5: Make your assistant tell the time
        elif 'the time' in query or 'time kya' in query or 'kya time' in query:
            strTime = datetime.datetime.now().strftime('%H:%M:%S')
            speak(f'Sir, The time is {strTime}')
        
        #Task 6: Make your assistant send an email for you
        elif 'send email' in query or 'email bhejna' in query or 'email send' in query:
            try:
                sender_email = secrets['sender_email']
                sender_password = secrets['sender_password']
                speak('Sure, to whom should I write the email to? Do not mention @gmail.com')
                receiver_email = takeCommand()
                receiver_email = receiver_email.replace(" dot ", '.')
                receiver_email = receiver_email.replace(" ", "")
                receiver_email = receiver_email.strip() + "@gmail.com"
                speak('alright, and what would the subject be?')
                email_subject = takeCommand()
                speak("Cool, now just tell me what to write in the email body line by line. Let's start with line 1")
                email_body_1 = takeCommand()
                speak("Okay, moving on to line 2")
                email_body_2 = takeCommand()
                email_body = email_body_1 + ". \n" + email_body_2
                speak('Perfect, I am all set to send an email.')
                sendEmail(sender_email, sender_password,receiver_email,email_subject,email_body)
                # speak("Your Email has been sent successfully")
            
            except Exception as e:
                speak('There was some problem while sending an email. So email could not be sent.')
        
        #Task 7: Make your assistant stop listening and taking orders
        elif 'stop listening' in query or 'chalo bye' in query or 'thik hai' in query:
            speak("Okay Sir, I will stop listening now. Talk to you later, Byee!")
            engine.stop()
            assistant_listen = False #Just break the loop to stop the assistant from taking orders

        
