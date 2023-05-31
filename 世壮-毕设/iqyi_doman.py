import json
import socket

import pymysql
import requests

if __name__ == '__main__':
    conn = pymysql.connect(host='localhost',
                           user='root',
                           passwd='root',
                           port=3306,
                           db='video',
                           charset='utf8')

    cs = conn.cursor()


    def date(d_id, latestOrder):  # 获取动漫集数

        user = []

        urld = "https://pcw-api.iqiyi.com/albums/album/avlistinfo?aid={}&page={}&size=200&callback="

        x = 0
        for a in range(1, (latestOrder // 200) + 2):
            url = urld.format(d_id, a)
            req = requests.get(url, headers=headers, proxies=proxies).content.decode()
            strList = json.loads(req)
            strList = strList["data"]["epsodelist"]
            for str in strList:
                name = str["name"]
                url = str["playUrl"]
                x = x + 1
                user.append((name, x, url, d_id))

        # transfer(a_id=d_id, p_title=name, a_movieurls=url, p_id=x)  # 输入url 集数
        transfer(user)


    def transfer(user):  # 写入动漫集数

        # usersvalues = []
        # for num in range(1, 20000):
        #     usersvalues.append(('在list中的每一个元素必须是元组', num))

        # usersvalues.append((p_title, p_id, a_movieurls, a_id))
        # print(usersvalues)

        # , ('航海王 第399集', 399, 'http://www.iqiyi.com/v_19rrok8qcs.html', 202861101)
        # , ('在list中的每一个元素必须是元组', 19996)
        # cs.executemany('insert into anime_pending(p_title,p_id,a_movieurls,a_id) values(%s,%s,%s,%s)', user) #插入数据
        # sql = "insert ignore into anime_pending(p_title,p_id,a_movieurls,a_id) values(%s,%s,%s,%s)"  # 插入数据时跳过重复数据
        sql = "insert ignore into anime_pending(p_title,p_id,a_movieurls,a_id) values(%s,%s,%s,%s)"  # 插入时更新数据
        cs.executemany(sql, user)
        conn.commit()
        try:
            print("写入成功")
        except:
            conn.close()
            cs.close()
            print("写入失败")


    def Anime(a_id, name, description, latestOrder, period, score, categories, imageUrl):

        param = (a_id, name, score, latestOrder, categories, period, imageUrl, description)

        # sql = "insert ignore into anime values(%s,%s,%s,%s,%s,%s,%s,%s)"  # 插入数据时跳过重复数据

        sql = "insert ignore into anime values (%s,%s,%s,%s,%s,%s,%s,%s)"  # 插入时更新数据

        cs.execute(sql, param)

        conn.commit()
        try:
            print("动漫数据写入成功")

            date(d_id=a_id, latestOrder=latestOrder)  # 输入动漫id
        except:
            print("动漫数据写入失败")


    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51"
    }

    urld = "https://pcw-api.iqiyi.com/search/recommend/list?channel_id=4&data_type=1&mode=24&page_id={}&ret_num=20&session=811d9805b18144adc0246c4fba23e952"
    # num = int(input("输入所爬页数-一页20条数据："))
    proxy = '183.239.68.61:4780'
    proxies = {"https": proxy,
               "http": proxy
               }


    for a in range(1, 9 + 1):
        url = urld.format(a)
        req = requests.get(url, proxies=proxies).content.decode()
        strList = json.loads(req)

        strList = strList["data"]["list"]
        for str in strList:
            a_id = str["albumId"]  # 动漫id
            name = str["name"]  # 动漫名称
            description = str["description"]  # 简介
            latestOrder = str["latestOrder"]  # 总集数
            period = str["period"]  # 最后更新时间
            score = str["score"]  # 动漫评分
            categories = str["categories"]  # 动漫类型
            # print(categories)
            categories = ','.join(categories)
            # print(categories)
            imageUrl = str["imageUrl"]  # 动漫图片地址

            print(a_id, name, description, latestOrder, period, score, categories, imageUrl)

            Anime(a_id, name, description, latestOrder, period, score, categories, imageUrl)  # 写入动漫数据

            # date(a_id) # 输入动漫id
