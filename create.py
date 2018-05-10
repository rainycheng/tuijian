#!/usr/bin/python
#encoding=utf-8

import MySQLdb
import random

db = MySQLdb.connect("rds1fx2zo9067lgv33st.mysql.rds.aliyuncs.com","qylm","xkjd21ualk3Sd3i39","qylm")

cursor = db.cursor()

sql = """
      CREATE TABLE CLASSIFICATION(
      ID INT NOT NULL PRIMARY KEY,
      LABEL INT
      )
      """
sql2 = """
      CREATE TABLE RECOMMENDATION(
      ID INT NOT NULL PRIMARY KEY,
      T1 INT,
      T2 INT,
      T3 INT
      )
      """
sql3 = """
       INSERT INTO CLASSIFICATION(ID,LABEL)
       VALUES(
       """
sql4 = """
       SELECT * FROM CLASSIFICATION
       """
sql5 = """
       INSERT INTO RECOMMENDATION(ID,T1,T2,T3)
       VALUES( 
       """
fid = open('/home/html/tuijian/newsID.txt','r')
flabel = open('/home/html/tuijian/newslabel.txt','r')

#insert newsID and newslabel into CLASSIFICATION table
for newsid in fid.readlines():
    newslabel = flabel.readline()
    sqlc = sql3 + newsid + ',' + newslabel + ')'
    print sqlc
    cursor.execute(sqlc)
sqlc = "select * from classification"
cursor.execute(sqlc)
data =cursor.fetchall()
print data

fid.close()
fid = open('/home/html/tuijian/newsID.txt','r')

i=0
#insert newsID and recommend newsIDs into RECOMMENDATION table
for newsid in fid.readlines():
    sqlc = "select label from classification where ID="+newsid
    cursor.execute(sqlc)
    data = cursor.fetchall()
    sqlc = "select id from classification where label="+ str(data[0][0])
    cursor.execute(sqlc)
    data = cursor.fetchall()
    T1 = data[random.randint(0,len(data)-1)][0]
    T2 = data[random.randint(0,len(data)-1)][0]
    T3 = data[random.randint(0,len(data)-1)][0]
    sqlc = sql5 + newsid + ','+ str(T1)+','+str(T2)+','+str(T3)+')'
    cursor.execute(sqlc)

sqlc = "select * from recommendation"
cursor.execute(sqlc)

data = cursor.fetchall()
#print data

#cursor.execute(sql)
#cursor.execute(sql2)
db.commit()
db.close()

