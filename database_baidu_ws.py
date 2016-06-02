from __future__ import division
import sqlite3

db_path="H:/SJTU/data/baidu/data/dongfangzhixing/baidu_sample.db"

#start date 20150612
#end date 20150701
date=range(20150612,20150631)+[20150701]
#count to record daily popularity
count=[0]*len(date)

hotwords=[line.strip() for line in open('hotwords_baidu.txt','rb').readlines()]
for i in range(len(hotwords)):
    hotwords[i]=hotwords[i].decode('utf8')

select_cmd=[None]*len(date)
for i in range(len(date)):
    select_cmd[i]="select text from query where create_time like '%d%%'"%date[i]

db=sqlite3.connect(db_path)
c=db.cursor()
for i in range(len(date)):
    c.execute(select_cmd[i])
    #print(type(c))
    #print(type(c.fetchall()))
    ans=c.fetchall()
    for each in ans:
        for word in hotwords:
            count[i]+=each.count(word)
#print count
#print ans[0]
#print hotwords
c.close()
print [i/max(count) for i in count]

db.commit()
db.close()
