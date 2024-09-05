import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

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
                    "The response format must be one of this two."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="gpt-3.5-turbo",
        max_tokens=500
    )

    
    return chat_completion.choices[0].message.content

def load_bad_words_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        bad_words = [line.strip() for line in f if line.strip()]  # 빈 줄은 무시
    return bad_words

# .txt 파일 경로
txt_file_path = "wordguard/gpt_model/bad_words.txt"

# 비속어 리스트 로드
bad_words = load_bad_words_from_file(txt_file_path)
ans = 0
cnt = 0

with open("not_filtered.txt", "w", encoding="utf-8") as f:
    for word in bad_words:
        prompt = f"{word}\n\n이 문장에 비속어가 있는지 판별해줘"
        result = gpt(prompt)
        if result != "비속어 포함":
            f.write(word + "\n")
            ans += 1
        print(cnt)
        cnt += 1

    print(ans)