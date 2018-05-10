#!/usr/bin/python
#encoding=utf-8

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

##load trained model
#vectorizer = joblib.load("/home/html/tuijian/vectorizer"+str(sys.argv[2])+".m")
#transformer = joblib.load("/home/html/tuijian/tfidf"+str(sys.argv[2])+".m")
#kmeans = joblib.load("/home/html/tuijian/kmeans"+str(sys.argv[2])+".m")
#
db = MySQLdb.connect("rds1fx2zo9067lgv33st.mysql.rds.aliyuncs.com","qylm","xkjd21ualk3Sd3i39","qylm")

cursor = db.cursor()

sql = "select ID from news where PaperNameID=" + str(sys.argv[1])
print sql
db.commit()
cursor.execute(sql)
data = cursor.fetchall()
i=0
for id0 in data:
    try:
       os.system("python predict2.py "+ str(id0[0]) + " " + str(sys.argv[1]))
    except:
       i = i+1
       break
print i
db.close()

