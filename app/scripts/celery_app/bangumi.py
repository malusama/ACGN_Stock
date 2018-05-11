import requests
from pyquery import PyQuery
import gevent
import logging
import functools
import redis
from celery import Celery
import datetime

import sys

sys.path.append('../../')
from models import (
    Stock,
    Stock_Tag,
    base
)

app = Celery('tasks', broker='redis://localhost:6379/3')
redis_client = redis.Redis(host='localhost', port=6379,
                           db=1, decode_responses=True)

BANGUMI_URL = 'http://bangumi.tv/anime/browser/?sort=date&page='
DMM_URL = 'http://www.dmm.co.jp/digital/anime/-/list/=/sort=ranking/'
logger = logging.getLogger("test")
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko)' \
             ' Chrome/61.0.3163.100 Safari/537.36'

REQUEST_CACHE_TIMEOUT = 30 * 60 * 60 * 24  # 30 days
proxies = {"http": "socks5://127.0.0.1:10010"}


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
    for i in range(1, 2):
        html = pq(get_web_page("{}{}/".format(BANGUMI_URL, i)))
        for i in html("#browserItemList > li").items():
            # print("http://bangumi.tv{}".format(i("a").attr("href")))
            worker("http://bangumi.tv{}".format(i("a").attr("href")))
            break


@app.task
def worker(url):
    # print(url)
    # print(get_web_page('http://pv.sohu.com/cityjson?ie=utf-8'))
    html = pq(get_web_page(url))
    works_name = html("h1 > a").text()
    release_time = html("#infobox > li") # .eq(3).text().split(':')[1]
    if release_time.eq(3).text().split(":")[0] == "上映年度":
        release_time = release_time.eq(3).text().split(":")[1]
    elif release_time.eq(2).text().split(":")[0] == "上映年度":
        release_time = release_time.eq(2).text().split(":")[1]
    else:
        release_time = "1980年1月1日"
        
    year = int(release_time.split("年")[0])
    month = int(release_time.split("年")[1].split("月")[0])
    day = int(release_time.split("年")[1].split("月")[1].split("日")[0])
    # length_time = html(".mg-b20 tr").eq(3)("td").eq(1).text()
    # works_series = html(".mg-b20 tr").eq(4)("td").eq(1).text()
    company = html("#infobox > li").eq(1).text().split(':')[1]
    # factory = html("#infobox > li").eq(1).text()
    category = html(".inner > a > span").text().split()
    cover = html(".cover")
    if cover:
        cover = "https:{}".format(cover("a").attr('href'))
    else:
        cover = "https://malu-picture.oss-cn-beijing.aliyuncs.com/18-5-11/3774354.jpg"
    # Introduction = html(".lh4").text()
    # Screenshots = ["https://{}".format(i.attr("src").split("://")[1])
    #                for i in html("#sample-image-block img").items()]
    # try:
    #     year = int(release_time[0])
    #     month = int(release_time[1])
    #     day = int(release_time[2])
    # except ValueError:
    #     day = int(release_time[2].split(' ')[0])
    print("作品名：{},\n发布时间:{}, \n公司：{}, \ntag:{}, \ncover:{}".format(
            works_name,
            release_time,
            # length_time,
            # works_series,
            company,
            # factory,
            category,
            cover
            # Introduction,
            # Screenshots
        ))
    session = base.DBSession()

    if session.query(Stock).filter(Stock.name == works_name).first():
        print("已经存在")
    else:
        tag = []
        for i in category:
            if session.query(Stock_Tag).filter(
                            Stock_Tag.tag == i).one_or_none() is None:
                sub = Stock_Tag(tag=i)
                session.add(sub)
                session.commit()
            tag.append(session.query(Stock_Tag).filter(
                Stock_Tag.tag == i).first().id)


        sub = Stock(name=works_name,
                    # introduction=Introduction,
                    cover=cover,
                    release_time=datetime.datetime(year, month, day),
                    # length_time=length_time,
                    # works_series=works_series,
                    company=company,
                    # factory=factory,
                    category=",".join(str(i) for i in tag),
                    # screenshots=",".join(i for i in Screenshots)
                    )
        session.add(sub)
        session.commit()
        print("插入成功")


if __name__ == '__main__':
    # worker('http://bangumi.tv/subject/128131')
    get_anime_link()