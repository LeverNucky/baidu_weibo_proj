import json
import sqlite3

path="H:/SJTU/data/baidu/data/dongfangzhixing/dongfangzhixing_query_sample"
db_path="H:/SJTU/data/baidu/data/dongfangzhixing/baidu_sample.db"
create_cmd='''create table if not exists query
(qid text,
label text,
create_time text,
uid text,
text text)
'''
insert_cmd='insert into query values (?,?,?,?,?)'

db=sqlite3.connect(db_path)
c=db.cursor()
c.execute(create_cmd)

with open(path,'rb') as f:
    data=f.readlines()
columns=['qid','label','create_time','uid','text']

for each in data:
    contents=json.loads(each)
    keys=tuple(contents[i] for i in columns)
    #print str(keys)
    c.execute(insert_cmd,keys)
c.close()
db.commit()
db.close()
    

