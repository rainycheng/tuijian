#!/usr/bin/python
#encoding=utf-8

import sys
import jieba
import MySQLdb
from lxml import html
import time
import re
import os
import sys
import codecs
import shutil
import random
import numpy as np
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib
from sklearn.cluster import KMeans

reload(sys)
sys.setdefaultencoding('utf-8')
stopkey=[line.strip().decode('utf-8') for line in open('stopkey.txt').readlines()]

#load trained model
vectorizer = joblib.load("/home/html/tuijian/vectorizer"+str(sys.argv[2])+".m")
transformer = joblib.load("/home/html/tuijian/tfidf"+str(sys.argv[2])+".m")
kmeans = joblib.load("/home/html/tuijian/kmeans"+str(sys.argv[2])+".m")

# 打开数据库连接
#db = MySQLdb.connect("127.0.0.1","root","1234","jhkfq",charset='utf8' )
db = MySQLdb.connect("rds1fx2zo9067lgv33st.mysql.rds.aliyuncs.com","qylm","xkjd21ualk3Sd3i39","qylm",charset='utf8')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

sql = "select AContent from news where ID="

sqlc = sql + str(sys.argv[1])
print sqlc
cursor.execute(sqlc)
data = cursor.fetchall()
i=0
corpus = []
try:
    for content in data:
        page = html.document_fromstring(content[0])
        news_text = page.text_content()
        f1=open('spacetext.txt','wb')
        f1.write(news_text)
        f1.close()
        f2=open('spacetext.txt','a+')
        chinese_text = ''
        for l2 in f2.readlines():
            ss = l2.strip()
            if len(ss) > 2:
               chinese_text = chinese_text + ss
        #print chinese_text
        seg_list = jieba.cut(chinese_text)
        chinese_seg = ' '.join(list(seg_list))    
        #corpus.append(chinese_seg)    
        outstr = ''
        for word in chinese_seg:
            if word not in stopkey:
                if word != '\t':
                    outstr += word
        corpus.append(outstr)
    
    if len(data)!=0:
       tfidf = transformer.transform(vectorizer.transform(corpus))
       word = vectorizer.get_feature_names()
       weight = tfidf.toarray()
       clabel = kmeans.predict(weight)
    
       sql4 = "select id from classification where label="+str(clabel[0]) + " and PID="+str(sys.argv[2]) + " order by id desc limit 30"
       print sql4
       cursor.execute(sql4)
       data2 = cursor.fetchall()
    #   print data2
       tid = []
       while len(tid) < 3:
           tdata = data2[random.randint(0,len(data2)-1)][0]
           if tdata != int(sys.argv[1]) and tdata not in tid:
               tid.append(tdata)
       print tid
       sql = "replace into recommendation(ID,PID,T1,T2,T3)value("+str(sys.argv[1])+','+str(sys.argv[2])+','+str(tid[0])+','+str(tid[1])+','+str(tid[2])+')'
       print sql
       cursor.execute(sql)
    else:
       print "No news content!\n"

except:
    sql = "select id from classification where label=0 and PID="+str(sys.argv[2])+" order by id desc limit 30"
    cursor.execute(sql)
    data2 = cursor.fetchall()
    tid = []
    while len(tid) < 3:
        tdata = data2[random.randint(0,len(data2)-1)][0]
        if tdata != int(sys.argv[1]) and tdata not in tid:
            tid.append(tdata)
    print tid
    sql = "replace into recommendation(ID,PID,T1,T2,T3)value("+str(sys.argv[1])+','+str(sys.argv[2])+','+str(tid[0])+','+str(tid[1])+','+str(tid[2])+')'
    print sql
    cursor.execute(sql)

db.commit()
db.close()
