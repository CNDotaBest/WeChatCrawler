# -*- coding: UTF-8 -*-
import requests
import time
import pandas as pd
import math
import random

user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Mobile Safari/537.36",
]

# 目标url
url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
cookie = "appmsglist_action_3938608885=card; appmsglist_action_3935619326=card; RK=dtHkk/fYaX; ptcz=19c2f43d5a09cb8a05d14c61e4085c44714fad1071c125461284666a60a97ef8; ua_id=euXJRprud7Td8gB9AAAAAHru4dL-IXNzwepHGzvzXAo=; wxuin=99170031338042; pgv_pvid=7665033420; qq_domain_video_guid_verify=dc05d329a5e3b6a6; _qimei_uuid42=17b0513202d1001c5156e83b40666491e4572e0a09; _qimei_fingerprint=9f4553ac0c1bde71f90a2b70947ea519; _qimei_q36=; _qimei_h38=98e595e55156e83b406664910300000ca17b05; mm_lang=zh_CN; ts_uid=2444490576; noticeLoginFlag=1; rewardsn=; wxtokenkey=777; cert=49b8mszOGixPO33oZdv6uDISXBg3D5u1; sig=h0154a50c1df9586793c7fad43b04e5f74eced8422033e0c0c9add69548a66bd59965b9c9cc405a3d70; uuid=d2e1b79ef37ddec9b882d328aeabc14d; rand_info=CAESII6wO2FqgO9tLc8x1L/Py5Bx/kdKJAvpJV6i2suKcnD3; slave_bizuin=3935619326; data_bizuin=3935619326; bizuin=3935619326; data_ticket=qClm9TexaL2ZN0xpX8pOEzm5EEDnBKCobt8M8189en4LyHufcQSGU0jstBbrI1Si; slave_sid=UWwwSmRYckViNXNVUUxadmhUaFAyWVFHSXg2cEdmMFBZS1ZEYnpwbkp0Yl9GM1loWm1tSTcycU16Mm9VeG1HeFpLTGZuX0pYQnlUb2p3V2cwWEZSUVZSSV9BWER0V1c0VmlsaF9Tc2V0TDJfQlY2bVMyWU1ZOXV5R2hBenE0UUpWc3BRQ0VsS09IdmJNaTlJ; slave_user=gh_573b7fb7b5b3; xid=981355d99614165c3ec2cc54317ad8f1; _clck=3935619326|1|fhr|0; _clsk=1ssbx15|1703208122742|1|1|mp.weixin.qq.com/weheat-agent/payload/record"

# 使用Cookie，跳过登陆操作
data = {
    "token": "913700746",
    "lang": "zh_CN",
    "f": "json",
    "ajax": "1",
    "action": "list_ex",
    "begin": "0",
    "count": "5",
    "query": "",
    "fakeid": "MjM5MzI5NTU3MQ==",
    "type": "9",
}
headers = {
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Mobile Safari/537.36",

    }
content_json = requests.get(url, headers=headers, params=data).json()
count = int(content_json["app_msg_cnt"])
print(count)
page = int(math.ceil(count / 5))
print(page)
content_list = []
# 功能：爬取IP存入ip_list列表

for i in range(page):
    data["begin"] = i * 5
    user_agent = random.choice(user_agent_list)
    headers = {
        "Cookie": cookie,
        "User-Agent": user_agent,

    }
    ip_headers = {
        'User-Agent': user_agent
    }
    # 使用get方法进行提交
    content_json = requests.get(url, headers=headers, params=data).json()
    # 返回了一个json，里面是每一页的数据
    for item in content_json["app_msg_list"]:
        # 提取每页文章的标题及对应的url
        items = []
        items.append(item["title"])
        items.append(item["link"])
        t = time.localtime(item["create_time"])
        items.append(time.strftime("%Y-%m-%d %H:%M:%S", t))
        content_list.append(items)
    print(i)
    # if (i > 0) and (i % 10 == 0):
    if i == 2:
        name = ['title', 'link', 'create_time']
        test = pd.DataFrame(columns=name, data=content_list)
        test.to_csv("url.csv", mode='a', encoding='utf-8')
        print("第" + str(i) + "次保存成功")
        content_list = []
        time.sleep(random.randint(60,90))
    else:
        time.sleep(random.randint(15,25))

name = ['title', 'link', 'create_time']
test = pd.DataFrame(columns=name, data=content_list)
test.to_csv("url.csv", mode='a', encoding='utf-8')
print("最后一次保存成功")