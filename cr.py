# commit use request
import urllib.request
import urllib.parse
import http.cookiejar
import urllib.error
import json
import time
from bs4 import BeautifulSoup
import urllib.request
import requests

cookie = ''


def auto_comment(oid, message, cookie):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Host': 'api.bilibili.com',
        'Origin': 'https://www.bilibili.com',
        # 视频类型在这里修改
        'Referer': 'https://www.bilibili.com/bangumi/play/ep285752',  # 动态时候使用 oid
        # 'Referer': 'https://www.bilibili.com/video/av'+oid+'/?spm_id_from=333.334.home_popularize.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    }

    url = 'https://api.bilibili.com/x/v2/reply/add'
    comment = {
        'oid': oid,  # 70781027
        'type': '1',
        'message': message,
        'plat': '1',
        'jsonp': 'jsonp',
        'csrf': 'e7e3a6578428e434258a4e7d62127212'
    }

    postdata = urllib.parse.urlencode(comment).encode('utf-8')
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    urllib.request.install_opener(opener)
    try:
        request = urllib.request.Request(url, headers=headers, data=postdata)
        response = opener.open(request)
        print(response.reason)

        print('响应描述:' + response.reason)
        print('响应体:' + response.read().decode('UTF-8'))

    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)


if __name__ == '__main__':

    url = 'https://www.bilibili.com/bangumi/play/ep285752'
    while True:
        try:
            stat = urllib.request.urlopen(url)  # 判断页面是否存在
        except:
            print('还没更新')
        else:
            req = requests.get(url)
            html = req.text
            bf = BeautifulSoup(html, 'lxml')
            text = bf.find_all('a', class_='av-link')
            avnumber = text[0].text
            number = avnumber[2:len(avnumber)]
            auto_comment(
                number,
                'ccc',
                ''
            )
            break