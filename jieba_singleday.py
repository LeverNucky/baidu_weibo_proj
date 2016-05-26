import jieba
import sqlite3
from collections import OrderedDict

db_path="H:/SJTU/data/baidu/data/dongfangzhixing/baidu_sample.db"
filt_num=20

#start date 20150612
#end date 20150701
date=range(20150612,20150631)+[20150701]
#count to record daily popularity
count=[0]*len(date)

d=[OrderedDict() for i in range(len(date))]
bar=[[]]*len(date)
top=[[]]*len(date)

stopwords=[line.strip() for line in open('dict/stopwords.txt','rb').readlines()]
for i in range(len(stopwords)):
    stopwords[i]=stopwords[i].decode('utf8')
jieba.load_userdict("dict/event.txt")

select_cmd=[None]*len(date)
for i in range(len(date)):
    select_cmd[i]="select text from query where create_time like '%d%%'"%date[i]

db=sqlite3.connect(db_path)
c=db.cursor()

for i in range(len(date)):
    c.execute(select_cmd[i])
    ans=c.fetchall()
    ans=[''.join(x) for x in ans]
    for each in ans:
        result=jieba.lcut(each)    
        for word in result:
            if word:
                if word in d[i]:
                    d[i][word]+=1
                else:
                    d[i][word]=1
for i in range(len(date)):
    print '-------------------------------------------'
    print date[i]
    print '-------------------------------------------'
    
    bar[i]=sorted(d[i].items(), key=lambda x: x[1],reverse=True)
    top[i]=bar[i][:50]
    cur=0
    for x,y in top[i]:
        if cur>=filt_num:
            break
        if x not in [u' ']+stopwords:
            print x,y
            cur+=1
    
    
c.close()
db.commit()
db.close()
