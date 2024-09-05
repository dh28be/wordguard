import os
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, request, render_template

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
    
    prompt = f"{message}\n\n이 문장에 {type}가 있는지 판별해줘."
    print("Received Prompt:", prompt)
    
    return gpt(prompt)

def gpt(prompt):
    client = OpenAI(
        # This is the default and can be omitted
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
                    "So, consider the context and answer wheter it has offensive word or not."
                    "If there is any offensive language, respond with '비속어 포함'. "
                    "If not, respond with '비속어 포함되지 않음'."
                )
            },
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