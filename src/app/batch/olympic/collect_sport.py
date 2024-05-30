import re
import json
import urllib3
import requests
import os

from datetime import datetime
from bs4 import BeautifulSoup
from typing import List, Tuple, Dict, Any, Optional

from urllib import parse
from pprint import pprint
from common.http import http_get, http_post
from pymongo.errors import DuplicateKeyError
from nosql.mongo.session import client as mongo_client

from batch.olympic.common import list_sport
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



from nosql.mongo.session import client as mongo_client
from nosql.mongo.session import client_dev as mongo_client_dev


def db_save(
        result: List[Dict[str, str]]
        , debug: bool
    ):
    """MongoDB 저장 기능

    Args:
        result (List[Dict[str, str]]): 경기일정 정보 리스트 저장
    """
    if debug:
        mongo_db_dev = mongo_client_dev['olympic']
        mongo_col_dev = mongo_db_dev['sports_info']
        mongo_col_dev.insert_many(result)
    else:
        mongo_db = mongo_client['olympic']
        mongo_col = mongo_db['sports_info']
        mongo_col.insert_many(result)

def bulk_sport_info(
        sport: List[Dict[str, str]]
        , debug: bool
    ):
    pass


def collect_sport(
        sport: str
        , debug: bool
    ):
    """경기 종목 정보 수집

    Args:
        sport (List[str]): 영문종목명
    """
    # 대상 URL
    url = f"https://olympics.com/ko/paris-2024/sports/{sport}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    res = requests.get(url, headers=headers, verify=False)

    html_content = res.content

    # BeautifulSoup을 사용하여 HTML을 파싱합니다.
    soup = BeautifulSoup(html_content, 'html.parser')

    # BeautifulSoup을 사용하여 HTML을 파싱합니다.
    soup = BeautifulSoup(html_content, 'html.parser')

    # 대상 XPath에 해당하는 CSS 선택자
    # //*[@id="grid-container"]/section/p -> #grid-container > section > p
    # //*[@id="grid-container"]/section/p[1] -> #grid-container > section > p:nth-of-type(1)
    # //*[@id="grid-container"]/section/p[2] -> #grid-container > section > p:nth-of-type(2)
    # 종목 타이틀 이미지
    title_image_elem = soup.select_one('#p2024-main-content > div:nth-of-type(1) > section > picture > source:nth-of-type(1)')
    tite_image = ""
    if title_image_elem:
        # 이미지 링크 가져오기
        tite_image = title_image_elem.get('srcset') if tite_image else ""

    # CSS 선택자를 사용하여 요소를 찾습니다.
    elements = soup.select('#grid-container > section > p')
    # first_element = soup.select_one('#grid-container > section > p:nth-of-type(1)')
    # second_element = soup.select_one('#grid-container > section > p:nth-of-type(2)')

    # 결과를 출력합니다.
    bp = len(elements) / 2
    print("All elements matching //*[@id='grid-container']/section/p:")
    for idx, elem in enumerate(elements):
        if idx == bp:
            break
        print(f"elem{idx}---------------------------------")
        print(elem.get_text(strip=True))