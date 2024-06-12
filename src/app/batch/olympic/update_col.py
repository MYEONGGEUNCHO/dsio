import re
import json
import urllib3
import requests
import os
import locale

from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from typing import List, Tuple, Dict, Any, Optional

from urllib import parse
from pprint import pprint
from common.http import http_get, http_post
from pymongo.errors import DuplicateKeyError
from nosql.mongo.session import client as mongo_client
from nosql.mongo.session import client_dev as mongo_client_dev
from db.session import engine, engine_dev, SessionLocal, SessionLocal_dev
from sqlalchemy import text 

from batch.olympic.common import list_sport
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def update_col(debug: bool):
    if debug:
        mongo_db_dev = mongo_client_dev['olympic']
        mongo_col_a = mongo_db_dev['changed_stadium']
        mongo_col_b = mongo_db_dev['schedule_stadium_info']
    else:
        mongo_db = mongo_client['olympic']
        mongo_col_a = mongo_db['changed_stadium']
        mongo_col_b = mongo_db['schedule_stadium_info']

    docs = mongo_col_a.find()
    D = [doc for doc in docs]

    for idx, d in enumerate(D, 1):
        print(f'진행률 {idx}/{len(D)}')
        
        mongo_col_b.update_one({
            '_id': d['_id']
        }, {
            '$set': {
                'stadium': d['stadium_ko_name']
            }
        })

def update_pymongo(mongo_col_b, select, update):

    docs = mongo_col_b.find()
    D = [doc for doc in docs]

    for idx, d in enumerate(D, 1):
        print(f'진행률 {idx}/{len(D)}')
        
        mongo_col_b.update_one(select, update)


def update_schedule_info(
        issu_dt_start: str = ''
        , tcals1: int = 0
        , debug: bool = False
    ):
    if debug:
        mongo_db_dev = mongo_client_dev['olympic']
        mongo_col_a = mongo_db_dev['schedule_info']
        mongo_col_b = mongo_db_dev['schedule_stadium_info']
    else:
        mongo_db = mongo_client['olympic']
        mongo_col_a = mongo_db['schedule_info']
        mongo_col_b = mongo_db['schedule_stadium_info']
    
    # 날짜가 없으면, 당일 일자로 계산해서 조회
    if issu_dt_start == '':
        issu_dt_start = (datetime.now() + timedelta(days=tcals1)).strftime('%Y-%m-%d')
    # 날짜가 있으면, 해당 일자로 계산해서 조회
    else:
        check_date = datetime.strptime(issu_dt_start, '%Y-%m-%d')
        check_date_cals = check_date + timedelta(tcals1)
        issu_dt_start = check_date_cals.strftime('%Y-%m-%d')

    query = {
        "std_date" : issu_dt_start
    }

    docs = mongo_col_a.find(query, no_cursor_timeout=True)
    D = [doc for doc in docs]

    for idx, d in enumerate(D, 1):
        print(f'진행률 {idx}/{len(D)}')

        select = {
            "sport_en_name": d["sport_en_name"],
            "stadium": d["stadium"],
            "tournament": d["tournament"],
            "korea_date": d["korea_date"],
            "korea_time": d["korea_time"]
        }

        update = {
            '$set': {
                "std_date": d["std_date"],
                "sport_name": d['sport_name'],
                "sport_en_name": d['sport_en_name'],
                "stadium": d['stadium'],
                "tournament": d['tournament'],
                "country": d['country'],
                "country1_name": d['country1_name'],
                "country1_flag": d['country1_flag'],
                "country2_name": d['country2_name'],
                "country2_flag": d['country2_flag'],
                "paris_date": d['paris_date'],
                "paris_time": d['paris_time'],
                "korea_date": d['korea_date'],
                "korea_time": d['korea_time'],
            }
        }

        update_pymongo(mongo_col_b=mongo_col_b, select=select, update=update)

        

