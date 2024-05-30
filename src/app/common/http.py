import datetime
import logging
import time
import requests as req

from typing import List, Tuple, Dict, Any, Optional
from ast import Call
from functools import wraps

from typing import Callable, OrderedDict, TypeVar, get_origin, get_type_hints
from typing_extensions import ParamSpec
from xml.dom import minidom

from selenium import webdriver
from selenium.webdriver.common.by import By

_P = ParamSpec("_P")
_R = TypeVar("_R")


def delay(f: Callable[_P, _R]) -> Callable[_P, _R]:
    """함수의 키워드 매개변수에 _delay 변수가 있을시 실행후 _delay 만큼 실행중지"""
    
    @wraps(f)
    def delayed_func(
            *args: _P.args
            , pre_delay: float = 0.0
            , delay: float = 0.5
            , **kwargs: _P.kwargs
        ) -> _R:

        if pre_delay > 0:
            time.sleep(pre_delay)

        result = f(*args, **kwargs)

        if delay > 0:
            time.sleep(delay)

        return result

    return delayed_func

http_get = delay(req.get)
http_post = delay(req.post)
