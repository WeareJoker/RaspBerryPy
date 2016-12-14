from analysis.database import Session

from analysis.utility import http_request_filter
from .model import Kakao

session = Session()


@http_request_filter('(th-)?p.talk.kakao.co.kr')
def handler(req):
    session.add(Kakao(req.url))
    session.commit()
