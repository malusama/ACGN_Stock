import requests
from pyquery import PyQuery
import gevent
import logging
import functools
import redis


logger = logging.getLogger("test")
redis_client = redis.Redis(host='localhost', port=6379,
                           db=1, decode_responses=True)
BTSO_URL = 'https://btso.pw/search/'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) ' \
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
Accept_Language = 'zh-CN,zh;q=0.9,zh-TW;q=0.8,ja;q=0.7'
REQUEST_CACHE_TIMEOUT = 60 * 60 * 24  # 1 days


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
        session.headers['Accept-Language'] = Accept_Language
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
        logger.warning('Get web page {} error'.format(
            url))


def btsoSearch(keywords):
    html = pq(get_web_page("{}{}".format(BTSO_URL, keywords)))
    link = [i.attr("href") for i in html(".data-list a").items()]
    magnet = []
    for i in link[0:5]:
        info = {}
        html = pq(get_web_page(i))
        info['magnet'] = html("#magnetLink").text()
        info['name'] = html("h3").text()
        info['ContentSize'] = html(".data-list .col-md-10").eq(2).text()
        info['ConvertOn'] = html(".data-list .col-md-10").eq(3).text()

        magnet.append(info)

    return magnet
