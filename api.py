from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

# ... rest of your imports ...

app = Flask(__name__)
CORS(app)

# In-memory storage for messages, in real-world use you would store this in a database
messages_store = []

@app.route('/')
def index():
    # Serve the HTML page
    return render_template('index.html')

@app.route('/api/messages', methods=['GET', 'POST'])
def handle_messages():
    if request.method == 'POST':
        # Store the new message from the AJAX POST request
        message = request.json
        messages_store.append(message)
        return jsonify({'status': 'success', 'message': 'Message received'})
    else:
        # Return the stored messages for AJAX GET request
        return jsonify(messages_store)

if __name__ == '__main__':
    app.run(debug=True)
