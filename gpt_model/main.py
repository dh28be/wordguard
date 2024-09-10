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
    
    prompt = f"{message}\n이 문장에서 {type}가 포함되어 있다면 그 부분을 마스킹해줘."
    print("Received Prompt:", prompt)
    
    result = gpt(prompt)

    return result

def gpt(prompt):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert assistant that helps to filter offensive words or harmful, illegal, and scam websites in the sentence. "
                    "There are two tasks you have to do."
                    "First, mask the offensive words with '***'. Consider the context while determining whether there exists offensive words or not."
                    "If a word could be harmful or offensive in a certain context, but not in another, make sure to only mask it if it is harmful or offensive in the given context."
                    "Second, mask harmful, illegal, and scam websites with '*****'. You might use scam advisor to check whether it is scam site or not."
                    "If the sentence or URL is clean and contains no offensive language or harmful content, just reply with the original sentence. "
                    "'이 문장에서 비속어 또는 유해사이트가 포함되어 있다면 그 부분을 마스킹해줘.' This part is just the command. It might not be included in the output."
                    "Do not add any other words in the output. It must be organized only with original sentence or '*'."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="ft:gpt-4o-mini-2024-07-18:personal:chat-filtering:A5uOxEEa",
        max_tokens=500
    )
    
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    app.run(host="localhost", port=80, debug=True)
