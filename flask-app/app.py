# from flask import Flask, request, jsonify, render_template, url_for
# import openai
# from pathlib import Path

# app = Flask(__name__)
# client = openai.OpenAI(api_key="openai-api-key")

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
openai.api_key = "openai-api-key"

@app.route('/generate_speech')
def generate_speech(): # needs to trigger based on AI input
    def generate():
        with app.app_context():
            time.sleep(10)  # wait for 10 seconds
            text = "my burgers are the best in the world" # needs to change based on AI input
            speech_file_path = Path('static/speech.mp3')
            response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text
            )
            response.stream_to_file(speech_file_path)
            audio_url = url_for('static', filename='speech.mp3', _external=True)
            yield f"data: {audio_url}\n\n"

    return Response(generate(), mimetype='text/event-stream')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
