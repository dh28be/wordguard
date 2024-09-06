import os
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

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
    
    prompt = f"{message}\n이 문장에 {type}가 포함되어 있는지 판별해줘."
    print("Received Prompt:", prompt)
    
    if type == "비속어":
        result = detect_offensive_language(prompt)
    elif type == "유해사이트":
        result = detect_harmful_website(prompt)
    else:
        # 비속어 감지 + 유해사이트 감지 둘 다 실행
        offensive_result = detect_offensive_language(prompt)
        harmful_website_result = detect_harmful_website(prompt)
        result = offensive_result + '\n' + harmful_website_result
    
    return result

def detect_offensive_language(prompt):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert assistant that helps to detect offensive language. "
                    "Always reply with a clear statement about whether offensive language is present or not. "
                    "The most important thing is to consider the context. If it has the same letter but has different meaning, the result has to be different."
                    "So, consider the context and answer whether it has offensive word or not."
                    "If there is any offensive language, respond with '비속어 포함됨'. "
                    "If not, respond with '비속어 포함되지 않음'."
                    "The response format must be one of these two. Make sure the answer not to end with '.'."
                    "Make sure to consider the offensive word used in games. The user could have changed the format not to get filtered. ex) 엄마없네, 18ㅅㅐㄲㅣ, tlqkf년아"
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="ft:gpt-3.5-turbo-0125:personal:offensive-word-detector-v2:A4NeG62b",
        max_tokens=500
    )
    
    return chat_completion.choices[0].message.content

def detect_harmful_website(prompt):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert assistant that helps to detect illegal, harmful, or scam websites. "
                    "Always reply with a clear statement about whether the website is illegal, harmful, or a scam. "
                    "The most important thing is to consider the context. Some websites may seem legitimate but may contain harmful or scam-related content. "
                    "So, consider the URL structure, content, and keywords carefully to determine if the site is suspicious. "
                    "If the website is illegal, harmful, or a scam, respond with '유해 사이트 포함됨'. "
                    "If the website is safe, respond with '유해 사이트 포함되지 않음'."
                    "The response format must be one of these two. If you even don't know, just answer '유해 사이트 포함되지 않음'."
                    "Make sure the answer not to end with '.'."
                    "Make sure to consider sites that may involve phishing, online scams, fake marketplaces, illegal downloads, or adult content."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="gpt-3.5-turbo-0125",
        max_tokens=500
    )
    
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    app.run(host="localhost", port=80, debug=True)
