#!/usr/bin/python
#encoding=utf-8

import MySQLdb
import random

db1 = MySQLdb.connect("rds1fx2zo9067lgv33st.mysql.rds.aliyuncs.com","qylm","xkjd21ualk3Sd3i39","qylm")
db2 = MySQLdb.connect("rds1fx2zo9067lgv33st.mysql.rds.aliyuncs.com","qylm","xkjd21ualk3Sd3i39","qylm")
cursor1 = db1.cursor()
cursor2 = db2.cursor()

sql1 = """
       select ID from news order by CreateTime
       """
cursor2.execute(sql1)
data = cursor2.fetchall()
nlist= [] 
i=0
#for content in data:
#    nlist.append(content)
#    i = i + 1
#    if i%5 == 0:
#        i = 0
#for content in data:
#    print content

nlen = len(data)

nlist = []
nflag = [0,0,0,0,0]

sql2 = """
       insert into tjnewslist(ID) VALUE(
       """
sql3 = """
       delete from T"""
for i in range(0,5):
    sqlc = sql3 + str(i)
#    print sqlc
    cursor1.execute(sqlc)

sql4 = """
       insert into T"""

for k in range(0,5):
    
    for i in range(0,nlen,5):
        while len(nlist) < 5:
            rn = random.randint(0,4)
            if nflag[rn] == 0:
                nlist.append(rn)
                nflag[rn] = 1
        for j in range(0,5):
            if (i+nlist[j]) < nlen:
                sqlc = sql4 + str(k)+'(ID) VALUE(' + str(data[i+nlist[j]][0])+')'
#                print sqlc
                cursor1.execute(sqlc)
        nflag = [0,0,0,0,0]
        nlist = []
    
db1.commit()
db1.close()
