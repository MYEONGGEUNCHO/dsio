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

def list_schedule(debug: bool) -> List[str]:
    """MongoDB 종목정보 테이블에서 Mysql 경기장정보 테이블로 데이터 insert

    Returns:
        List[str]: 경기장 리스트
    """
    if debug:
        mongo_db_dev = mongo_client_dev['olympic']
        mongo_col_a = mongo_db_dev['schedule_stadium_join']
        mongo_col_b = mongo_db_dev['stadium_info']
    else:
        mongo_db = mongo_client['olympic']
        mongo_col_a = mongo_db['schedule_stadium_join']
        mongo_col_b = mongo_db['stadium_info']
    # 조인 쿼리 작성
    pipeline = [
        {
            '$lookup': {
                'from': 'stadium_info',  # 조인할 컬렉션
                'localField': 'stadium',  # orders 컬렉션에서의 필드
                'foreignField': 'stadium_ko_name',  # customers 컬렉션에서의 필드
                'as': 'stadium_info'  # 조인 결과를 저장할 필드 이름
            }
        }
    ]
    # 조인 수행
    docs = mongo_col_a.aggregate(pipeline)

    D = [doc for doc in docs]
    return D





def batch_item(debug: bool):
    """MongoDB 경기장정보 테이블에서 Mysql 경기장정보 테이블로 데이터 insert
    """
    if debug:
        db = SessionLocal()
        
    else:
        db = SessionLocal()
    D = list_schedule(debug)

    try:
        for idx, d in enumerate(D, 1):
            print(f'진행률 {idx}/{len(D)}-----------------------------------')
            query = text('''
                INSERT INTO item (
                    a_seat_sold, b_seat_sold, c_seat_sold, d_seat_sold,
                    vip_seat_sold, state, korean_advancement, a_seat_price,
                    b_seat_price, c_seat_price, d_seat_price, vip_seat_price,
                    game_id
                ) VALUES (
                    :a_seat_sold, :b_seat_sold, :c_seat_sold, :d_seat_sold,
                    :vip_seat_sold, :state, :korean_advancement, :a_seat_price,
                    :b_seat_price, :c_seat_price, :d_seat_price, :vip_seat_price,
                    :game_id
                )
            ''')
            
            db.execute(query, {
                "a_seat_sold" : 0,
                "b_seat_sold" : 0,
                "c_seat_sold" : 0,
                "d_seat_sold" : 0,
                "vip_seat_sold" : 0,
                "state" : 1,
                "korean_advancement" : 0,
                "a_seat_price" : 100000 if d["stadium_info"][0]["a_seat_quantity"] != 0 else 0,
                "b_seat_price" : 100000 if d["stadium_info"][0]["b_seat_quantity"] != 0 else 0,
                "c_seat_price" : 100000 if d["stadium_info"][0]["c_seat_quantity"] != 0 else 0,
                "d_seat_price" : 100000 if d["stadium_info"][0]["d_seat_quantity"] != 0 else 0,
                "vip_seat_price" : 200000 if d["stadium_info"][0]["vip_seat_quantity"] != 0 else 0,
                "game_id" : d["game_id"]
            })
        
        db.commit()
        print("Data insertion successful.")
    except Exception as e:
        db.rollback()
        print(f"Error Inserting Data: {e}")
    finally:
        db.close()