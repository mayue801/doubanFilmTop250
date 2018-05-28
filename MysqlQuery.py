# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
import pymysql
import json
import math


conn = pymysql.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    passwd = '123456',
    db = 'movie',
    charset = 'utf8mb4' #mysql中utf8不能存储4个字节的字符
)

cursor = conn.cursor()

def getJsonData(sql):
    cursor.execute(sql)

    data = cursor.fetchall()

    # print(data)
    return data


typeNameList = ['剧情','喜剧','动作','爱情','科幻','悬疑','惊悚','恐怖','犯罪',
            '同性','音乐','歌舞','传记','历史','战争','西部','奇幻','冒险',
            '灾难','武侠','情色']
def getMovieTypeJson():
    typeNumList = []
    for type in typeNameList:
        sql = r"select count(type) from movie where type like '%{}%'".format(type)
        dataM = getJsonData(sql)
        typeNumList.append(int(str(dataM).strip(r'(').strip(r',)')))

    return {'typeNameList' : typeNameList, 'typeNumList' : typeNumList}


def getPureList(ageList):
    numList = []
    # print(ageList)
    for age in ageList:
        numList.append(str(age).strip(r"('").strip(r"',)"))
    # print(numList)
    return numList


# getNumList((('2009',), ('2006',), ('1994',), ('1965',), ('1952',)))


def getMovieTreeJson():
    jsonFinal = '{"types": ['
    for type in typeNameList:
        sql = r"select distinct age from movie where type like '%{}%' order by age desc".format(type)
        ageList = getJsonData(sql)
        jsonFinal += '{{"name":"{}", "children":['.format(type)
        for age in getPureList(ageList):
            sql = r"select distinct country from movie where age = '{}' and type like '%{}%'".format(age, type)
            countryList = getJsonData(sql)
            countryArr = []
            jsonFinal += '{{"name":"{}", "children":['.format(age)
            for country in getPureList(countryList):
                if country.split(" ")[0] not in countryArr:
                    countryArr.append(country.split(" ")[0])
                else:
                    continue
                sql = r"select distinct score from movie where age = '{}' and type like '%{}%' and country like '{}%'" \
                      r"order by score desc".format(age, type, country.split(" ")[0])
                scoreList = getJsonData(sql)
                jsonFinal += '{{"name":"{}", "children":['.format(country.split(" ")[0])
                for score in getPureList(scoreList):
                    sql = r"select distinct movieLength from movie where age = '{}' and type like '%{}%' and country like '{}%'" \
                          r"and score = '{}' order by score desc".format(age, type, country.split(" ")[0], score)
                    movieLengthList = getJsonData(sql)

                    jsonFinal += '{{"name":"分数{}", "children":['.format(score)
                    for movieLength in getPureList(movieLengthList):
                        jsonFinal += '{{"name":"时长{}", "children":['.format(movieLength)
                        sql = r"select title, note from movie where age = '{}' and type like '%{}%' and country like '{}%'" \
                              r"and score = '{}' and movieLength = '{}' order by score desc".format(
                              age, type, country.split(" ")[0], score, movieLength)
                        titleNoteList = getJsonData(sql)

                        # print(age, type, country.split(" ")[0], score, movieLength, str(titleNoteList[0]).strip(","))
                        for title, note in titleNoteList:
                            jsonFinal += '{{"name":"{}", "value":"{}"}},'.format(title, note)
                            # print(jsonFinal[:-1])
                        jsonFinal = jsonFinal[:-1] + ']},'
                    jsonFinal = jsonFinal[:-1] + ']},'
                jsonFinal = jsonFinal[:-1] + ']},'
            jsonFinal = jsonFinal[:-1] + ']},'
        jsonFinal = jsonFinal[:-1] + ']},'
    jsonFinal = jsonFinal[:-1] + ']},'

    return jsonFinal[:-1]


def getAgeScoreJson():
    ageScoreMap = {}
    ageScoreMap['ages'] = ['Growth']
    ageScoreMap['ageNames'] = []
    sql = r'select DISTINCT age from movie ORDER BY age desc'
    ageList = getPureList(getJsonData(sql))
    # print(ageList)
    for age in ageList:
        avgScoreList = []
        for type in typeNameList:
            sql = r"select avg(score) from movie where age = '{}' and type like '%{}%'".format(age, type)
            avgScore = str(getPureList(getJsonData(sql))).strip("['").strip("']")
            if avgScore == 'None':
                avgScore = 0
            avgScoreList.append(round(float(avgScore)))
        ageScoreMap[str(age)] = avgScoreList
        ageScoreMap['ages'].append(str(age))
        # ageScoreMap['ageNames'].append('result.type' + str(age))
    ageScoreMap['names'] = typeNameList

    return ageScoreMap

# print(getAgeScoreJson())

def writeTypeJsonFile(path):
    with open(path, 'w') as f:
        json.dump(getMovieTypeJson(), f)

def writeAgeScoreJsonFile(path):
    with open(path, 'w') as f:
        json.dump(getAgeScoreJson(), f)

def writeTreeJsonFile(path):
    with open(path, 'w') as f:
        json.dump(getMovieTreeJson(), f)

# writeTypeJsonFile(r'C:\Users\Administrator\Desktop\books\movieType.txt')
# writeTreeJsonFile(r'C:\Users\Administrator\Desktop\books\movieTreeJson.txt')
writeAgeScoreJsonFile(r'C:\Users\Administrator\Desktop\books\movieAgeScoreJson.txt')