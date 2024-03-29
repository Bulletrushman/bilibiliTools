import urllib.request
import time
from selenium import  webdriver
from bs4 import BeautifulSoup
import gzip
from io import StringIO
from io import BytesIO
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


# 账户的cookie信息在这里修改
cookielist = [
{'domain': '.bilibili.com','path': '/', 'httpOnly': False, 'name': 'DedeUserID','secure': False, 'value': ''},
{'domain': '.bilibili.com','path': '/', 'httpOnly': False, 'name': 'DedeUserID__ckMd5','secure': False, 'value': ''},
{'domain': '.bilibili.com','path': '/', 'httpOnly': False, 'name': 'LIVE_BUVID','secure': False, 'value': ''},
{'domain': '.bilibili.com','path': '/', 'httpOnly': False, 'name': 'SESSDATA','secure': False, 'value': ''},
{'domain': '.bilibili.com','path': '/', 'httpOnly': False, 'name': '_uuid','secure': False, 'value': ''},
{'domain': '.bilibili.com','path': '/', 'httpOnly': False, 'name': 'bili_jct','secure': False, 'value': ''},
{'domain': '.bilibili.com','path': '/', 'httpOnly': False, 'name': 'buvid3','secure': False, 'value': ''},
{'domain': '.bilibili.com','path': '/', 'httpOnly': False, 'name': 'sid','secure': False, 'value': ''},
]

# 请求头可以不需要改动
header = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
'Connection': 'keep-alive',
'Cookie': '',
'referer': 'https://www.bilibili.com'
}

#requests = urllib.request.Request(url,headers=header)
#response=urllib.request.urlopen(requests)
class CommentControll():
    def __init__(self):
        self.chrome_options = Options()
        #self.chrome_options.add_argument('--headless')
        #self.chrome_options.add_argument('--disable-gpu')
        self.dr=webdriver.Chrome(chrome_options=self.chrome_options)
        self.wait = WebDriverWait(self.dr,20)

    def testopenandcomment(self,url):#评论测试用
        self.dr.get(url)
        for each_cookie in cookielist:
            self.dr.add_cookie(each_cookie)
        self.dr.refresh()
        time.sleep(1)
        js = "var action=document.documentElement.scrollTop=10000" #刷新出评论元素
        self.dr.execute_script(js)
        time.sleep(2)
        textarea = self.dr.find_element_by_name("msg")
        js4 = "arguments[0].scrollIntoView();"
        self.dr.execute_script(js4,textarea)
        textarea.clear()
        textarea.send_keys('')
        button = self.dr.find_element_by_xpath('//button[@class="comment-submit"]')
        button.click()

    def comment(self):
        js = "var action=document.documentElement.scrollTop=10000"  # 刷新出评论元素
        self.dr.execute_script(js)
        textarea = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'ipt-txt')))
        js4 = "arguments[0].scrollIntoView();"
        self.dr.execute_script(js4, textarea)
        textarea.clear()
        # 评论的内容在这里修改
        textarea.send_keys('先评后看')
        button = self.dr.find_element_by_xpath('//button[@class="comment-submit"]')
        button.click()
        print('finish comment')

    def moniter(self,url):
        self.dr.get(url)
        for each_cookie in cookielist:
            self.dr.add_cookie(each_cookie)
        self.dr.refresh()
        time.sleep(2)
        requests = urllib.request.Request(url, headers=header)
        while True:
            try:
                stat = urllib.request.urlopen(requests)#判断页面是否存在
            except:
                print('番剧还没更新')
            else:
                self.dr.refresh()
                self.comment()
                break
        # nextnumber = dr.find_element_by_xpath('//div[@id="eplist_module"]/div[@class="list-wrapper simple"]/ul/li[@class="ep-item badge"]')
        # nextnumber.click()

if __name__=='__main__':
    # 番剧的地址在这里修改 
    url='https://www.bilibili.com/bangumi/play/ep285753'
    comm = CommentControll()
    #comm.testopenandcomment(url=url)
    comm.moniter(url)
    time.sleep(100)

