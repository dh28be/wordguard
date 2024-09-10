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
    message = message.replace('\n', '').strip()
    type = data["type"]
    
    prompt = f"{message}"
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
                    "First, mask the offensive words with '***'. Do not classify a word as offensive if the sentence does not convey an aggressive or hostile tone, considering the context."
                    "If you're not certain whether a word contains offensive language, assume that it does not."
                    "Second, mask harmful, illegal, and scam websites with '*****'. You might use scam advisor to check whether it is scam site or not."
                    "If the sentence or URL is clean and contains no offensive language or harmful content, just reply with the original input sentence."
                    "Do not add any other words in the output."
                    "When masking harmful websites, mask the entire URL."
                    "When masking offensive language, if a phrase like '엄마 없냐' is combined to form a single offensive expression, recognize it as one offensive word and mask it as '***'."
                    "Response has to be consistent, for the same input."
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
    app.run(host="localhost", port=80, debug=True)
