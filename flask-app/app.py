# from flask import Flask, request, jsonify, render_template, url_for
# import openai
# from pathlib import Path

# app = Flask(__name__)
# client = openai.OpenAI(api_key="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")

# @app.route('/generate_speech', methods=['POST'])
# def generate_speech():
#     text = request.json['text']
#     speech_file_path = Path('static/speech.mp3')
#     response = client.audio.speech.create(
#         model="tts-1",
#         voice="alloy",
#         input=text
#     )
#     response.stream_to_file(speech_file_path)
#     return jsonify({'audio_url': url_for('static', filename='speech.mp3', _external=True)})

# @app.route('/')
# def index():
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, Response, url_for, render_template
import openai
from pathlib import Path
import time

app = Flask(__name__)
app.config['SERVER_NAME'] = '127.0.0.1:5000'
client = openai.OpenAI(api_key="openAI-api-key HERE")

# Function to read and write the value of 'i' to a file
def read_i():
    try:
        with open('i_value.txt', 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0

def write_i(i):
    with open('i_value.txt', 'w') as file:
        file.write(str(i))

lesson = [
    "This will be today's lesson",
    "1 + 1 = 2",
    "Who wants to give us an example of linear regression?",
    "Does anyone have a question?",
    "If there are no questions, I will continue the lesson",
    "Thank you to everyone who joined the class"
]

@app.route('/generate_speech')
def generate_speech():
    i = read_i()  # Retrieve the value of 'i' from the file
    def generate():
        nonlocal i
        with app.app_context():
            if i < (len(lesson) + 1):
                speech_file_path = Path(f'static/speech_{i}.mp3')
                response = client.audio.speech.create(
                    model="tts-1",
                    voice="alloy",
                    input=lesson[i]
                )
                time.sleep(5)
                response.stream_to_file(speech_file_path)
                audio_url = url_for('static', filename=f'speech_{i}.mp3', _external=True)
                i += 1
                write_i(i)  # Update 'i' in the file
                yield f"data: {audio_url}\n\n"
            else:
                yield "data: Lesson completed\n\n"

    return Response(generate(), mimetype='text/event-stream')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
