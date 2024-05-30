import os
import logging
from dotenv import load_dotenv
from binascii import a2b_base64
from typing import Any, Optional, Dict, List, Tuple, TypeVar
from pydantic_settings import BaseSettings
from urllib.parse import quote
from urllib.parse import quote_plus as urlquote


SRC_DIR = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))))
LOG_DIR = os.path.join(SRC_DIR, 'logs')

class Settings(BaseSettings):
    load_dotenv()
    

    DEBUG: bool = True

    APP_NAME: str = 'DSIO'
    # 빈문자열('')이 아니라면 로깅 파일 이름에 추가
    APP_NAME_OPTION: str = ''
    
    
    

    ### mongodb config 운영
    MONGO_HOST: str = os.getenv("MONGO_HOST")
    MONGO_PORT: int = os.getenv("MONGO_PORT")
    MONGO_USER: str = os.getenv("MONGO_USER")
    MONGO_PWD: str = os.getenv("MONGO_PWD")

    ### mongodb config 개발
    MONGO_HOST_DEV: str = os.getenv("MONGO_HOST_DEV")
    MONGO_PORT_DEV: int = os.getenv("MONGO_PORT_DEV")
    MONGO_USER_DEV: str = os.getenv("MONGO_USER_DEV")
    MONGO_PWD_DEV: str = os.getenv("MONGO_PWD_DEV")


    class Config:
        # secrets_dir = SETCRETS_DIR

        # 입력된 환경변수중 Settings 에 포함될 변수의 접두사
        # 설정시 secrets는 포함되지 않는다.
        env_prefix = 'DSIO_'
    
settings = Settings()