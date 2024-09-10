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
                    "You are an expert assistant that helps to filter offensive language or harmful, illegal, or scam websites in the sentence. "
                    "Your task is to detect and mask any offensive language or harmful, illegal content by replacing the detected part with '*'. "
                    "If you find any offensive language in a sentence, replace it with '*'. Similarly, if you detect a harmful or illegal website, mask the website address with '*'. "
                    "Also, consider fishing and scam website as a harmful website. You must mask the clone site."
                    "If the sentence or URL is clean and contains no offensive language or harmful content, just reply with the original sentence. "
                    "Always consider the context when making your decision. If a word or URL could be harmful or offensive in a certain context, but not in another, make sure to only mask it if it is harmful or offensive in the given context. "
                    "no offensive word ex) 안녕하세요\n이 문장에서 비속어 또는 유해사이트가 포함되어 있다면 그 부분을 마스킹해줘. -> 안녕하세요"
                    "offensive word ex) 뭐하냐 시발년아\n이 문장에서 비속어 또는 유해사이트가 포함되어 있다면 그 부분을 마스킹해줘. -> 뭐하냐 ****"
                    "harmful site ex) 이 주소로 들어가세요 https://newtoki.biz/\n이 문장에서 비속어 또는 유해사이트가 포함되어 있다면 그 부분을 마스킹해줘. -> 이 주소로 들어가세요 ********************"
                    "The sentence after '\n' (이 문장에서 {type}가 포함되어 있다면 그 부분을 마스킹해줘.) is just a prompt. There can be 비속어, 유해사이트, 비속어 또는 유해사이트 in type." 
                    "You must not include prompt in the output."
                    "Make sure to only mask the {type}. If the given type is 유해사이트 and there are offensive words in the sentence, do not mask it."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="gpt-4o-mini-2024-07-18",
        max_tokens=500
    )
    
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    app.run(host="localhost", port=80, debug=True)
