import json

import pymysql
import requests


def date(param):
    db = pymysql.connect(host='localhost',
                         user='root',
                         passwd='root',
                         port=3306,
                         db='video',
                         charset='utf8')

    cursor = db.cursor()

    sql = "insert ignore into film(f_Title, f_Url, f_Year, f_Score, f_images, f_Introduction, f_Type, f_Area, f_Star, f_Director) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    cursor.executemany(sql, param)

    db.commit()
    try:
        print("写入成功")
    except:
        print("写入失败")

    db.close()
    cursor.close()


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51"
}

urld = "https://mesh.if.iqiyi.com/portal/videolib/pcw/data?version=1.0&ret_num=30&page_id={}&device_id=3342205419140be1877d4cdc991310db&passport_id=&recent_selected_tag=%E7%BB%BC%E5%90%88&recent_search_query=&ip=202.108.14.240&channel_id=1&tagName=&mode=24"


for a in range(1, 2):
    url = urld.format(a)
    req = requests.get(url, headers=headers).content.decode()
    strList = json.loads(req)

    strList = strList["data"]
    ddd = []

    for str in strList:
        # print(str)
        f_Title = str.get("title", "null")  # '电影名称'
        f_Url = str.get("page_url", "null")  # '播放路径
        Year = str.get("showDate", "null")  # '年份'
        if Year != "null":
            f_Year = Year[0:4]

        f_Score = str.get("sns_score", "0.0")  # '评分'
        f_images = str.get("image_url_normal", "null")  # '电影图片'
        f_Introduction = str.get("description", "null")  # '简介'
        f_Type = str.get("tag", "null")  # '类型'
        f_Area = str.get("tag_pcw", "null")  # '地区'
        Star = str["contributor"]  # '主演'

        f_Star = ""
        f_Director = ""
        for i in Star:
            name = i["name"]
            f_Star = name + " " + f_Star

        Director = str["creator"]  # '导演'

        for i in Director:
            name = i["name"]
            f_Director = name + " " + f_Director

        ddd.append((f_Title, f_Url, f_Year, f_Score, f_images, f_Introduction, f_Type, f_Area, f_Star, f_Director))

        # print(f_Title)
        # print(f_Url)
        # print(f_Year)
        # print(f_Score)
        # print(f_images)
        # print(f_Introduction)
        # print(f_Type)
        # print(f_Area)
        # print(f_Star)
        # print(f_Director)
        # print()
    print(a)
    # date(param=ddd)
