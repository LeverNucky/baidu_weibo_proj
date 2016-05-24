import json
import sqlite3

path="H:/SJTU/data/baidu/data/dongfangzhixing/dongfangzhixing_weibo_sample"
db_path="H:/SJTU/data/baidu/data/dongfangzhixing/weibo_sample.db"
create_cmd='''create table if not exists query
(rt_text text,
uid text,
text text,
rt_label int,
create_time text
label int)
'''
insert_cmd='insert into query values (?,?,?,?,?,?)'

db=sqlite3.connect(db_path)
c=db.cursor()
c.execute(create_cmd)

with open(path,'rb') as f:
    data=f.readlines()
columns=['rt_text','uid','text','rt_label','create_time','label']

for each in data:
    contents=json.loads(each)
    keys=tuple(contents[i] for i in columns)
    #print str(keys)
    c.execute(insert_cmd,keys)
c.close()
db.commit()
db.close()
    

