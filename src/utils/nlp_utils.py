import re
from konlpy.tag import Okt
from kiwipiepy import Kiwi
import pandas as pd

def get_token_list(
    series,
    nlp_type = "okt",
    stopwords = [],
    pos_tags = None,
    min_len = 2,
    flatten = True
):
    """
    텍스트 시리즈에서 전처리 → 형태소 분석 → (불용어, 품사, 길이) 필터 → 토큰 리스트 반환.

    Args:
        series: 문자열 iterable (예: df['text'])
        nlp_type: "okt" 또는 "kiwi"
        stopwords: 제외할 단어들
        pos_tags: 포함할 품사 태그 목록 (None/빈 리스트면 전 품사 허용)
            - OKT 예: ["Noun","Adjective"]
            - Kiwi 예: ["NNG","NNP","VA"]
            - 한국어 품사 태그 비교표: https://docs.google.com/spreadsheets/d/1OGAjUvalBuX-oZvZ_-9tEfYD2gQe7hTGsgUpiiBSXI8/edit?gid=0#gid=0
        min_len: 최소 글자 수 필터
        flatten: True면 모든 리뷰 토큰을 하나의 리스트로 병합, False면 리뷰별 리스트 유지

    Returns:
        - flatten=True  -> List[str]
        - flatten=False -> List[List[str]]
    """
    word_list = []
    
    nlp = Okt()
    if nlp_type == 'kiwi':
        nlp = Kiwi()
    
    for i, text in enumerate(series.tolist()):
        # STEP1: 데이터 전처리
        new_text = re.sub("[^a-zA-Z가-힣\\s]", "", text)

        # STEP2: 형태소 분석
        result = nlp.pos(new_text)
    
        temp_list = []
        # STEP3: 조건에 맞는 단어 담기
        for word, pos in result:
            # word의 길이가 min_len 보다 짧거나 불용어 포함시 넘어감
            if len(word) < min_len or word in stopwords:
                continue

            if pos_tags == None:                
                temp_list.append(word)
            elif pos in pos_tags:
                temp_list.append(word)
        
        if flatten:
            word_list.extend(temp_list)
        else:
            word_list.append(temp_list)
        
    return word_list