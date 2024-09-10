import json

# .txt 파일에서 줄별로 읽어와 리스트에 저장
def load_words_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip()]  # 빈 줄은 무시
    return words

# .txt 파일 경로
offensive_file_path = "gpt_model/model_tuning/files/offensive.txt"
offensive_mask_file_path = "gpt_model/model_tuning/files/offensive_mask.txt"
normal_file_path = "gpt_model/model_tuning/files/normal.txt"

illegal_file_path = "gpt_model/model_tuning/files/illegal_site_sentence.txt"
illegal_mask_file_path = "gpt_model/model_tuning/files/illegal_mask_site_sentence.txt"
normal_site_file_path = "gpt_model/model_tuning/files/normal_site_sentence.txt"

# 파일 로드
offensive_sentences = load_words_from_file(offensive_file_path)
offensive_mask_sentences = load_words_from_file(offensive_mask_file_path)
normal_sentences = load_words_from_file(normal_file_path)

illegal_site_sentences = load_words_from_file(illegal_file_path)
illegal_mask_site_sentences = load_words_from_file(illegal_mask_file_path)
normal_site_sentences = load_words_from_file(normal_site_file_path)

# JSONL 파일 생성
with open("gpt_model/model_tuning/dataset.jsonl", "w", encoding="utf-8") as f:

    # 비속어 파일 단일 생성
    for i in range(100):
        offensive_sentence = offensive_sentences[i]
        offensive_mask_sentence = offensive_mask_sentences[i]
        json_line = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert assistant that helps to filter offensive language or harmful, illegal, or scam websites in the sentence. "
                },
                {
                    "role": "user",
                    "content": f"{offensive_sentence}\n이 문장에서 비속어 또는 유해사이트가 포함되어 있다면 그 부분을 마스킹해줘."
                },
                {
                    "role": "assistant",
                    "content": f"{offensive_mask_sentence}"
                }
            ]
        }
        f.write(json.dumps(json_line, ensure_ascii=False) + "\n")

        normal_sentence = normal_sentences[i]
        json_line = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert assistant that helps to filter offensive language or harmful, illegal, or scam websites in the sentence. "
                },
                {
                    "role": "user",
                    "content": f"{normal_sentence}\n이 문장에서 비속어 또는 유해사이트가 포함되어 있다면 그 부분을 마스킹해줘."
                },
                {
                    "role": "assistant",
                    "content": f"{normal_sentence}"
                }
            ]
        }
        f.write(json.dumps(json_line, ensure_ascii=False) + "\n")


    # 유해사이트 파일 단일 생성
    for i in range(30):
        illegal_site_sentence = illegal_site_sentences[i]
        illegal_mask_site_sentence = illegal_mask_site_sentences[i]

        json_line = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert assistant that helps to filter offensive language or harmful, illegal, or scam websites in the sentence. "
                },
                {
                    "role": "user",
                    "content": f"{illegal_site_sentence}\n이 문장에서 비속어 또는 유해사이트가 포함되어 있다면 그 부분을 마스킹해줘."
                },
                {
                    "role": "assistant",
                    "content": f"{illegal_mask_site_sentence}"
                }
            ]
        }
        f.write(json.dumps(json_line, ensure_ascii=False) + "\n")

        normal_site_sentence = normal_site_sentences[i]

        json_line = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert assistant that helps to filter offensive language or harmful, illegal, or scam websites in the sentence. "
                },
                {
                    "role": "user",
                    "content": f"{normal_site_sentence}\n이 문장에서 비속어 또는 유해사이트가 포함되어 있다면 그 부분을 마스킹해줘."
                },
                {
                    "role": "assistant",
                    "content": f"{normal_site_sentence}"
                }
            ]
        }
        f.write(json.dumps(json_line, ensure_ascii=False) + "\n")

    # 비속어 + 유해사이트 생성
    for i in range(10):
        offensive_sentence = offensive_sentences[i]
        offensive_mask_sentence = offensive_mask_sentences[i]
        normal_sentence = normal_sentences[i]

        iillegal_site_sentence = illegal_site_sentences[i]
        illegal_mask_site_sentence = illegal_mask_site_sentences[i]
        normal_site_sentence = normal_site_sentences[i]

        for j in range(4):
            if j == 0:
                ask = offensive_sentence + " " + illegal_site_sentence
                answer = offensive_mask_sentence + " " + illegal_mask_site_sentence
            elif j == 1:
                ask = offensive_sentence + " " + normal_site_sentence
                answer = offensive_mask_sentence + " " + normal_site_sentence
            elif j == 2:
                ask = normal_sentence + " " + illegal_site_sentence
                answer = normal_sentence + " " + illegal_mask_site_sentence
            else:
                ask = normal_sentence + " " + normal_site_sentence
                answer = normal_sentence + " " + normal_site_sentence
                    
            json_line = {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert assistant that helps to filter offensive language or harmful, illegal, or scam websites in the sentence. "
                    },
                    {
                        "role": "user",
                        "content": f"{ask}\n이 문장에서 비속어 또는 유해사이트가 포함되어 있다면 그 부분을 마스킹해줘."
                    },
                    {
                        "role": "assistant",
                        "content": f"{answer}"
                    }
                ]
            }
            f.write(json.dumps(json_line, ensure_ascii=False) + "\n")

print("JSONL 파일이 생성되었습니다.")