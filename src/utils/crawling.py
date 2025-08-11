import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def collect_review_in_googlePlayStore(url, save_path, scroll_count):
    """
    구글 플레이 스토어 앱 리뷰 크롤링 함수.

    Selenium을 사용해 특정 앱의 리뷰 페이지에서 지정한 횟수만큼 스크롤하며
    작성자, 별점, 작성일, 리뷰 내용을 수집해 CSV로 저장합니다.

    Args:
        url (str): 크롤링 대상 앱의 구글 플레이 스토어 URL
        save_path (str): 저장할 CSV 파일 경로
        scroll_count (int): 리뷰 영역 스크롤 횟수

    작동 절차:
        1. 크롬 브라우저로 앱 페이지 접속 후 '리뷰 더보기' 클릭
        2. 지정한 횟수만큼 리뷰 영역 스크롤
        3. 작성자·별점·작성일·내용 추출
        4. 별점·날짜 전처리 후 CSV 저장

    주의:
        - 구글 플레이 UI 변경 시 CSS Selector 수정 필요
        - ChromeDriver 버전이 크롬과 호환되어야 함
    """

    # Chrome 창 켜기
    driver = webdriver.Chrome()
    driver.maximize_window()

    # URL로 이동
    driver.get(url)

    # 평점 및 리뷰 더보기 클릭
    more_btn_css = "#yDmH0d > c-wiz.SSPGKf.Czez9d > div > div > div:nth-child(1) > div > div.wkMJlb.YWi3ub > div > div.qZmL0 > div:nth-child(1) > c-wiz:nth-child(5) > section > header > div > div:nth-child(2) > button > i"
    more_btn = driver.find_element(By.CSS_SELECTOR, more_btn_css)
    more_btn.click()

    time.sleep(2)

    # 스크롤 내리기
    rep = scroll_count
    display_box_css = "#yDmH0d > div.VfPpkd-Sx9Kwc.cC1eCc.UDxLd.PzCPDd.HQdjr.VfPpkd-Sx9Kwc-OWXEXe-FNFY6c > div.VfPpkd-wzTsW > div > div > div > div > div.fysCi.Vk3ZVd"
    display_box = driver.find_element(By.CSS_SELECTOR, display_box_css)
    for i in range(rep):
        display_box.send_keys(Keys.END)

    # 스크롤 맨 위로 움직이기
    display_box.send_keys(Keys.HOME)

    # 리뷰 추출하기
    review_css = "#yDmH0d > div.VfPpkd-Sx9Kwc.cC1eCc.UDxLd.PzCPDd.HQdjr.VfPpkd-Sx9Kwc-OWXEXe-FNFY6c > div.VfPpkd-wzTsW > div > div > div > div > div.fysCi.Vk3ZVd > div > div:nth-child(2) > div"
    reviews = driver.find_elements(By.CSS_SELECTOR, review_css)
    reviews

    # 모든 리뷰 수집하기
    data_list = []
    # 10개정도 수집되었을 때 프린트하기
    review_count = len(reviews)
    for i, review in enumerate(reviews):
        customer_id = review.find_element(By.CLASS_NAME,'X5PpBb').text
        star = review.find_element(By.CLASS_NAME, "iXRFPc").get_attribute("aria-label")
        enroll_date = review.find_element(By.CLASS_NAME, "bp9Aid").text
        content = review.find_element(By.CLASS_NAME, "h3YV2d").text

        review_dict = {
            "customer_id": customer_id,
            "star": star,
            "enroll_date" : enroll_date,
            "content" : content
        }
        if i % 10 == 0:
            print(f"{review_count}개 중에 {i}번째 리뷰를 수집 중입니다 ....")

        data_list.append(review_dict)

    # 크롬창 닫기    
    driver.quit()

    # 데이터프레임 만들기
    import pandas as pd
    data = pd.DataFrame(data = data_list)


    # 데이터프레임 별점에 대한 전처리
    data["star"] = data["star"].apply(lambda x: int(x[10]))


    # 데이터프레임 날짜 데이터타입 변경
    data["enroll_date"] = data["enroll_date"].apply(lambda x: pd.to_datetime(x, format="%Y년 %m월 %d일"))


    # csv파일로 저장하기
    data.to_csv(save_path)