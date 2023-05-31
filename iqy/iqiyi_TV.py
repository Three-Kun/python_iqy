import json

import pymysql
import requests


class inte():
    def conn(self):
        conn = pymysql.connect(host='localhost',
                               user='root',
                               passwd='root',
                               port=3306,
                               db='video',
                               charset='utf8'
                               )

        return conn

    def TV(a_Id, a_title, hot_score, a_total_number, a_type, f_Update_Time, a_image_url, a_description, a_contributor):
        param = (
            a_Id, a_title, hot_score, a_total_number, a_type, f_Update_Time, a_contributor, a_image_url, a_description)

        # sql = 'insert into tv (t_Id, t_title, t_heat, t_total_number, t_type, t_Update_Time, t_image_url, t_description) values (%s,%s,%s,%s,%s,%s,%s,%s)on duplicate key update t_Star = %s, t_type = %s'  # 插入数据时覆盖重复
        sql = 'insert ignore into tv (t_Id, t_title, t_heat, t_total_number, t_type, t_Update_Time, t_Star, t_image_url, t_description) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        conn = inte().conn()
        cs = conn.cursor()
        cs.execute(sql, param)
        conn.commit()
        print('电视数据写入')
        inte().TV_pending(a_id=a_Id)

    def TV_pending(self, a_id):
        tv_urls = "https://pcw-api.iqiyi.com/albums/album/avlistinfo?aid={}&page=1&size=200&callback="
        tv_url = tv_urls.format(a_id)
        tv_req = requests.get(tv_url, headers).content
        tv_strs = json.loads(tv_req)
        tv_str = tv_strs['data']['epsodelist']
        user = []
        x = 0
        for str in tv_str:
            x = x + 1
            p_title = str['name']  # 电视名称
            p_id = x  # 第几集
            a_movieurls = str['playUrl']  # 播放路径
            a_id = a_id  # id
            # print(p_title, p_id, a_movieurls, a_id)
            user.append((p_title, p_id, a_movieurls, a_id))
        inte().TV_inte(user=user)

    def TV_inte(self, user):

        conn = inte().conn()
        cs = conn.cursor()

        # sql = "insert ignore into tv_pending(t_p_title, t_p_numint, t_p_movieurls, t_id) values (%s,%s,%s,%s)"  # 插入数据时跳过重复
        sql = "insert ignore into tv_pending(t_p_title, t_p_numint, t_p_movieurls, t_id) values (%s,%s,%s,%s)"
        cs.executemany(sql, user)
        conn.commit()
        try:
            print("集数写入成功")
            conn.close()
            cs.close()
        except Exception:
            print('集数写入失败')
            conn.close()
            cs.close()


if __name__ == '__main__':
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34"
    }
    urls = "https://mesh.if.iqiyi.com/portal/videolib/pcw/data?version=1.0&ret_num=20&page_id={}&device_id=81ffb48d000cc90b4ca2d6e64d416e0f&passport_id=&recent_search_query=&channel_id=2&tagName=&mode=24"
    num = int(input("输入需爬页数-一页20条数据："))
    for i in range(1, num + 1):
        url = urls.format(i)
        req = requests.get(url, headers=headers).content

        str = json.loads(req)

        strs = str['data']

        for str in strs:
            a_Id = str['entity_id']  # 电视ID
            a_title = str['title']  # 电视名称
            hot_score = str['hot_score']  # 热度
            a_total_number = str['dq_updatestatus']  # 总集数
            a_type = str.get('tag', "null")  # 电视类型
            f_Update_Time = str['showDate']  # 最后更新时间
            a_image_url = str['image_url_normal']  # 电视图片地址
            a_description = str.get('description', "null")  # 简介
            contributor = ""
            for i in str.get('contributor', 'null'):
                name = i['name']
                contributor = name + " " + contributor
            # print(contributor)
            print(a_title)
            inte.TV(a_Id=a_Id, a_title=a_title, hot_score=hot_score, a_total_number=a_total_number, a_type=a_type,
                    f_Update_Time=f_Update_Time, a_image_url=a_image_url, a_description=a_description,
                    a_contributor=contributor)
