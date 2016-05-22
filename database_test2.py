import sqlite3

db_path="H:/SJTU/data/baidu/data/dongfangzhixing/sample.db"


#start date 20150612

#end date 20150701
date=range(20150612,20150631)+[20150701]

count=0
select_cmd="select text from query where create_time like '%d%%'"%date[5]

hotwords=[line.strip() for line in open('hotwords.txt','rb').readlines()]
for i in range(len(hotwords)):
    hotwords[i]=hotwords[i].decode('utf8')
    
db=sqlite3.connect(db_path)
c=db.cursor()

c.execute(select_cmd)
print(type(c))
#print(type(c.fetchall()))
ans=c.fetchall()

for each in ans:
    for word in hotwords:
        count+=each.count(word)
print count
#print ans[0]
#print hotwords
c.close()

db.commit()
db.close()
