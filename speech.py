import speech_recognition as sr
from openai import OpenAI
import pygame
import requests
import time



# Set your OpenAI API key here
client = OpenAI(api_key="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")

def speak(text):
    try:
        # Generate speech using OpenAI's API
        response = client.audio.speech.create(
            model='tts-1',
            input=text,
            voice='alloy'
        )
        # Save the response to a file
        mp3file = f"output.mp3{time.localtime()}"
        response.stream_to_file(mp3file)

        pygame.mixer.init()
        pygame.mixer.music.load(mp3file)
        pygame.mixer.music.play()

        # Wait for the music to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)        

    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError:
            return "Sorry, my speech service is down."
