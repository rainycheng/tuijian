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

sqlc = sql + sys.argv[1]

cursor.execute(sqlc)
data = cursor.fetchall()
i=0
corpus = []

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
    corpus.append(chinese_seg)    
db.close()

if len(data)!=0:
   tfidf = transformer.transform(vectorizer.transform(corpus))
   word = vectorizer.get_feature_names()
   weight = tfidf.toarray()
   clabel = kmeans.predict(weight)
#   db2 = MySQLdb.connect("127.0.0.1","root","1234","tuijian",charset='utf8' )
   db2 = MySQLdb.connect("rds1fx2zo9067lgv33st.mysql.rds.aliyuncs.com","qylm","xkjd21ualk3Sd3i39","qylm",charset='utf8')
   cursor2 = db2.cursor()
   sql2 = """INSERT INTO CLASSIFICATION(ID,LABEL)
             VALUES(
          """
   sql3 = """INSERT INTO RECOMMENDATION(ID,T1,T2,T3)
             VALUES(   
          """
   sql4 = "select id from classification where label="+str(clabel[0])
   print sql4
   cursor2.execute(sql4)
   data2 = cursor2.fetchall()
#   print data2
   T1 = data2[random.randint(0,len(data2)-1)][0]
   T2 = data2[random.randint(0,len(data2)-1)][0]
   T3 = data2[random.randint(0,len(data2)-1)][0]

   sqlc = sql2 + sys.argv[1] + ','+str(clabel[0])+')'
   try:
       cursor2.execute(sqlc)
   except:
       print sqlc
       print "ID already exists in classification\n"

   sqlc = sql3 + sys.argv[1] + ','+str(T1)+','+str(T2)+','+str(T3)+')'
   try:
       cursor2.execute(sqlc)
   except:
       print sqlc
       print "ID already exists in recommendation\n"
   db2.commit()
   db2.close()
else:
    print "No news content correspond to ID="+sys.argv[1]
