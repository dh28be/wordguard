from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from dataclasses import dataclass
import json

import os
from openai import OpenAI
from dotenv import load_dotenv

app = Flask(__name__)
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
    author  = db.Column(db.String(100), nullable=False)
    __bind_key__ = 'chat' 

@app.route("/", methods=["GET", "POST"])
def default():
    print("redirecting to login_controller for the first time")
    return redirect(url_for("login_controller"))

@app.route("/login/", methods=["GET", "POST"])
def login_controller():
    if request.method == "POST":
        user_username = request.form['username']
        if userChatter.query.filter_by(username=user_username).first() is not None:
            print(userChatter.query.filter_by(username=user_username).first())
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
                return render_template("loginPage.html")
    else:
        return render_template("loginPage.html")

@app.route("/profile/<username>")
def profile(username=None):
    chats = chatInfo.query.order_by(chatInfo.date_created.desc()).all()
    user = userChatter.query.filter_by(username=username).first()
    return render_template('chat_page.html', user=user, chats=chats)

@app.route("/logout/")
def unlogger():
	# if logged in, log out, otherwise offer to log in
	if "username" in session:
		# note, here were calling the .clear() method for the python dictionary builtin
		session.clear()
		return render_template("logoutPage.html")
	else:
		return redirect(url_for("login_controller"))

@app.route("/new_message/", methods=["POST"])
def new_message(): 
	message = request.form.get('message')
	author = request.form.get('author')
	new_chat = chatInfo(author=author, message=message)
	try:
		db.session.add(new_chat)
		db.session.commit()
		addChat = {'author': author, 'message': message}
		return json.dumps(addChat)
		# return redirect(url_for('profile', username=author))
	except Exception as e:
		print(e)
		return 'There was an error adding your chat message'

@app.route("/messages/") 
def messages():
	all_chats = chatInfo.query.order_by(chatInfo.date_created.desc()).all()
	all_chats_json = { }
	for index, element in enumerate(all_chats):
		all_chats_json[index] = { }
		all_chats_json[index]['author'] = element.author
		all_chats_json[index]['message'] = element.message
		all_chats_json[index]['datetime'] = element.date_created.date()
	return jsonify(all_chats_json)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.secret_key = "super secret key"
    app.run(debug=True)