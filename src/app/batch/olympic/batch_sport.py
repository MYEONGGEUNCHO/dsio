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

def list_sport(debug: bool) -> List[str]:
    """MongoDB 종목정보 테이블에서 Mysql종목정보 테이블로 데이터 insert

    Returns:
        List[str]: 종목 리스트
    """
    if debug:
        mongo_db_dev = mongo_client_dev['olympic']
        mongo_col = mongo_db_dev['sports_info']
    else:
        mongo_db = mongo_client['olympic']
        mongo_col = mongo_db['sports_info']

    docs = mongo_col.find()

    D = [doc for doc in docs]
    return D





def batch_sport(debug: bool):
    """MongoDB 종목정보 테이블에서 Mysql종목정보 테이블로 데이터 insert
    """
    if debug:
        db = SessionLocal()
        
    else:
        db = SessionLocal()
    D = list_sport(debug)

    

    try:
        for d in D:
            query = text('''
                INSERT INTO sport (
                    sport_code, sport_name, 
                    sport_pictogram, title_image,
                    link, sport_info, 
                    sport_rule, sport_history
                ) VALUES (
                    :sport_code, :sport_name,
                    :sport_pictogram, :title_image,
                    :link, :sport_info,
                    :sport_rule, :sport_history
                )
            ''')
            
            db.execute(query, {
                'sport_code': d['sport_code'],
                'sport_name': d['sport_name'],
                'sport_pictogram': d['sport_pictogram'],
                'title_image': d['title_image'],
                'link': d['link'],
                'sport_info': d['sport_info'],
                'sport_rule': d['sport_rule'],
                'sport_history': d['sport_history']
            })
        
        db.commit()
        print("Data insertion successful.")
    except Exception as e:
        db.rollback()
        print(f"Error Inserting Data: {e}")
    finally:
        db.close()


        

