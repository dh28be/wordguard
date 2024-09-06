import json

# 비속어가 저장된 .txt 파일에서 줄별로 읽어와 리스트에 저장
def load_words_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip()]  # 빈 줄은 무시
    return words

# .txt 파일 경로
bad_words_file_path = "gpt_model/test/not_filtered.txt"
good_words_file_path = "gpt_model/test/good_words.txt"

# 비속어 리스트 로드
bad_words = load_words_from_file(bad_words_file_path)
good_words = load_words_from_file(good_words_file_path)

# JSONL 파일 생성
with open("gpt_model/dataset.jsonl", "w", encoding="utf-8") as f:
    for i in range(90):
        bad_word = bad_words[i]
        json_line = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant who detects offensive language in sentences considering the context."
                },
                {
                    "role": "user",
                    "content": f"'{bad_word}'\n 이 문장에 비속어가 포함되어 있는지 판별해줘."
                },
                {
                    "role": "assistant",
                    "content": "비속어 포함됨"
                }
            ]
        }
        f.write(json.dumps(json_line, ensure_ascii=False) + "\n")

        good_word = good_words[i]
        json_line = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant who detects offensive language in sentences considering the context."
                },
                {
                    "role": "user",
                    "content": f"'{good_word}'\n 이 문장에 비속어가 포함되어 있는지 판별해줘."
                },
                {
                    "role": "assistant",
                    "content": "비속어 포함되지 않음"
                }
            ]
        }
        f.write(json.dumps(json_line, ensure_ascii=False) + "\n")

print("JSONL 파일이 생성되었습니다.")