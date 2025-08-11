# utils/list_utils.py
def flatten_2d_list(nested_list):
    """
    2차원 리스트를 1차원 리스트로 변환하는 함수.

    Args:
        nested_list (list of lists): 2차원 리스트

    Returns:
        list: 평탄화된 1차원 리스트
    """
    return [item for sublist in nested_list for item in sublist]
