import json
import random

# 파일 경로 설정 (파일 경로를 실제 경로로 대체하세요)
input_file_path = 'gpt_model/model_tuning/dataset.jsonl'  # 읽을 파일 경로
train_file_path = 'gpt_model/model_tuning/train_dataset.jsonl'  # train 파일 경로
valid_file_path = 'gpt_model/model_tuning/valid_dataset.jsonl'  # valid 파일 경로

# jsonl 파일 읽기
with open(input_file_path, 'r', encoding='utf-8') as file:
    data = [json.loads(line) for line in file]  # jsonl 파일을 리스트로 변환

# 20% 랜덤 샘플링
random.shuffle(data)
split_index = int(len(data) * 0.2)

# Train과 Valid 데이터셋으로 나누기
valid_data = data[:split_index]
train_data = data[split_index:]

# Train 데이터셋 저장
with open(train_file_path, 'w', encoding='utf-8') as train_file:
    for entry in train_data:
        json.dump(entry, train_file, ensure_ascii=False)
        train_file.write('\n')

# Valid 데이터셋 저장
with open(valid_file_path, 'w', encoding='utf-8') as valid_file:
    for entry in valid_data:
        json.dump(entry, valid_file, ensure_ascii=False)
        valid_file.write('\n')