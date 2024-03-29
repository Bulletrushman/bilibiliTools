# commit use request
import urllib.request
import urllib.parse
import http.cookiejar
import urllib.error
import json
import time
from bs4 import BeautifulSoup
import urllib.request
from urllib import request
from http import cookiejar
import requests
import datetime



def auto_comment(oid, message, cookie, csrf):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Host': 'api.bilibili.com',
        'Origin': 'https://www.bilibili.com',
        # 视频类型在这里修改
        'Referer': 'https://www.bilibili.com/bangumi/play/ep' + str(oid),  # 动态时候使用 oid
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
        'csrf': csrf  # 本机重置
    }

    postdata = urllib.parse.urlencode(comment).encode('utf-8')
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    urllib.request.install_opener(opener)
    try:
        request = urllib.request.Request(url, headers=headers, data=postdata)
        response = opener.open(request)
        #print(response.reason)

        print(time_out() + 'Response code:' + response.reason)
        print(time_out() + 'Response text:' + response.read().decode('UTF-8'))

    except urllib.error.URLError as e:
        # if hasattr(e,'code'):
        #     print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)

# 通过接口快速获得AID
# SSID SSXXXXX
# 国番 type传入4
# 日番 type传入1
# 返回AID列表
def auto_getAid(ssID, typeID):
    url = 'https://api.bilibili.com/pgc/web/season/section'
    buildUrl = url + '?' + 'season_id=' + str(ssID) + '&' + 'season_type=' + str(typeID)
    # 主机拒绝的容错
    while True:
        try:
            result = requests.get(buildUrl)
        except:
            print(time_out() + 'Network error try again...')
            time.sleep(0.1)
        else:
            break
    result = requests.get(buildUrl)
    # 处理json数据
    data = json.loads(result.text)
    arr = []
    try:
        for i in data["result"]["main_section"]["episodes"]:
            arr.append(i["aid"])
    except:
        print(time_out() + 'The video has not been released yet.')

    #print(arr)
    return arr
    
# 通过番剧集数判定是否更新
# 传入参数 当前已有集数 从接口获取的ID数组
def is_update(oldIndex, arr):
    if len(arr) <= oldIndex:
        print(time_out() + 'The video has not been updated yet.')
        return False
    else:
        return True

#SS开头ID 番剧类型(Ch:1  Jp:4) 当前已有集数 评论内容 登录cookie 本机csrf 容错次数
#注意设置本机csrf
def main_run(ssID, type_tig, nums, commit_str, cookie, csrf, times):
    while True:
        arr = auto_getAid(ssID, type_tig)
        if is_update(nums, arr):
            for i in range(0, times):
                auto_comment(arr[len(arr)-1], commit_str, cookie, csrf)
                i = i + 1
                time.sleep(0.1)  
            break
        else:
            arr = auto_getAid(ssID, type_tig)

def time_out():
    return 'Log：' + time.strftime('%H:%M:%S',time.localtime(time.time())) + ' '

def read_cookie_fromjson():
    with open('cookies.json', 'r', encoding='utf-8') as f:
        listCookies = json.loads(f.read())
    result = ''
    for cookie in listCookies:
        result = result + cookie["name"] + '=' + cookie["value"] + ";"
    # 去除尾部的多余符号
    result = result[0:len(result)-1]
    print(result)
    return result



#param
ssID = '26777'
type_tig = 4
nums = 0
commit_str = 'Come to see'
# csrf = '7e198f779af88aca590f26cd2f211f56'
csrf = '7dbfc12d33219e3deba41427209ff470'
times= 3

if __name__ == '__main__':
    print('-----Preloading completed-----')
    
    main_run(ssID, type_tig, nums, commit_str, read_cookie_fromjson(), csrf, times)
    
    
