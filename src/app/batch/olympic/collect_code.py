import os
import json
from typing import List, Tuple, Dict, Any, Optional
from batch.olympic.common import list_sport
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
        mongo_col_dev = mongo_db_dev['code_info']
        mongo_col_dev.insert_many(result)
    else:
        mongo_db = mongo_client['olympic']
        mongo_col = mongo_db['code_info']
        mongo_col.insert_many(result)


def collect_code(
        debug: bool    
    ):
    """JSON파일 변환하여 올림픽 종목 코드 정보 저장
    """
    # json파일 읽기
    input_file_path = os.path.join(os.path.dirname(__file__), 'displine.json')
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    sports_list = list()

    for discipline in data["disciplines"]:
        new_discipline = {
            "game_name": discipline["title"].strip(),
            "game_en_name": discipline["slug"].replace("discipline-", ""),
            "link": discipline["hrefLink"],
            "game_code": discipline["OdfCode"]
        }
        sports_list.append(new_discipline)
    db_save(sports_list, debug)
