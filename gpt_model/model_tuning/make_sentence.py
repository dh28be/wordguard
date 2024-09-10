# .txt 파일에서 줄별로 읽어와 리스트에 저장
def load_words_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip()]  # 빈 줄은 무시
    return words

# 리스트의 내용을 .txt 파일로 저장
def save_words_to_file(words, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        for word in words:
            f.write(word + "\n")

mode = int(input())
if mode == 0:
    # input file 주소
    input_file_path = "gpt_model/model_tuning/files/illegal_sites.txt"
    output_file1_path = "gpt_model/model_tuning/files/illegal_site_sentence.txt"
    output_file2_path = "gpt_model/model_tuning/files/illegal_mask_site_sentence.txt"

    # 입력 파일에서 데이터 읽어오기
    illegal_sites = load_words_from_file(input_file_path)

    site_sentence_formats = [
        "{} 이 사이트로 들어가셔서 로그인하시면 됩니다.",
        "다음 사이트로 접속하세요 {}",
        "인생에 단 한번뿐인 기회!! 지금 당장 접속하세요. {}",
        "정부에서 공식적으로 운영중인 이 사이트로 들어오세요. {}"
    ]

    illegal_site_sentences = []
    illegal_mask_site_sentences = []
    for i in range(len(illegal_sites)):
        illegal_site = illegal_sites[i]
        illegal_mask_site = "*" * 6
        
        sentence_format = site_sentence_formats[i % 4]
        illegal_site_sentences.append(sentence_format.format(illegal_site))
        illegal_mask_site_sentences.append(sentence_format.format(illegal_mask_site))


    # 데이터 저장
    save_words_to_file(illegal_site_sentences, output_file1_path)
    save_words_to_file(illegal_mask_site_sentences, output_file2_path)

    print("유해사이트 포함 문장 목록 완성")
else:
    # input file 주소
    input_file_path = "gpt_model/model_tuning/files/normal_sites.txt"
    output_file_path = "gpt_model/model_tuning/files/normal_site_sentence.txt"

    # 입력 파일에서 데이터 읽어오기
    illegal_sites = load_words_from_file(input_file_path)

    site_sentence_formats = [
        "{} 이 사이트로 들어가셔서 로그인하시면 됩니다.",
        "다음 사이트로 접속하세요 {}",
        "인생에 단 한번뿐인 기회!! 지금 당장 접속하세요. {}",
        "정부에서 공식적으로 운영중인 이 사이트로 들어오세요. {}"
    ]

    normal_site_sentences = []
    for i in range(len(illegal_sites)):
        illegal_site = illegal_sites[i]
        
        sentence_format = site_sentence_formats[i % 4]
        normal_site_sentences.append(sentence_format.format(illegal_site))


    # 데이터 저장
    save_words_to_file(normal_site_sentences, output_file_path)

    print("정상사이트 포함 문장 목록 완성")