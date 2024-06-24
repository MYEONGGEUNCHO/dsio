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
        mongo_col = mongo_db_dev['schedule_stadium_join']
    else:
        mongo_db = mongo_client['olympic']
        mongo_col = mongo_db['schedule_stadium_join']

    docs = mongo_col.find()

    D = [doc for doc in docs]
    return D

def batch_update_schedule(debug: bool):
    """MongoDB 경기장정보 테이블에서 Mysql 경기장정보 테이블로 데이터 insert
    """
    if debug:
        db = SessionLocal()
        
    else:
        db = SessionLocal()

    D = list_schedule(debug)

    try:
        for idx, d in enumerate(D, 1):
            print(f'진행률 {idx}/{len(D)}----------------------------------------')
            query = text('''
                INSERT INTO game (
                    UPDATE game SET
                    country1_name = :country1_name,
                    country2_name = :country2_name,
                    tournament = :tournament,
                    country = :country,
                    country1_flag = :country1_flag,
                    country2_flag = :country2_flag,
                    WHERE game_id = :game_id
                )
            ''')

            db.execute(query, {
                "country1_name" : d["country1_name"]
                , "country2_name" : d["country2_name"]
                , "tournament" : d["tournament"]
                , "country" : d["country"]
                , "country1_flag" : d["country1_flag"]
                , "country2_flag" : d["country2_flag"]
                , "game_id" : d["game_id"]
            })
        
        db.commit()
        print("Data is updated .")
    except Exception as e:
        db.rollback()
        print(f"Error Inserting Data: {e}")
    finally:
        db.close()