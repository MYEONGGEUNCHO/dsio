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
    
    # DATABASE
    ## 데이터베이스는 MariaDB, MongoDB로 구성
    # DB_TYPE = 'MariaDB' or 'MongoDB'
    DB_URI_TYPE: str = 'MYSQL'
    DB_URI_TEMPLATE: Dict[str, str] = {
        'MYSQL' : 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4',
        # 'MARIA_SOL' : 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4',
        # 'MSSQL_MSG': 'mssql+pymssql://{}:{}@{}:{}/{}?charset=cp949',
        # 'MSSQL': 'mssql+pymssql://{}:{}@{}:{}/{}?charset=cp949',
        # 'MSSQL_BND_MSG': 'mssql+pymssql://{}:{}@{}:{}/{}?charset=cp949',
        # 'MSSQL_BND_MSG_PROD': 'mssql+pymssql://{}:{}@{}:{}/{}?charset=cp949',
    }

    DB_CONNECTION_INFO: Dict[str, Dict[str, str]] = {
        'MYSQL': {
            'user': os.getenv("MYSQL_HOST")
            , 'pwd': os.getenv("MYSQL_PORT")
            , 'host': os.getenv("MYSQL_USER")
            , 'port': os.getenv("MYSQL_PWD")
            , 'database': os.getenv("MYSQL_SCHEMA")
        }
    }

    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = -1

    # COMMON Utils 관련 환경설정
    # DATE_FMT = [
    #     '%Y%m%d',
    #     '%Y-%m-%d',
    #     '%Y/%m/%d'
    # ]

    def get_db_uri(
        self,
        uri_type: str,
        user: str,
        pwd: str,
        host: str,
        port: str,
        database: str
    
    ) -> str:
        """
        대상 db 이름을 입력받아 db 연결을 위한 URI 반환
        
        Returns
        -------
        : str
            대상 DB URI
    
        """
        print(self.DB_URI_TEMPLATE[uri_type].format(
            user,
            quote(pwd),
            host,
            port,
            database
        ))
        return self.DB_URI_TEMPLATE[uri_type].format(
            user,
            quote(pwd),
            host,
            port,
            database
        )
    
    

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