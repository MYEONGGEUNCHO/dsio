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
                'stadium': d['stadium']
            }
        })
    

