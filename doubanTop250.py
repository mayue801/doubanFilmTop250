# -*- coding: utf-8 -*-
import requests
import time
import re
import pymysql

conn = pymysql.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    passwd = '123456',
    db = 'movie',
    charset = 'utf8mb4' #mysql中utf8不能存储4个字节的字符
)

cursor = conn.cursor()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
cookies = {'cookie': 'll="108288"; bid=G4oiRkK4MYo; _vwo_uuid_v2=D09E6E6F27485A2A9534CF9DAC6455E7C|6d2f5c57a592a6cee6084f1489fb46f2; gr_user_id=646ad381-40f6-40d6-af0c-e5cdb6b839b6; _ga=GA1.2.1544213960.1527212266; ps=y; ue="2287093698@qq.com"; push_doumail_num=0; __utmv=30149280.6232; ap=1; __utma=30149280.1544213960.1527212266.1527431188.1527438227.14; __utmb=30149280.0.10.1527438227; __utmc=30149280; __utmz=30149280.1527438227.14.7.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; push_noty_num=0; as="https://movie.douban.com/subject/1292052/"'}

def getMovieList(start):
    res = requests.get('https://movie.douban.com/top250?start='+ start, headers = headers, cookies = cookies)
    html = res.text

    # print(html)
    reg = r'<div class="item">.*?<a href="(.*?)">.*?<span class="title">(.*?)</span>.*?<p class="">(.*?)&nbsp.*?<br>.*?(.*?)&nbsp;/&nbsp;(.*?)&nbsp;/&nbsp;(.*?)</p>'
    reg += r'.*?<div class="star">.*?property="v:average">(.*?)</span>.*?<span>(.*?)</span>'
    reg += r'.*?<span class="inq">(.*?)</span>'

    return re.findall(reg, html, re.S)




def getComment(url):
    res = requests.get(""+url, headers = headers, cookies = cookies)
    html = res.text

    reg = r'<span class="comment-info">.*?class="">(.*?)</a>.*?<span class="comment-time.*?>(.*?)</span>'
    reg += r'.*?<p class="">(.*?)</p>'

    return re.findall(reg, html, re.S)


def getMovieContent(url,movieId):
    res = requests.get(url, headers = headers, cookies = cookies)
    html = res.text

    # print(html)

    reg = r'<span class="actor">(.*?)<br/>'
    actors = re.findall(reg, html)

    if '<div class="hd">' in html:
        prize = '<div class="hd">(.*?)'
    else:
        prize = ''

    if "又名:" in html:
        alias = '</span> (.*?)<br/>'
    else:
        alias = ''


    reg = r'<a class="nbgnbg".*?<img src="(.*?)".*?'
    reg += r'.*?<span property="v:initialReleaseDate" content="(.*?)".*?<span property="v:runtime" content="(.*?)">.*?'+alias
    reg += r'.*?<span property="v:summary".*?>(.*?)</span>.*?'+ prize +'<div id="recommendations" class="">'
    reg += r'.*?<a class="comment_btn j a_collect_btn".*?<a href="(.*?)">'

    if prize != '':
        if alias != '':
            poster, time, movieLength, otherName, summary, award, commentLink = re.findall(reg, html, re.S)[0]
        else:
            poster, time, movieLength, summary, award, commentLink = re.findall(reg, html, re.S)[0]
            otherName = ""
        reg = r'<li>.*?<a href=".*?">(.*?)</a>.*?<li>(.*?)</li>'
        for awardName, awardType in re.findall(reg, award, re.S):
            cursor.execute("insert into award(movieId, name, type) values('{}', '{}', '{}')".format(
                movieId, (""+awardName).replace("'", r"\'"), (""+awardType).replace("'", r"\'")))
    else:
        resultList = re.findall(reg, html, re.S)
        if len(resultList) != 0:
            if alias != '':
                poster, time, movieLength, otherName, summary, commentLink =  resultList[0]
            else:
                poster, time, movieLength, summary, commentLink = resultList[0]
                otherName = ""
        else:
            return

    # print(poster, actors, time, movieLength, otherName, summary, award, commentLink)
    if len(otherName) != 0:
        updateSql = "update movie set poster='{}', time='{}', movieLength='{}',otherName='{}', summary='{}', commentLink='{}' where id = '{}'".format(
            poster, (""+time).strip("\n").strip(), movieLength, (""+otherName).replace("'", r"\'"),(""+summary).strip().replace("'", r"\'"),
            (""+commentLink).replace("'", r"\'"), movieId)
    else:
        updateSql = "update movie set poster='{}', time='{}', movieLength='{}', summary='{}', commentLink='{}' where id = '{}'".format(
            poster, ("" + time).strip("\n").strip(), movieLength,
            ("" + summary).strip().replace("'", r"\'"), ("" + commentLink).replace("'", r"\'"), movieId
        )

    cursor.execute(updateSql)

    # print(award)

    reg = r'<a href="(.*?)" rel="v:starring">(.*?)</a>'
    for link, name in re.findall(reg, str(actors)):
        cursor.execute("insert into actor(movieId, link, name) values('{}', '{}', '{}')".format(
            movieId, (""+link).replace("'", r"\'"), (str(name))))

    for userName, time, commentContent in getComment(commentLink):
        cursor.execute("insert into comment(movieId, userName, content, time) values('{}', '{}', '{}', '{}')".format(
            movieId, (""+userName).replace("'", r"\'"), (""+commentContent).replace("'", r"\'"), (""+time).strip("\n").strip()))

    conn.commit()

# getMovieContent("https://movie.douban.com/subject/3442220/", 12)

def startUpMovie():
    count = 0
    for i in range(0,10):
        for link, title, director, age, country, type, score, evaluationNum, note in getMovieList(str(25*i)):
            print('正在存储----{}'.format(""+title))
            # print(link, title, director, age, country, type, score, evaluationNum, note)
            cursor.execute("insert into movie(link, title, director, age, country, type, score, evaluationNum, note)"
                           " values('{}', '{}','{}', '{}', '{}', '{}','{}', '{}', '{}')".format(
                            link, (""+title), (""+director[6:]).strip("导演: ").strip().replace("'", r"\'"), (""+age).strip("\n").strip(),
                             country, (""+type).strip("\n").strip().replace("'", r"\'"), score, evaluationNum[0:-3], note)
                           )


            getMovieContent(link, cursor.lastrowid)
            conn.commit()
            count += 1
            if count % 2 == 0:
                time.sleep(3)
            print("num:'{}'".format(count))
        #     break
        # break
    # return count

startUpMovie()
# print(startUpMovie())




















