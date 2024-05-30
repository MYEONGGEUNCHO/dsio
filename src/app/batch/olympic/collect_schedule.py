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
from nosql.mongo.session import client_dev as mongo_client_dev

from batch.olympic.common import list_sport
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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
        mongo_col_dev = mongo_db_dev['schedule_info']
        mongo_col_dev.insert_many(result)
    else:
        mongo_db = mongo_client['olympic']
        mongo_col = mongo_db['schedule_info']
        mongo_col.insert_many(result)

def collect_schedule_test():
    # 대상 URL
    url = "https://olympics.com/ko/paris-2024/schedule/basketball"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    # GET 요청을 보내고 HTML 내용을 가져옵니다.
    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()  # HTTP 요청이 성공했는지 확인
        html_content = response.content

        # BeautifulSoup을 사용하여 HTML을 파싱합니다.
        soup = BeautifulSoup(html_content, 'html.parser')

        # # CSS 선택자 사용
        # css_selector = '#p2024-main-content > div:nth-child(1) > div > div.PreGamesSchedule-styles__SportEventListContainer-sc-9792ac12-0.fEJXtp'
        # target_element = soup.select_one(css_selector)

        # # 요소가 존재하는지 확인하고 텍스트를 추출합니다.
        # if target_element:
        #     print("Target element text:")
        #     print(target_element)
        #     # print(target_element.get_text(strip=True))
        # else:
        #     print("Element not found:", css_selector)

        # 타겟 요소를 CSS 선택자로 찾기
        target_element = soup.select_one("#p2024-main-content > div:nth-child(1) > div > div.PreGamesSchedule-styles__SportEventListContainer-sc-9792ac12-0.fEJXtp")
        
        # 텍스트 데이터 추출 및 딕셔너리로 정리
        if target_element:
            elements_dict = {}
            for elem in target_element.find_all(recursive=True):
                class_name = ' '.join(elem.get('class', []))
                if class_name:  # 클래스가 있는 요소만 추가
                    text = elem.get_text(separator=" ", strip=True)
                    if class_name in elements_dict:
                        elements_dict[class_name].append(text)
                    else:
                        elements_dict[class_name] = [text]
            
            # 결과 출력
            for key, value in elements_dict.items():
                print(f"클래스명: {key}")
                for text in value:
                    print(f"  - {text}")
        else:
            print("타겟 요소를 찾을 수 없습니다.")

    except requests.exceptions.RequestException as e:
        print(f"HTTP 요청 중 오류가 발생했습니다: {e}")




def list_schedule(debug: bool):
    """경기일정 정보 전체 리스트 저장 기능
    """
    # 대상 URL
    sports = list_sport(debug)

    for sport in sports:
        url = f"https://olympics.com/ko/paris-2024/schedule/{sport}"
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

            # 타겟 요소를 CSS 선택자로 찾기
            target_element = soup.select_one("#p2024-main-content > div:nth-child(1) > div > div.PreGamesSchedule-styles__SportEventListContainer-sc-9792ac12-0.fEJXtp")
            
            # 텍스트 데이터 추출 및 딕셔너리로 정리
            
            save_row = list()
            if target_element:
                for elem in target_element:
                    date_elem = elem.find(class_="SportScheduleEventsList-styles__DateContainer-sc-4f7d284d-1")
                    stadium_elem = elem.find(class_="EventList-styles__VenueContainer-sc-32051fc0-2")
                    tournament_info = elem.find_all(class_="EventList-styles__EventContainer-sc-32051fc0-1")
                    
                    for schedule in tournament_info:
                        elements_dict = dict()
                        time_elem = schedule.find(class_="EventListItem-styles__Time-sc-6aa92e06-2")
                        tournament_elem = schedule.find(class_="EventListItem-styles__ContentContainer-sc-6aa92e06-3")
                    

                        country = schedule.find(class_="EventListItem-styles__MatchContainer-sc-6aa92e06-4")
                        left_country = schedule.find(class_='EventListItem-styles__LeftCountryContainer-sc-6aa92e06-11')
                        right_country = schedule.find(class_='EventListItem-styles__RightCountryContainer-sc-6aa92e06-12')
                        
                        elements_dict['std_date'] = std_date
                        elements_dict['game_name'] = sport
                        elements_dict['date'] = date_elem.get_text(separator=" ", strip=True) if date_elem else ""
                        elements_dict['stadium'] = stadium_elem.get_text(separator=" ", strip=True) if stadium_elem else ""
                        elements_dict['time'] = time_elem.get_text(separator=" ", strip=True) if time_elem else ""
                        elements_dict['tournament'] = tournament_elem.get_text(separator=" ", strip=True) if tournament_elem else ""
                        elements_dict['country'] = country.get_text(separator=" ", strip=True) if country else ""
                        elements_dict['left_country'] = left_country.get_text(separator=" ", strip=True) if left_country else ""
                        elements_dict['left_country_flag'] = left_country.find('img')['src'] if left_country else ""
                        elements_dict['right_country'] = right_country.get_text(separator=" ", strip=True) if right_country else ""
                        elements_dict['right_country_flag'] = right_country.find('img')['src'] if right_country else ""

                        save_row.append(elements_dict)
            else:
                print("타겟 요소를 찾을 수 없습니다.")
            
            # 결과 출력
            # pprint(save_row)
            try:
                # 저장
                db_save(save_row, debug)
            except DuplicateKeyError:
                continue
            except Exception as e:
                print(e)

        except requests.exceptions.RequestException as e:
            print(f"HTTP 요청 중 오류가 발생했습니다: {e}")
            
        except Exception as e:
            print(e)
            pprint(f"요청 실패: {response.status_code}")


def collect_schedule(
        sport: str
        , debug: bool
    ):
    """단일 스포츠 종목 수집 기능

    Args:
        sports (str): 종목 영문명
    """
    # 대상 URL
    url = f"https://olympics.com/ko/paris-2024/schedule/{sport}"
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

        # 타겟 요소를 CSS 선택자로 찾기
        target_element = soup.select_one("#p2024-main-content > div:nth-child(1) > div > div.PreGamesSchedule-styles__SportEventListContainer-sc-9792ac12-0.fEJXtp")
        
        # 텍스트 데이터 추출 및 딕셔너리로 정리
        
        if target_element:
            save_row = list()
            for elem in target_element:
                date_elem = elem.find(class_="SportScheduleEventsList-styles__DateContainer-sc-4f7d284d-1")
                stadium_elem = elem.find(class_="EventList-styles__VenueContainer-sc-32051fc0-2")
                sports = elem.find_all(class_="EventList-styles__EventContainer-sc-32051fc0-1")
                
                for sport in sports:
                    elements_dict = dict()
                    time_elem = sport.find(class_="EventListItem-styles__Time-sc-6aa92e06-2")
                    tournament_elem = sport.find(class_="EventListItem-styles__ContentContainer-sc-6aa92e06-3")
                

                    country = sport.find(class_="EventListItem-styles__MatchContainer-sc-6aa92e06-4")
                    left_country = sport.find(class_='EventListItem-styles__LeftCountryContainer-sc-6aa92e06-11')
                    right_country = sport.find(class_='EventListItem-styles__RightCountryContainer-sc-6aa92e06-12')
                    
          
                    elements_dict['std_date'] = std_date
                    elements_dict['game_name'] = sport
                    elements_dict['date'] = date_elem.get_text(separator=" ", strip=True) if date_elem else ""
                    elements_dict['stadium'] = stadium_elem.get_text(separator=" ", strip=True) if stadium_elem else ""
                    elements_dict['time'] = time_elem.get_text(separator=" ", strip=True) if time_elem else ""
                    elements_dict['tournament'] = tournament_elem.get_text(separator=" ", strip=True) if tournament_elem else ""
                    elements_dict['country'] = country.get_text(separator=" ", strip=True) if country else ""
                    elements_dict['left_country'] = left_country.get_text(separator=" ", strip=True) if left_country else ""
                    elements_dict['left_country_flag'] = left_country.find('img')['src'] if left_country else ""
                    elements_dict['right_country'] = right_country.get_text(separator=" ", strip=True) if right_country else ""
                    elements_dict['right_country_flag'] = right_country.find('img')['src'] if right_country else ""

                    save_row.append(elements_dict)
        else:
            print("타겟 요소를 찾을 수 없습니다.")
        
        # 결과 출력
        # pprint(save_row)

        try:
            # 저장
            db_save(save_row, debug)
        except DuplicateKeyError as e:
            print(e)
        except Exception as e:
            print(e)

    except requests.exceptions.RequestException as e:
        print(f"HTTP 요청 중 오류가 발생했습니다: {e}")
        
    except Exception as e:
        print(e)
        pprint(f"요청 실패: {response.status_code}")

