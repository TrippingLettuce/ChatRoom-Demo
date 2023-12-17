import time
import requests
from Backend.core import get_bot_response
import urllib.parse
from speech import speak

# ------------------------------------------------------------ #
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Define memory chat
openai_api_key = "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"
llm = ChatOpenAI(temperature=0.2, openai_api_key=openai_api_key)
memory = ConversationBufferMemory()

conversation = ConversationChain(
    llm=llm, 
    memory = memory,
    # verbose=True
)
# ------------------------------------------------------------ #

def send_message(message):
    # Your chat room details
    room_id = 'Qs1uFHWMQ'
    auth_token = '336c50666a3142486970723857467347724c4f776b6b6e42685752445851757963796951544a4d3573694c51746b6847'
    
    # URL encode the auth token
    encoded_auth_token = urllib.parse.quote_plus(auth_token)

    # Prepare the response
    send_message_url = f"https://api.deadsimplechat.com/consumer/api/v1/chatroom/{room_id}/message"
    data = {
        "user": {
            "username": "AI Professor"
        },
        # "message": get_bot_response(message) # For general chat
        "message": conversation.predict(input=message) # for conversational
    }
    speak(data["message"])

    params = {'auth': encoded_auth_token}

    # Send the response
    try:
        response = requests.post(send_message_url, json=data, params=params)
        response.raise_for_status()
        print("Message sent successfully.")
    except requests.RequestException as e:
        print(f"An error occurred while sending the message: {e}")
        print(f"Response details: {response.text}")

def main():
    last_processed_message = None

    while True:
        try:
            response = requests.get('http://127.0.0.1:5000/api/messages')
            response.raise_for_status()
            messages = response.json()

            if messages:
                latest_message = messages[-1]

                # Check if 'user' key exists and the message is not from 'AI Professor'
                if 'user' in latest_message and latest_message['user']['username'] != 'AI Professor':
                    current_message = latest_message['message']
                    
                    # Process the message if it's different from the last one
                    if current_message != last_processed_message:
                        send_message(current_message)
                        last_processed_message = current_message
                else:
                    print("Message is not from a user or from AI Professor.")
            else:
                print("No messages in the chat room.")

        except requests.RequestException as e:
            print(f"An error occurred: {e}")

        time.sleep(5)  # Sleep before making the next request

if __name__ == '__main__':
    main()