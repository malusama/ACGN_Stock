import requests
from pyquery import PyQuery
import gevent
import logging
import functools
import redis
from tasks import worker


redis_client = redis.Redis(host='localhost', port=6379,
                           db=1, decode_responses=True)

DMM_URL = 'http://www.dmm.co.jp/digital/anime/-/list/=/sort=ranking/'
logger = logging.getLogger("test")
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) ' \
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'

REQUEST_CACHE_TIMEOUT = 30 * 60 * 60 * 24  # 30 days
proxies = { "http": "socks5://127.0.0.1:10010"}


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
            resp = session.get(url, timeout=timeout, proxies=proxies)
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
    # session = models.DBSession()
    for i in range(1,2):
        html = pq(get_web_page("{}page={}/".format(DMM_URL, i)))
        for i in html("#list li .tmb a").items():
            # print(i.attr("href").split()[0])
            worker.delay(i.attr("href"))


if __name__ == '__main__':
    get_anime_link()