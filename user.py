#!/usr/bin/python
#encoding=utf-8

import MySQLdb
import random

db1 = MySQLdb.connect("rds1fx2zo9067lgv33st.mysql.rds.aliyuncs.com","qylm","xkjd21ualk3Sd3i39","qylm")
db2 = MySQLdb.connect("rds1fx2zo9067lgv33st.mysql.rds.aliyuncs.com","qylm","xkjd21ualk3Sd3i39","qylm")

cursor1 = db1.cursor()
cursor2 = db2.cursor()

sql1 = """
       create table appclass(AppID VARCHAR(50), Label INT)
       """
#cursor1.execute(sql1)

#sql2 = """
#       select AppID,count(1) from appviewrecord group by AppID
#       """
#cursor2.execute(sql2)
#
#data = cursor2.fetchall()
#
#for content in data:
#    sql3 = 'select NewID from appviewrecord where AppID=' +"'"+ str(content[0])+"'"
#    cursor2.execute(sql3)
#    newsid = cursor2.fetchall()
#    mycount = []
#    i=0
#    for i in range (0,20):
#        mycount.append(0)
#    for nid in newsid:
#        sql4 = 'select LABEL from classification where ID='+ str(nid[0])
#        cursor1.execute(sql4)
#        label = cursor1.fetchall()
#        if len(label) != 0:
#            mycount[label[0][0]] = mycount[label[0][0]]+1  
#    sql4 = """
#           insert into appclass(AppID,Label)
#           VALUES(
#           """
#    sqlc = sql4 + "'"+ str(content[0])+"',"+ str(mycount.index(max(mycount)))+')'
#    cursor1.execute(sqlc)
#    
sql5 = "create table T"
sql6 = "drop table t"

for i in range(0,5):
    sqlc = sql5 + str(i) +'(ID int)'
#    sqlc = sql6 + str(i)
    print sqlc
    cursor1.execute(sqlc)

db1.commit()
db2.commit()
db1.close()
db2.close()
