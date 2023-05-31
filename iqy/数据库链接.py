import pymysql


def date():
    conn = pymysql.connect(host='localhost',
                           user='root',
                           passwd='root',
                           port=3306,
                           db='sushe',
                           charset='utf8')

    cs = conn.cursor()

    usersvalues = []
    for num in range(1, 20000):
        usersvalues.append(('在list中的每一个元素必须是元组', num))

    cs.executemany('insert into table_name values(%s,%s)', usersvalues)

    conn.commit()
    print("写入成功")

    conn.close()
    cs.close()


class change():
    def data(self):
        conn = pymysql.connect(host='localhost',
                               user='root',
                               passwd='root',
                               port=3306,
                               db='video',
                               charset='utf8'
                               )
        return conn


change = change().data()
cs = change.cursor()
a = 202030000001
for i in range(202030000188, 202030002918):
    ue = (a, i)
    cs.execute('UPDATE film SET f_Id = %s where f_Id = %s', ue)
    a = a + 1
    print(a, i)
    change.commit()
    print('完成', a)

change.close()
cs.close()

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51"
# }
#
# urld = "https://mesh.if.iqiyi.com/portal/videolib/pcw/data?version=1.0&ret_num=30&page_id=0&device_id=7345fb3fc83133eed54b6ba783a07a9a&passport_id=&recent_selected_tag=%E7%BB%BC%E5%90%88&recent_search_query=&ip=202.108.14.240&channel_id=1&tagName=&mode=24"
#
# # url = urld.format(a)
# req = requests.get(urld, headers=headers).content.decode()
# strList = json.loads(req)
#
# f_Star = ""
#
# strList = strList["data"]
# # str = strList["contributor"]
# for i in strList:
#     f_Area = i.get("tag_pcw", "null")
#     print(f_Area)


# a =
# b =
#
# date(a,b)
