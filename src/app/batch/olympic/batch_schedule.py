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

from pprint import pprint

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def list_schedule(debug: bool) -> List[str]:
    """MongoDB 종목정보 테이블에서 Mysql 경기장정보 테이블로 데이터 insert

    Returns:
        List[str]: 경기장 리스트
    """
    if debug:
        mongo_db_dev = mongo_client_dev['olympic']
        mongo_col = mongo_db_dev['schedule_stadium_info']
    else:
        mongo_db = mongo_client['olympic']
        mongo_col = mongo_db['schedule_stadium_info']

    docs = mongo_col.find()

    D = [doc for doc in docs]
    return D


def find_sport(debug: bool, sport_en_name: str):
    if debug:
        mongo_db_dev = mongo_client_dev["olympic"]
        mongo_col = mongo_db_dev["sports_info"]
    else:
        mongo_db = mongo_client["olympic"]
        mongo_col = mongo_db["sports_info"]

    query = {
        "sport_en_name" : sport_en_name
    }

    d = mongo_col.find_one(query, no_cursor_timeout=True)

    if d:
        return d["sport_code"]

def find_stadium(debug: bool, stadium: str):
    if debug:
        mongo_db_dev = mongo_client_dev["olympic"]
        mongo_col = mongo_db_dev["stadium_info"]
    else:
        mongo_db = mongo_client["olympic"]
        mongo_col = mongo_db["stadium_info"]

    query = {
        "stadium_ko_name" : stadium
    }

    d = mongo_col.find_one(query, no_cursor_timeout=True)

    if d:
        return d["stadium_no"]

    
    
def update_schedule(debug: bool):
    D = list_schedule(debug)

    save_row = list()
    for d in D:
        sport_code = find_sport(debug, d["sport_en_name"])
        stadium_no = find_stadium(debug, d["stadium"])

        if sport_code is not None:
            d["sport_code"] = sport_code
        else:
            # pprint(d)
            continue
        if stadium_no is not None:
            d["stadium_no"] = stadium_no
        else:
            # pprint(d)
            continue
        save_row.append(d)
    return save_row


    



def batch_schedule(debug: bool):
    """MongoDB 경기장정보 테이블에서 Mysql 경기장정보 테이블로 데이터 insert
    """
    if debug:
        db = SessionLocal()
        
    else:
        db = SessionLocal()

    D = update_schedule(debug)

    try:
        for idx, d in enumerate(D, 1):
            print(f'진행률 {idx}/{len(D)}----------------------------------------')
            query = text('''
                INSERT INTO game (
                    sport_name, country1_name
                    , country2_name, tournament
                    , country, country1_flag
                    , country2_flag, stadium_name
                    , paris_date, paris_time
                    , korea_time, korea_date
                    , sport_code, stadium_no
                ) VALUES (
                    :sport_name, :country1_name
                    , :country2_name, :tournament
                    , :country, :country1_flag
                    , :country2_flag, :stadium_name
                    , :paris_date, :paris_time
                    , :korea_time, :korea_date
                    , :sport_code, :stadium_no
                )
            ''')

            db.execute(query, {
                "sport_name" : d["sport_name"]
                , "country1_name" : d["country1_name"]
                , "country2_name" : d["country2_name"]
                , "tournament" : d["tournament"]
                , "country" : d["country"]
                , "country1_flag" : d["country1_flag"]
                , "country2_flag" : d["country2_flag"]
                , "stadium_name" : d["stadium"]
                , "paris_date" : d["paris_date"]
                , "paris_time" : d["paris_time"]
                , "korea_time" : d["korea_time"]
                , "korea_date" : d["korea_date"]
                , "sport_code" : d["sport_code"]
                , "stadium_no" : d["stadium_no"]
            })
        
        db.commit()
        print("Data insertion successful.")
    except Exception as e:
        db.rollback()
        print(f"Error Inserting Data: {e}")
    finally:
        db.close()