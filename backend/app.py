from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from dataclasses import dataclass
import json
from flask_socketio import SocketIO

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowrd_origin="*")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./app.db' 
app.config['SQLALCHEMY_BINDS'] = {'chat': 'sqlite:///./chat.db'} 
db = SQLAlchemy(app)

class userChatter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)


class chatInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message =  db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    author  = db.Column(db.String(80), nullable=False)
    __bind_key__ = 'chat' 



@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login/", methods=["GET", "POST"])
def login_controller():
    if request.method == "POST":
        user_username = request.form['username']
        if(user_username.strip()):
            if userChatter.query.filter_by(username=user_username).first() is not None:
                user = userChatter.query.filter_by(username=user_username).first()
                return redirect(url_for("profile", username=user_username))
            else:
                try:
                    new_user = userChatter(username=user_username)
                    db.session.add(new_user)
                    db.session.commit()
                    
                    return redirect(url_for("profile", username=user_username))
                except Exception as e:
                    print(e)
                    return render_template("index.html")
        else:
             return render_template("index.html")
    else:
        return render_template("index.html")

@app.route("/profile/<username>")
def profile(username=None):
    chats = chatInfo.query.order_by(chatInfo.date_created.desc()).all()
    user = userChatter.query.filter_by(username=username).first()
    return render_template('chat.html', user=user, chats=chats)

@socketio.on('message')
def handle_username(data):
    data["user"] = data["user"].encode("utf-8").decode("utf-8")
    data["message"] = data["message"].encode("utf-8").decode("utf-8")
    data["message"] = detect(data["message"])
    new_chat = chatInfo(author=data["user"],message=data["message"])
    print('received massage : ',data)
    socketio.emit("response", {"username":data["user"], "message": data["message"]})
    try:
        db.session.add(new_chat) 
        db.session.commit()
        addChat = {'author': data["user"], 'message': data["message"]}
        return json.dumps(addChat)
        # return redirect(url_for('profile', username=author))
    except Exception as e:
        print(e)
        return 'There was an error adding your chat message'
    
def detect(message):
    
    message = message.replace('\n', '').strip()
    # type = data["type"]
    
    prompt = f"{message}"
    print("Received Prompt:", prompt)
    
    mode = int(determine_existence(prompt))

    print(mode)
    if mode == 0:
        result = illegal_mask(offensive_mask(prompt))
    elif mode == 1:
        result = offensive_mask(prompt)
    elif mode == 2:
        result = illegal_mask(prompt)
    else:
        result = prompt

    return result

def determine_existence(prompt):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert assistant that detect offensive words or harmful, illegal, and scam websites in the sentence. "
                    "If there exists offensive words and illegal websites, output 0."
                    "If there exists only offensive words, output 1."
                    "If there exists only illegal websites, output 2."
                    "If there does not exist any of them, output 3."
                    "Detecting offensive words, the most important thing is to consider the context. If it has the same letter but has different meaning, the result has to be different."
                    "So, consider the context and answer whether it has offensive word or not."
                    "Detecting illegal websites, consider sites that may involve phishing, online scams, fake marketplaces, illegal downloads, or adult content."
                    "Try using scam advisor when you need it to consider whether it is scam site or not."
                    "Your output must be one of 0~3."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="gpt-4",
        #model="ft:gpt-4o-mini-2024-07-18:personal:chat-filtering:A5vtEEgW",
        max_tokens=500
    )
    
    return chat_completion.choices[0].message.content

def offensive_mask(prompt):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert assistant that mask offensive words to *** in the sentence."
                    "There are offensive words in the given sentence. Find it and replace it with ***."
                    "If you cannot find any offensive word, just output the original sentence."
                    "Do not add anything in the output."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="gpt-4",
        #model="ft:gpt-4o-mini-2024-07-18:personal:chat-filtering:A5vtEEgW",
        max_tokens=500
    )
    
    return chat_completion.choices[0].message.content

def illegal_mask(prompt):
    print(prompt)
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert assistant that helps to filter harmful, illegal, and scam websites in the sentence. "
                    "Your task is to mask harmful, illegal, and scam websites with '******'. There must be at least one harmful website."
                    "I'll provide you the example of harmful sites. ex) https://emarteshops.com, https://blacktoon319.com, http://zizixsoul.com/, https://aspot36.com/, https://norpo21.net/"
                    "Except the site you are planning to mask, Do not modify it. ex) https://newtoki318.com 이 주소로 접속하세요. -> ****** 이 주소로 접속하세요."
                    "You might use scam advisor to check whether it is scam site or not."
                    "Do not add any other words in the output. When masking the website, you must mask the entire URL"
                    "Response has to be consistent, for the same input."
                    "Your additional task is to tell me what kind of illegal site it is. Answer this part with Korean."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="gpt-4",
        #model="ft:gpt-4o-mini-2024-07-18:personal:chat-filtering:A5vtEEgW",
        max_tokens=500
    )
    
    return chat_completion.choices[0].message.content



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.secret_key = "super secret key"
    socketio.run(app, host="0.0.0.0", port=80, debug=True, allow_unsafe_werkzeug=True)