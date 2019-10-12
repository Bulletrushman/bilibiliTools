from io import BytesIO
from PIL import Image
import base64
import random
import requests 
import json
import os
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
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

#set account here
ACCOUNT = ''
PASSWORD = ''


'''
自动化处理相关模块
'''
# 登录集合类
class LoginCollection():
    def __init__(self):
        self.url = 'https://passport.bilibili.com/login?gourl=https%3A%2F%2Faccount.bilibili.com%2Faccount%2Fbig'
        self.chrome_options = Options()
        # self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(chrome_options=self.chrome_options)
        self.wait = WebDriverWait(self.browser, 20)
        self.email = ACCOUNT
        self.password = PASSWORD

    def __del__(self):
        self.browser.close()


    # 打开网页输入账户
    def open(self):
        self.browser.get(self.url)
        email = self.wait.until(EC.presence_of_element_located((By.ID, 'login-username')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'login-passwd')))
        email.send_keys(self.email)
        password.send_keys(self.password)
    
    # 点击登录按钮
    def login(self):
        submit = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-login')))
        submit.click()
        time.sleep(1)
        print('Login do')
        
    # 对验证码图片的相关处理
    # 下载验证码图片
    # self.save_img('full.jpg', 'geetest_canvas_fullbg')
    # self.save_img('cut.jpg','geetest_canvas_bg')
    def save_img(self, img_name, class_name):
        # img_name 是保存图片的名字，class_name 是需要保存的canvas的className
        getImgJS = 'return document.getElementsByClassName("' + class_name + '")[0].toDataURL("image/png");'
        img = self.browser.execute_script(getImgJS)
        base64_data_img = img[img.find(',') + 1:]
        print("get img")
        image_base = base64.b64decode(base64_data_img)
        file = open(img_name, 'wb')
        file.write(image_base)
        file.close()

    # 判断颜色是否相近
    def is_similar_color(self, x_pixel, y_pixel):
        for i, pixel in enumerate(x_pixel):
            if abs(y_pixel[i] - pixel) > 50:
                return False
        return True

    # 计算移动距离
    def get_offset_distance(self, cut_image, full_image):
        for x in range(cut_image.width):
            for y in range(cut_image.height):
                cpx = cut_image.getpixel((x, y))
                fpx = full_image.getpixel((x, y))
                if not self.is_similar_color(cpx, fpx):
                    img = cut_image.crop((x, y, x + 50, y + 40))
                    # 保存一下计算出来位置图片，看看是不是缺口部分
                    img.save("hole.png")
                    return x

    # 开始移动
    def start_move(self, distance):
        element = self.browser.find_element_by_xpath('//div[@class="geetest_slider_button"]')

        # 这里就是根据移动进行调试，计算出来的位置不是百分百正确的，加上一点偏移
        distance -= element.size.get('width') / 2
        distance += 25

        print(distance)
        # 按下鼠标左键 出现验证失败的情况 在这里调整拖动的随机性
        ActionChains(self.browser).click_and_hold(element).perform()
        time.sleep(0.5)
        while distance > 0:
            if distance > 18:
                span = random.randint(distance-12,distance-6)
            elif distance > 10:
                # 如果距离大于10，就让他移动快一点
                span = random.randint(5, 8)              
            else:
                # 快到缺口了，就移动慢一点
                span = random.randint(2, 3)          
            ActionChains(self.browser).move_by_offset(span, 0).perform()
            distance -= span
            print(distance)
            #time.sleep(random.randint(10, 50) / 100)
            time.sleep(random.randint(10, 15) / 100)
            #time.sleep(0.1)


        ActionChains(self.browser).move_by_offset(distance, 1).perform()
        ActionChains(self.browser).release(on_element=element).perform()

    # 总流程
    def run(self):
        self.open()
        # 调用一次登录 唤出验证码框
        self.login()
        # 下载图片
        self.save_img('full.jpg', 'geetest_canvas_fullbg')
        self.save_img('cut.jpg','geetest_canvas_bg')
        full_image = Image.open('full.jpg')
        cut_image = Image.open('cut.jpg')

        # 根据两个图片计算距离
        distance = self.get_offset_distance(cut_image, full_image)

        # 开始移动
        self.start_move(distance)

        time.sleep(5)
        self.browser.get('https://api.bilibili.com/x/v2/reply/add')
        time.sleep(3)
        #设定10s后读取cookie
        cookies = self.browser.get_cookies()
        jsonCookies = json.loads(json.dumps(cookies))
        result = ''
        for cookie in jsonCookies:
            result = result + cookie["name"] + '=' + cookie["value"] + ";"
        print(result)

        json_str = json.dumps(cookies)
        with open('cookies.json', 'w') as f:
            f.write(json_str)
        print('Downlaod the cookie')
        time.sleep(100)
        return result[0:len(result)-1]
        # 增加对结果的判定
        # try:
        #     WebDriverWait(self.browser, 5, 0.5).until(
        #         EC.presence_of_element_located((By.XPATH, '//div[@class="geetest_slider geetest_error"]')))
        #     print("验证失败")
        #     return
        # except Exception as e:
        #     pass

        # # 判断是否验证成功
        # try:
        #     WebDriverWait(self.browser, 10, 0.5).until(
        #         EC.presence_of_element_located((By.XPATH, '//div[@class="geetest_slider geetest_success"]')))
        # except Exception:
        #     print("again times")
        #     self.run()
        # else:
        #     print("验证成功")

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



# 抓取改视频下评论数和评论者ID   修改这里函数可以实现锁楼
def commit(av_id):
    r = requests.get('https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=1&type=1&oid={}&sort=2&_=1558948726737'.format(av_id))  
    # 这个json地址获取方法：随便找一个评论用户的ID，在网页F12中CTRL+f 搜索 ，可以找到一个地址，复制地址，去掉callback回调部分
    data = json.loads(r.text)
    page_count=(data['data']['page']['count'])//20+1  # 获取总页数
    # pprint.pprint(data['data']['replies'])
    #这个json里不只有用户id ，而且能找到用户评论，楼中楼的用户ID 评论等

    user_list=[] # 保存用户名

    for pg_num in range(1,page_count+1):  # 循环获取所有页面上的用户名，这地方运行速度慢，后续尝试利用多线程加快速度
        # print('go to {} page...'.format(pg_num))
        r=requests.get(
        'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={}&type=1&oid={}&sort=2&_=1558948726737'.format(pg_num,av_id))
        data=json.loads(r.text)
        
        for i in data['data']['replies']:  # 每页有20层楼，遍历这20层楼获取ID
            user_list.append(i['member']['uname'])

    # index = 1;
    # for i in user_list:
    #     print(str(index) + '楼:  ' + i)
    #     index = index + 1

    print('当前评论数 ',len(user_list),'去除重复昵称后评论数 ',len(set(user_list)))




'''
请求处理相关模块
'''

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


# 现在参数在这里设置
ssID = '26777'
type_tig = 4
nums = 0
commit_str = 'Come to see'
# csrf = '7e198f779af88aca590f26cd2f211f56'
csrf = '7dbfc12d33219e3deba41427209ff470'
times= 3


if __name__ == '__main__': 
    # 预准备内容 
    Login = LoginCollection()
    cookie = Login.run()
    time.sleep(5)
    # print('-----Preloading completed-----')
    
    
    main_run(ssID, type_tig, nums, commit_str, cookie, csrf, times)