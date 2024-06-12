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

def list_stadium(debug: bool) -> List[str]:
    """MongoDB 종목정보 테이블에서 Mysql 경기장정보 테이블로 데이터 insert

    Returns:
        List[str]: 경기장 리스트
    """
    if debug:
        mongo_db_dev = mongo_client_dev['olympic']
        mongo_col = mongo_db_dev['stadium_info']
    else:
        mongo_db = mongo_client['olympic']
        mongo_col = mongo_db['stadium_info']

    docs = mongo_col.find()

    D = [doc for doc in docs]
    return D





def batch_stadium(debug: bool):
    """MongoDB 경기장정보 테이블에서 Mysql 경기장정보 테이블로 데이터 insert
    """
    if debug:
        db = SessionLocal()
        
    else:
        db = SessionLocal()
    D = list_stadium(debug)

    

    try:
        for idx, d in enumerate(D, 1):
            query = text('''
                INSERT INTO stadium (
                    stadium_name, stadium_img_url
                    , stadium_url, stadium_en_name
                    , stadium_position, a_seat_quantity
                    , b_seat_quantity, c_seat_quantity
                    , d_seat_quantity, vip_seat_quantity
                ) VALUES (
                    :stadium_name, :stadium_img_url
                    , :stadium_url, :stadium_en_name
                    , :stadium_position, :a_seat_quantity
                    , :b_seat_quantity, :c_seat_quantity
                    , :d_seat_quantity, :vip_seat_quantity
                )
            ''')
            
            db.execute(query, {
                "stadium_name" : d["stadium_ko_name"],
                "stadium_img_url" : d["stadium_img_url"],
                "stadium_url" : d["stadium_url"],
                "stadium_en_name" : d["stadium_en_name"],
                "stadium_position" : d["stadium_position"],
                "a_seat_quantity" : d["a_seat_quantity"],
                "b_seat_quantity" : d["b_seat_quantity"],
                "c_seat_quantity" : d["c_seat_quantity"],
                "d_seat_quantity" : d["d_seat_quantity"],
                "vip_seat_quantity" : d["vip_seat_quantity"]
            })
        
        db.commit()
        print("Data insertion successful.")
    except Exception as e:
        db.rollback()
        print(f"Error Inserting Data: {e}")
    finally:
        db.close()