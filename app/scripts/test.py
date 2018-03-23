import requests
from pyquery import PyQuery
import gevent
import logging
import functools
import redis
import sys
sys.path.append('../')
from models import (
    models
)

redis_client = redis.Redis(host='localhost', port=6379,
                           db=1, decode_responses=True)
BANGUMI_URL = 'http://bangumi.tv'
logger = logging.getLogger("test")
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) ' \
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
REQUEST_CACHE_TIMEOUT = 30 * 60 * 60 * 24  # 30 days


def pq(content):
    if content:
        return PyQuery(content)


def retry(times=3):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.exception("retry {} times exception.".format(i), e)
                    gevent.sleep(3)
                else:
                    break
        return wrapper
    return deco


def get_web_page(url, timeout=15):
    content = redis_client.get(url)
    if content:
        return content
    with requests.Session() as session:
        session.headers['User-Agent'] = USER_AGENT
        try:
            resp = session.get(url, timeout=timeout)
            if resp.status_code == 200:
                logger.warning('missing cache for url: {}'.format(url))
                content = resp.content
                redis_client.setex(url, content, REQUEST_CACHE_TIMEOUT)
                web_page = content.decode('utf8')
                return web_page
        except requests.exceptions.ConnectionError:
            # NOTE: do not raise and not retry
            pass
        logger.warning('Get web page {} error'.format(url))


def get_anime_link():
    anime_link = []
    session = models.DBSession()
    for i in range(20):
        html = pq(get_web_page("{}/{}?page={}".format(
            BANGUMI_URL, "anime/browser", i)))
        for iter in html("#browserItemList li h3 a").items():
            anime_link.append("{}{}".format(BANGUMI_URL, iter.attr("href")))
            # print("{}{}".format(BANGUMI_URL, iter.attr("href")))

    for iter in anime_link:
        html = pq(get_web_page(iter))
        if html(".infobox img").attr("src"):
            cover = '{}{}'.format(
                'http://', html(".infobox img").attr("src").split('//', 1)[1])
        else:
            cover = ""
        anime_name = html(".nameSingle a").text()
        Introduction = html("#subject_summary").text()
        if session.query(models.Stock).filter(
                models.Stock.name == anime_name).first():
            continue
        else:
            sub = models.Stock(
                name=anime_name, introduction=Introduction, cover=cover)
            session.add(sub)
            session.commit()


if __name__ == '__main__':
    get_anime_link()
