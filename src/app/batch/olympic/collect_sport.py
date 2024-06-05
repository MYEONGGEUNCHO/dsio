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

item = {
    "3x3-basketball": [	0,	0,	1,	2,	3,	3],
    "rugby-sevens":	[0,	0,	1,	1,	2,	3],
    "swimming":	[0,	0,	1,	1,	2,	4],
    "golf":	[0,	0,	1,	2,	3,	3],
    "modern-pentathlon":  	[0,	0,	1,	3,	4,	4],
    "artistic-gymnastics":	[0,	0,	1,	3,	4,	5],
    "basketball":	[0,	0,	1,	1,	2,	3],
    "diving":	[0,	1,	2,	3,	4,	5],
    "wrestling":	[0,	1,	2,	3,	4,	5],
    "rhythmic-gymnastics":	[0,	1,	2,	3,	4,	5],
    "marathon-swimming":	[0,	0,	1,	2,	3,	4],
    "volleyball":	[0,	2,	3,	4,	5,	6],
    "badminton":	[0,	0,	1,	1,	2,	5],
    "boxing":	[0,	1,	2,	3,	4,	4],
    "breaking":	[0,	1,	2,	2,	3,	3],
    "beach-volleyball":	[0,	0,	1,	2,	3,	3],
    "shooting":	[0,	0,	1,	2,	3,	3],
    "cycling-bmx-racing":	[0,	0,	1,	2,	3,	3],
    "cycling-bmx-freestyle":	[0,	0,	1,	1,	2,	3],
    "cycling-road":	[0,	0,	1,	3,	4,	4],
    "cycling-mountain-bike":	[0,	0,	1,	2,	3,	3],
    "cycling-track":	[0,	0,	1,	2,	3,	4],
    "surfing":	[0,	0,	1,	1,	2,	2],
    "water-polo":	[0,	0,	1,	2,	3,	4],
    "skateboarding":	[0,	1,	2,	6,	7,	7],
    "sport-climbing":	[0,	1,	2,	4,	5,	6],
    "equestrian":	[0,	0,	1,	4,	5,	5],
    "artistic-swimming":	[0,	0,	1,	2,	3,	4],
    "archery":	[0,	0,	1,	3,	4,	5],
    "weightlifting":	[0,	0,	1,	2,	3,	4],
    "sailing":	[0,	0,	1,	2,	3,	3],
    "judo":	[0,	0,	1,	2,	3,	4],
    "athletics":	[0,	0,	1,	5,	6,	7],
    "rowing":	[0,	0,	1,	2,	3,	4],
    "football":	[0,	1,	2,	3,	4,	7],
    "canoe-kayak-flatwater":	[0,	0,	1,	2,	3,	3],
    "canoe-kayak-slalom":	[0,	0,	1,	3,	4,	4],
    "table-tennis":	[0,	0,	1,	2,	3,	4],
    "taekwondo":	[0,	0,	1,	1,	2,	4],
    "tennis":	[0,	0,	1,	1,	2,	2],
    "triathlon":	[0,	0,	1,	2,	3,	3],
    "trampoline-gymnastics":	[0,	0,	1,	1,	2,	2],
    "fencing":	[0,	1,	2,	3,	4,	5],
    "hockey":	[0,	3,	4,	8,	9,	11],
    "handball":	[0,	0,	1,	2,	3,	4]
}

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
        debug: bool
    ):
    sports = list_sport(debug)

    save_row = list()
    for sport in sports:
        item_dict = dict()
        url = f"https://olympics.com/ko/paris-2024/sports/{sport["sport_en_name"]}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        std_date = (datetime.now()).strftime('%Y-%m-%d')
        # GET 요청을 보내고 HTML 내용을 가져옵니다.
        try:
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()  # HTTP 요청이 성공했는지 확인
            html_content = response.content

            # BeautifulSoup을 사용하여 HTML을 파싱합니다.
            soup = BeautifulSoup(html_content, 'html.parser')

            # 대상 XPath에 해당하는 CSS 선택자
            # //*[@id="grid-container"]/section/p -> #grid-container > section > p
            # //*[@id="grid-container"]/section/p[1] -> #grid-container > section > p:nth-of-type(1)
            # //*[@id="grid-container"]/section/p[2] -> #grid-container > section > p:nth-of-type(2)
            # 종목 타이틀 이미지
            title_image_elem = soup.select_one('#p2024-main-content > div:nth-of-type(1) > section > picture > source:nth-of-type(1)')
            title_image = ""
            if title_image_elem:
                # 이미지 링크 가져오기
                title_image = title_image_elem.get('srcset')

            # CSS 선택자를 사용하여 요소를 찾습니다.
            elements = soup.select('#grid-container > section > p')
            # first_element = soup.select_one('#grid-container > section > p:nth-of-type(1)')
            # second_element = soup.select_one('#grid-container > section > p:nth-of-type(2)')

            # 결과를 출력합니다.
            bp = len(elements) / 2
            game_disc_list = []
            game_rule_list = []
            game_hist_list = []
            for idx, elem in enumerate(elements):
                if idx == bp:
                    break
                if idx < item[sport["sport_en_name"]][2]:
                    game_disc_list.append(elem.get_text(strip=True))
                    
                elif idx < item[sport["sport_en_name"]][4]:
                    game_rule_list.append(elem.get_text(strip=True))
                    
                elif idx < item[sport["sport_en_name"]][5] + 1:
                    game_hist_list.append(elem.get_text(strip=True))
            
            item_dict["sport_code"] = sport["sport_code"]
            item_dict["sport_name"] = sport["sport_name"]
            item_dict["sport_en_name"] = sport["sport_en_name"]
            item_dict["link"] = sport["link"]
            item_dict["tite_image"] = title_image
            item_dict["sport_info"] = "\n".join(game_disc_list)
            item_dict["sport_info_lsit"] = game_disc_list
            item_dict["sport_rule"] = "\n".join(game_rule_list)
            item_dict["sport_rule_list"] = game_rule_list
            item_dict["sport_history"] = "\n".join(game_hist_list)
            item_dict["sport_history_list"] = game_hist_list


            save_row.append(item_dict)
            
            
        except Exception as e:
            print(e)

    try:
        # 저장
        db_save(save_row, debug)
    except DuplicateKeyError:
        pass
    except Exception as e:
        print(e)


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