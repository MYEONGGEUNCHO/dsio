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
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def list_sport(debug: bool) -> List[str]:
    """종목정보 테이블에서 영문종목명 리스트 수집

    Returns:
        List[str]: 영문종목명 리스트
    """
    if debug:
        mongo_db_dev = mongo_client_dev['olympic']
        mongo_col = mongo_db_dev['code_info']
    else:
        mongo_db = mongo_client['olympic']
        mongo_col = mongo_db['code_info']

    D = mongo_col.find()

    sport_list = list()
    for d in D:
        sport = d['game_en_name']
        sport_list.append(sport)
    
    return sport_list


    