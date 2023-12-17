import streamlit as st
import speech_recognition as sr
from openai import OpenAI
import io
from pydub import AudioSegment
from pydub.playback import play
import pygame
import os
import time



# Set your OpenAI API key here
client = OpenAI(api_key="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")

# max_token here should be one since 'bug', 'feature', and 'question' are one token long. This might change for future versions of the model and api but you can check the value on the
def query_chatgpt(prompt, model='gpt-3.5-turbo', temperature=0.7):
    """
    Function to query ChatGPT-4 with a given prompt, with retries for timeouts.

    :param prompt: Prompt string to send to ChatGPT-2.5
    :param model: The model to use, default is ChatGPT-3.5
    :param max_tokens: Maximum number of tokens to generate
    :param max_retries: Maximum number of retries for timeout
    :return: Response from ChatGPT-3.5 or None if all retries fail
    """

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a Professor Assistant ChatBot."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature
    )
    return(completion.choices[0].message.content)




def get_bot_response(user_input):
    responses = {
        user_input: query_chatgpt(user_input)
    }
    return responses.get(user_input.lower())

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

    except Exception as e:
        st.error(f"An error occurred: {e}")

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError:
            return "Sorry, my speech service is down."

st.title('Simple Chatbot')

if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []

user_input = st.text_input("Type your message here:", key="user_input")

if st.button('Send'):
    st.session_state.conversation.append(f"You: {user_input}")
    bot_response = get_bot_response(user_input)
    st.session_state.conversation.append(f"Bot: {bot_response}")
    speak(bot_response)

if st.button("Speak"):
    spoken_text = recognize_speech()
    if spoken_text:
        st.session_state.conversation.append(f"You: {spoken_text}")
        bot_response = get_bot_response(spoken_text)
        st.session_state.conversation.append(f"Bot: {bot_response}")
        speak(bot_response)

conversation_text = "\n".join(st.session_state.conversation)
st.text_area("Conversation:", value=conversation_text, height=300, key="conversation_display")
