#!/usr/bin/python
#encoding=utf-8

import MySQLdb
import random
import sys

db1 = MySQLdb.connect("rds1fx2zo9067lgv33st.mysql.rds.aliyuncs.com","qylm","xkjd21ualk3Sd3i39","qylm")

cursor1 = db1.cursor()

if len(sys.argv) == 2:

    sql1= 'select label from appclass where AppID=' + "'" + str(sys.argv[1]) + "'"
    print sql1
    cursor1.execute(sql1)
    data = cursor1.fetchall()

    print 't'+str((random.randint(0,5)+data[0][0])%5)

else:
    print 'input parameters error! Please input AppID!'




