# utils/io_utils.py

def save_text_to_file(text_list, file_path):
    """
    텍스트 리스트를 줄 단위로 파일에 저장하는 함수.

    Args:
        text_list (list of str): 저장할 문자열 리스트
        file_path (str): 저장할 파일 경로

    동작:
        - 리스트의 각 문자열을 한 줄씩 기록
        - UTF-8 인코딩 사용
    """
    with open(file_path, "w", encoding="utf-8") as f:
        for text in text_list:
            f.write(f"{text}\n")


def load_text_from_file(file_path):
    """
    텍스트 파일을 읽어 문자열 리스트로 반환하는 함수.

    Args:
        file_path (str): 읽을 파일 경로

    Returns:
        list of str: 줄바꿈과 공백을 제거한 문자열 리스트

    동작:
        - 파일의 각 줄을 읽어서 양쪽 공백 제거
        - 빈 줄은 제외
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]
