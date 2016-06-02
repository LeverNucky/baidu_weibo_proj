import jieba
import sqlite3
from rbo import score
from collections import OrderedDict

db_path="H:/SJTU/data/baidu/data/dongfangzhixing/baidu_sample.db"
filt_num=20

#start date 20150612
#end date 20150701
date=range(20150612,20150631)+[20150701]
#count to record daily popularity
count=[0]*len(date)

d=[OrderedDict() for i in range(len(date))]
bar=[[] for i in range(len(date))]
top=[[] for i in range(len(date))]
top_filt=[[] for i in range(len(date))]

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
            top_filt[i].append(x)
            cur+=1
print top_filt[0]
print top_filt[1]

test=[u'\u4e1c\u65b9\u4e4b\u661f', u'\u6c89\u8239', u'\u9047\u96be', u'\u73b0\u573a', u'\u4e8b\u6545', u'\u4e00\u4f4d', u'\u8bb0\u8005', u'\u4e00\u8d77', u'\u6b64\u523b', u'\u4eba\u5458', u'cn', u'http', u't', u'\u9ed8\u54c0', u'\u5934\u4e03', u'\u65f6', u'\u9047\u96be\u8005', u'\u957f\u6c5f', u'\u4e2d', u'\u8f6c\u53d1']
for i in range(len(date)):
    print score(test,top_filt[i])
    
c.close()
db.commit()
db.close()
