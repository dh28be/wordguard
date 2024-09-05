import json

# 비속어가 저장된 .txt 파일에서 줄별로 읽어와 리스트에 저장
def load_bad_words_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        bad_words = [line.strip() for line in f if line.strip()]  # 빈 줄은 무시
    return bad_words

# .txt 파일 경로
txt_file_path = "wordguard/reference/bad_words.txt"

# 비속어 리스트 로드
bad_words = load_bad_words_from_file(txt_file_path)

# JSONL 파일 생성
with open("bad_words_dataset.jsonl", "w", encoding="utf-8") as f:
    for word in bad_words:
        prompt = f"{word}\n\n이 문장에 비속어가 있는지 판별해줘"
        completion = " 포함됨"
        json_line = {"prompt": prompt, "completion": completion}
        f.write(json.dumps(json_line, ensure_ascii=False) + "\n")

print("JSONL 파일이 생성되었습니다.")
