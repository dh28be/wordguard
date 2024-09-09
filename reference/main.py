"""import os
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, request, render_template
from subprocess import call
from flask_socketio import SocketIO, send

load_dotenv()
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/detect", methods=["post"])
def detect():
    data = request.json
    
    message = data["message"]
    type = data["type"]
    
    prompt = f"{message}\n\n이 문장에 {type}가 있는지 판별해줘"
    
    return gpt(prompt)

def gpt(prompt):
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="gpt-4",
        max_tokens=500
    )
    
    return chat_completion.choices[0].message.content


app.run(host="localhost", port=80)


"""
          
import os
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
from app import db

app = Flask(__name__)
app.secret_key = "secret"
socketio = SocketIO(app)
db.create_all()
user_no = 1

@app.before_request
def before_request():
    global user_no
    if 'session' in session and 'user-id' in session:
       pass
    else:
        session['session'] = os.urandom(24)
        session['username'] = 'user'+str(user_no)
        user_no += 1

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/mynamespace')
def connect():
    emit("response", {'data': 'Connected', 'username': session['username']})

@socketio.on('disconnect', namespace='/mynamespace')
def disconnect():
    session.clear()
    print("Disconnected")

@socketio.on("request", namespace='/mynamespace')
def request(message):
    emit("response", {'data': message['data'], 'username': session['username']}, broadcast=True)

"""if __name__ == '__main__':
    socketio.run(app)"""

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.secret_key = "super secret key"
    app.run(debug=True)