from flask import Flask, render_template, request
import requests
from gtts import gTTS
import tempfile
import os


app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    message = request.form['message']
    response = get_chatbot_response(message)
    return response
def get_chatbot_response(message):
    # Call the ChatGPT API and retrieve the response
    # Replace 'YOUR_API_KEY' with your actual ChatGPT API key
    api_key = 'YOUR_API_KEY'
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'messages': [{'role': 'system', 'content': 'You are a user.'},
                     {'role': 'user', 'content': message}]
    }
    response = requests.post(url, json=data, headers=headers)
    json_response = response.json()
    bot_reply = json_response['choices'][0]['message']['content']
    return bot_reply
def get_chatbot_response(message):
    # ... existing code ...
    bot_reply = json_response['choices'][0]['message']['content']
    tts = gTTS(bot_reply, lang='en')
    # Save the audio file temporarily
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    tts.save(temp_file.name + '.mp3')
    audio_file_path = temp_file.name + '.mp3'
    # Convert the audio file to base64 for embedding in HTML
    with open(audio_file_path, 'rb') as audio_file:
        audio_data = audio_file.read()
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
    # Remove the temporary audio file
    os.remove(audio_file_path)
    return bot_reply, audio_base64
    @app.route('/chat', methods=['POST'])
    def chat():
        message = request.form['message']
        bot_reply, audio_base64 = get_chatbot_response(message)
        return {'text': bot_reply, 'audio': audio_base64}

