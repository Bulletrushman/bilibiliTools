import requests 
import json
import random
import os

#av_id=input('please input av_id   ')  # 视频号
av_id = 26605386

r=requests.get(
    'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=1&type=1&oid={}&sort=2&_=1558948726737'.format(26605386))  
    # 这个json地址获取方法：随便找一个评论用户的ID，在网页F12中CTRL+f 搜索 ，可以找到一个地址，复制地址，去掉callback回调部分
data=json.loads(r.text)
page_count=(data['data']['page']['count'])//20+1  # 获取总页数，本来想用xpath直接爬到总页数，后来发现json里有个count总楼层数统计，所以可以计算出总页数
# pprint.pprint(data['data']['replies'])
# 这个json里不只有用户id ，而且能找到用户评论，楼中楼的用户ID 评论等

user_list=[] # 保存用户名

for pg_num in range(1,page_count+1):  # 循环获取所有页面上的用户名，这地方运行速度慢，后续尝试利用多线程加快速度
    print('go to {} page...'.format(pg_num))
    r=requests.get(
    'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={}&type=1&oid={}&sort=2&_=1558948726737'.format(pg_num,av_id))
    data=json.loads(r.text)
    
    for i in data['data']['replies']:  # 每页有20层楼，遍历这20层楼获取ID
    #     pprint.pprint(i['member']['uname'])
        user_list.append(i['member']['uname'])

index = 1;
for i in user_list:
    print(str(index) + '楼:  ' + i)
    index = index + 1


# 所有评论用户的id

# 抽奖模块
print('\n\n\n\n')
print('当前评论数 ',len(user_list),'去除重复昵称后评论数 ',len(set(user_list)))  # 去重 ，防止多次回复拉高中奖几率

luck_user=random.choice(user_list)
print('Lucker user ', luck_user)
os.system("pause") # 如果是直接双击运行该文件，那么运行完成后cmd窗口会直接关闭，加入这一条便于查看输出结果，当然也可以把运行结果写入txt文件内
