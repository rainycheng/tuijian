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
import numpy as np  
from sklearn import feature_extraction    
from sklearn.feature_extraction.text import TfidfTransformer    
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.externals import joblib

reload(sys)
sys.setdefaultencoding('utf-8')

# 打开数据库连接
#db = MySQLdb.connect("127.0.0.1","root","1234","jhkfq",charset='utf8' )
db = MySQLdb.connect("rds1fx2zo9067lgv33st.mysql.rds.aliyuncs.com","qylm","xkjd21ualk3Sd3i39","qylm",charset='utf8')
# 使用cursor()方法获取操作游标
cursor = db.cursor()

sql1 = "select ID from news where PaperNameID="+ str(sys.argv[1])+' limit 1000;'
sql2 = "select AContent from news where ID="

cursor.execute(sql1)

data = cursor.fetchall()

i=0
corpus = [ ]
fid = open('/home/html/tuijian/newsID.txt','wb')
#traverse every news in news table

for id in data:
    sqlc = sql2 + str(id[0]) + ';'
    cursor.execute(sqlc)
    newsC = cursor.fetchall()
    # preprocess each news content, strip html text and spaces
    try:
        for title in newsC:
            page = html.document_fromstring(title[0])
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
        fid.write(str(id[0])+'\n')
    except:
        #print 'Document empty'
        jaq=0

fid.close()
f2.close()
#    i = i + 1
#    print i

print len(corpus)

vectorizer = CountVectorizer()
transformer = TfidfTransformer()

tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
word = vectorizer.get_feature_names()
weight = tfidf.toarray() 

vectorP = vectorizer.get_params()
tfidfP = transformer.get_params()

print 'vectorP:',vectorP
print 'tfidfP:',tfidfP

joblib.dump(vectorizer,"vectorizer"+str(sys.argv[1])+".m")
joblib.dump(transformer,"tfidf"+str(sys.argv[1])+".m")
   
resName = "BaiduTfidf_Result.txt"  
result = codecs.open(resName, 'w', 'utf-8')  
for j in range(len(word)):  
    result.write(word[j] + ' ')  
result.write('\r\n\r\n')

for i in range(len(weight)):  
#    print u"-------这里输出第",i,u"类文本的词语tf-idf权重------"    
    for j in range(len(word)):  
        result.write(str(weight[i][j]) + ' ')  
    result.write('\r\n\r\n') 
result.close()  

from sklearn.cluster import MiniBatchKMeans

flabel = open('/home/html/tuijian/newslabel.txt','wb')

clf = MiniBatchKMeans(n_clusters=20,batch_size=1000,random_state=0)
s = clf.fit(weight)
print s

print(clf.cluster_centers_)

print(clf.labels_)
i=1
while i <= len(clf.labels_):
    flabel.write(str(clf.labels_[i-1])+'\n')
    print i, clf.labels_[i-1]
    i = i+1

print(clf.inertia_)
joblib.dump(clf,"kmeans"+str(sys.argv[1])+".m")

