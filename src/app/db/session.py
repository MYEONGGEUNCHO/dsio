"""
Sqlalchemy Database 연결 객체 관리
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import declarative_base
from core.config import settings

conn_str = settings.get_db_uri(
    'MYSQL'
    , **settings.DB_CONNECTION_INFO['MYSQL']    
)

engine = create_engine(
    conn_str
    , pool_pre_ping = False
    , pool_size = settings.DB_POOL_SIZE
    , max_overflow = settings.DB_MAX_OVERFLOW
)

SessionLocal = sessionmaker(
    autocommit=False
    , autoflush=False
    , bind=engine
)

conn_str_dev = settings.get_db_uri(
    'MYSQL_DEV'
    , **settings.DB_CONNECTION_INFO['MYSQL_DEV']    
)

engine_dev = create_engine(
    conn_str_dev
    , pool_pre_ping = False
    , pool_size = settings.DB_POOL_SIZE
    , max_overflow = settings.DB_MAX_OVERFLOW
)

SessionLocal_dev = sessionmaker(
    autocommit=False
    , autoflush=False
    , bind=engine
)