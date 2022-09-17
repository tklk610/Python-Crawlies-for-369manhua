import requests
import datetime
import time
import random
import os

from io import BytesIO
from PIL import Image
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions


# 设置保存路径
save_dir = r'xxx'
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])

user_agent = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (WindowsNT 10.0; Win64; x64; rv:100.0) Gecko/20100101Firefox/100.0"
    ]

start = datetime.datetime.now()

def get_page_path(url):
    headers_path = {
        "Accept"                    : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding"           : "gzip, deflate, br",
        "Accept-Language"           : "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection"                : "keep-alive",
        # "Cookie"                    : "td_cookie=1374660017;ComicHistoryitem_zh=History=614,637984042562212870,101201,2,0,0,0,37&ViewType=0;MANGABZ_MACHINEKEY=deb97fc6-b460-45e1-b401-d74a6ac5931c;\
        #                               _ga_1SQXP46N58=GS1.1.1662778212.1.1.1662779657.0.0.0;_ga=GA1.1.1637493032.1662778213;firsturl=http % 3A % 2F % 2/Fwww.mangabz.com%2Fm101201%2F;readhistory_time=1-614-101201-2;\
        #                               image_time_cookie=109286|637984038221919904|0,40443|637984038335211502|0,40444|637984038452627191|0,101201| 637984042564044762 | 1;\
        #                               mangabzimgpage=109286|1:1,40443|1:1,40444|1:1,101201|2:1;\
        #                               mangabzcookieenabletest=1;mangabzimgcooke=109286%7C2%2C40443%7C2%2C40444%7C2%2C101201%7C6",
        # "Host"                      : "www.mangabz.com",
        # "Referer"                   : "http://www.mangabz.com/614bz/",
        # "Upgrade-Insecure-Requests" : "1",
        "User-Agent"                : random.choice(user_agent)
    }

    response_path = requests.get(url, headers=headers_path)   # 发送请求,获取响应
    if response_path.status_code == 200:
        print('Path Request success.')

    response_path.encoding = 'utf-8'  # 重新设置编码解决编码问题

    print(response_path.text)
    html_path = etree.HTML(response_path.text)
    # xpath定位提取想要的数据  得到图片链接和名称
    # //从匹配选择的当前节点选择文档中的节点，而不考虑他们的位置
    # @选取属性
    # /是从根节点选取。
    page_path = html_path.xpath('/html/body/div[5]/div[5]/div[2]/div[3]/ul/li/a/@href')
    page_path = ['https://www.369manhua.com' + x for x in page_path]

    page_name = html_path.xpath('/html/body/div[5]/div[5]/div[2]/div[3]/ul/li/a/text()')

    print(page_path)
    print(len(page_path))
    print(page_name)

    for page_index in range(0, len(page_path)) :
        page_url   = page_path[page_index]
        image_name = page_name[page_index]
        image_name = image_name.replace(' ', '')

        get_page_url(page_url, image_name)
        time.sleep(random.randint(5, 20))

        print("下载了一画")


def get_page_url(url, name) :
    headers_page = {
        "Accept"          : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding" : "gzip, deflate, br",
        "Accept-Language" : "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection"      : "keep-alive",
        "User-Agent"      : random.choice(user_agent)
    }

    save_path = save_dir + '/' + str(name)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    bro = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options, options=option)
    bro.get(url)
    response_img = bro.page_source

    html_page = etree.HTML(response_img)
    image_url = list(html_page.xpath('/html/body/div[9]/div[1]/img/@src'))

    for page_num in range(0, len(image_url)) :
        get_image(image_url[page_num], page_num, name, save_path)
        time.sleep(random.randint(5, 20))

    bro.quit()


def get_image(url, num, name, save_path) :
    headers_image = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q = 0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "User-Agent": random.choice(user_agent)
    }

    try:
        image_data = requests.get(url=url, headers=headers_image).content
    except:
        image_data = requests.get(url=url, headers=headers_image, verify=False).content

    if str(url).endswith('.webp') :
        byte_stream = BytesIO(image_data)
        im = Image.open(byte_stream)
        # im.show()
        if im.mode == "RGBA":
            im.load()  # required for png.split()
            background = Image.new("RGB", im.size, (255, 255, 255))
            background.paste(im, mask=im.split()[3])

        im.save(save_path + '/' + str(num+1) + '.png', 'PNG')

    else :
        with open(save_path + '/' + str(num+1) + '.png', 'wb') as fp:
            fp.write(image_data)

    print("Get {} ep {} Picture!!!".format(name, num))

    time.sleep(random.randint(5, 20))


def main():
    # 要请求的url
    url_list = 'https://www.369manhua.com/manhua/zaiyishijiemigongkaihougong/'

    get_page_path(url_list)

    delta = (datetime.datetime.now() - start).total_seconds()
    print(f"抓取所有页图片用时：{delta}s")

if __name__ == '__main__':
    main()