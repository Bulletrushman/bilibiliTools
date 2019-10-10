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

cookielist = [

]

header = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
'Connection': 'keep-alive',
'Cookie': '',
'referer': 'https://www.bilibili.com'
}

#requests = urllib.request.Request(url,headers=header)
#response=urllib.request.urlopen(requests)
class CommentControll():
    def __init__(self):
        self.dr=webdriver.Chrome()
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
        #time.sleep(4)
        #textarea = self.dr.find_element_by_name("msg")
        textarea = self.wait.until(EC.presence_of_element_located((By.NAME,'msg')))
        js4 = "arguments[0].scrollIntoView();"
        self.dr.execute_script(js4, textarea)
        textarea.clear()
        textarea.send_keys('')
        button = self.dr.find_element_by_xpath('//button[@class="comment-submit"]')
        button.click()

    def moniter(self,url):
        self.dr.get(url)
        for each_cookie in cookielist:
            self.dr.add_cookie(each_cookie)
        self.dr.refresh()
        time.sleep(2)
        while True:
            try:
                requests = urllib.request.Request(url, headers=header)
                stat = urllib.request.urlopen(requests)#判断页面是否存在
            except:
                print('还没更新')
            else:
                self.dr.refresh()
                self.comment()
                break
        # nextnumber = dr.find_element_by_xpath('//div[@id="eplist_module"]/div[@class="list-wrapper simple"]/ul/li[@class="ep-item badge"]')
        # nextnumber.click()

if __name__=='__main__':
    url='https://www.bilibili.com/bangumi/play/ep285481'
    comm = CommentControll()
    #comm.testopenandcomment(url=url)
    comm.moniter(url)

