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
    # type = data["type"]
    
    prompt = f"{message}"
    print("Received Prompt:", prompt)
    
    mode = int(determine_existence(prompt))

    if mode == 0:
        result = illegal_mask(offensive_mask(prompt))
    elif mode == 1:
        result = offensive_mask(prompt)
    elif mode == 2:
        result = illegal_mask(prompt)
    else:
        result = prompt

    return str(mode) + result

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
                    "Make sure to filter out subtle insults or cleverly disguised offensive language used in games like 'ㅇㅁ 없음?'."
                    "Also treat insults made up of initials as offensive language when the context is quite aggresive. You should always consider the context."
                    "Meaningless word like 엄 and duplication of it are not a offensive word. "
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
        model="gpt-4o-2024-08-06",
        #model="ft:gpt-4o-mini-2024-07-18:personal:chat-filtering:A64JvdnK",
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
                    "Make sure to filter out subtle insults or cleverly disguised offensive language used in games like 'ㅇㅁ 없음?'."
                    "Also treat insults made up of initials as offensive language."
                    "If you cannot find any offensive word, just output the original sentence."
                    "If the whole sentence is insulting, mask the whole sentence."
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
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="gpt-4o-2024-08-06",
        max_tokens=500
    )
    
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    app.run(host="localhost", port=80, debug=True)
