import time
from io import BytesIO

from PIL import Image

import base64
import random

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#set account here
ACCOUNT = '123'
PASSWORD = '123'

class LoginCollection():
    def __init__(self):
        self.url = 'https://passport.bilibili.com/login?gourl=https%3A%2F%2Faccount.bilibili.com%2Faccount%2Fbig'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.email = ACCOUNT
        self.password = PASSWORD

    def __del__(self):
        self.browser.close()


    #打开网页输入账户
    def open(self):
        self.browser.get(self.url)
        email = self.wait.until(EC.presence_of_element_located((By.ID, 'login-username')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'login-passwd')))
        email.send_keys(self.email)
        password.send_keys(self.password)
    
    #点击登录按钮
    def login(self):
        submit = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-login')))
        submit.click()
        time.sleep(1)
        print('Login do')
        
    #对验证码图片的相关处理
    #下载验证码图片
    #self.save_img('full.jpg', 'geetest_canvas_fullbg')
    #self.save_img('cut.jpg','geetest_canvas_bg')
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

        # 按下鼠标左键
        ActionChains(self.browser).click_and_hold(element).perform()
        time.sleep(0.5)
        while distance > 0:
            if distance > 10:
                # 如果距离大于10，就让他移动快一点
                span = random.randint(5, 8)
            else:
                # 快到缺口了，就移动慢一点
                span = random.randint(2, 3)
            ActionChains(self.browser).move_by_offset(span, 0).perform()
            distance -= span
            time.sleep(random.randint(10, 50) / 100)

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

if __name__ == '__main__':
    login = LoginCollection()
    login.run()
    time.sleep(100)
