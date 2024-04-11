#-*-coding:utf-8-*-
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options

import pandas as pd
import time
import re
import csv
import datetime
page = 0
asd = 1
def crawl_current_page():
    # 현재 페이지의 abstracts 요소를 새롭게 찾아서 처리
    abstracts = WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "thesis__abstract"))
    )
    
    with open('myenv/DBpia_crawler/crawled.txt', 'a', encoding='utf-8') as file:
        for abstract in abstracts:
            file.write(abstract.text + "\n\n")  # 각 abstract의 텍스트를 파일에 쓰기

def go_to_next_page():
    """다음 페이지로 넘어가는 JavaScript 함수를 실행"""
    global page
    try:
        driver.execute_script(f"setPageNum({page})")
        # 페이지 넘김 후 충분한 로딩 시간을 기다림
        time.sleep(2)  # 필요에 따라 대기 시간 조절
        return True
    except Exception as e:
        print(f"다음 페이지로 넘어가는 데 실패: {e}")
        return False
    
searchQ = "Chat GPT"
startYear = 2021
endYear = 2025

print("start crawling..")
chrome_options = Options()
driver = webdriver.Chrome()

#스타트업 검색
driver.get('https://www.dbpia.co.kr/')
keyword = driver.find_element(By.ID, 'searchInput')
keyword.clear()
keyword.send_keys(searchQ)
keyword.send_keys(Keys.RETURN)

# 첫 페이지에서 시작하여 모든 페이지를 순회
while True:
    page += 1
    print(page)
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, "thesis__abstract")))
    if asd == 0:
        asd = 1
        if not go_to_next_page():  # 다음 페이지로 넘어가기 시도, 불가능하면 종료
            break
    else:
        crawl_current_page()  # 현재 페이지의 내용을 크롤링하고 파일에 저장
    
        if not go_to_next_page():  # 다음 페이지로 넘어가기 시도, 불가능하면 종료
            break

# WebDriver 종료
driver.quit()

print("Crawling and writing to file completed.")
