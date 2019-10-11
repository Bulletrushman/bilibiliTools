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
import datetime
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# 预加载内容
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)


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
        'Referer': 'https://www.bilibili.com/bangumi/play/ep285799',  # 动态时候使用 oid
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
        'csrf': '39da25dd3969010c6c3b3fedeb0abf58'  # 本机重置
    }

    postdata = urllib.parse.urlencode(comment).encode('utf-8')
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    urllib.request.install_opener(opener)
    try:
        request = urllib.request.Request(url, headers=headers, data=postdata)
        response = opener.open(request)
        #print(response.reason)

        print('响应描述:' + response.reason)
        print('响应体:' + response.read().decode('UTF-8'))

    except urllib.error.URLError as e:
        # if hasattr(e,'code'):
        #     print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)

# 暂时使用自动化的库来处理第一集的AVID
# 需要容错这一块ID的爬取
def getUrlId(url):
    # req = requests.get(url)
    # html = req.text
    driver.get(url)
    html = driver.page_source
    bf = BeautifulSoup(html, 'lxml')
    text = bf.find_all('a', class_='av-link')
    avnumber = text[0].text
    number = avnumber[2:len(avnumber)]
    return number

if __name__ == '__main__':
    print('预加载完毕')
    url = 'https://www.bilibili.com/bangumi/play/ep285799'
    
    # url = 'https://www.bilibili.com/bangumi/play/ep285752' #test
    oldId = '69061916'
    while True:
        try:
            stat = urllib.request.urlopen(url)  # 判断页面是否存在
            # while(True):
            #     print(getUrlId(url))
            #     if(getUrlId(url) != oldId):
            #         break
            #     time.sleep(1)
        except:
            x = 1
            # print(str(datetime.datetime.now()) + ' 当前链接番剧内容未更新...')
            # time.sleep(0.5) #循环判定链接的时候 频率调整
        else:
            number = getUrlId(url)
            auto_comment(
                number,
                '来了来了我来了',
                ''
            )
            #快速补发
            auto_comment(
                number,
                '来了来了我来了',
                ''
            )
            #快速补发
            auto_comment(
                number,
                '来了来了我来了',
                ''
            )
            
            break
