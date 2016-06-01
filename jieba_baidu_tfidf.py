from __future__ import division 
import jieba
import sqlite3
from rbo import score
from collections import OrderedDict
from math import log

db_path="H:/SJTU/data/baidu/data/dongfangzhixing/baidu_sample.db"
filt_num=20

#start date 20150612
#end date 20150701
date=range(20150612,20150631)+[20150701]
#count to record daily popularity
count=[0]*len(date)

d=[OrderedDict() for i in range(len(date))]
idf_d=dict()
bar=[[] for i in range(len(date))]
top=[[] for i in range(len(date))]
top_filt=[[] for i in range(len(date))]
fw=[[] for i in range(len(date))]
stopwords=[line.strip() for line in open('dict/stopwords.txt','rb').readlines()]
for i in range(len(stopwords)):
    stopwords[i]=stopwords[i].decode('utf8')
jieba.load_userdict("dict/event.txt")

select_cmd=[None]*len(date)
for i in range(len(date)):
    select_cmd[i]="select text from query where create_time like '%d%%'"%date[i]

idf_cmd='select text from query'
db=sqlite3.connect(db_path)
c=db.cursor()

for i in range(len(date)):
    c.execute(select_cmd[i])
    ans=c.fetchall()#tupel
    ans=[''.join(x) for x in ans]#unicode
    for each in ans:
        result=jieba.lcut(each)    
        for word in result:
            if word:
                if word in d[i]:
                    d[i][word]+=1
                else:
                    d[i][word]=1
for i in range(len(date)):
    bar[i]=sorted(d[i].items(), key=lambda x: x[1],reverse=True)
    top[i]=bar[i][:50]
    cur=0
    for x,y in top[i]:
        if cur>=filt_num:
            break
        if x not in [u' ']+stopwords:
            print x,y
            top_filt[i].append(x)
            fw[i].append(y)
            cur+=1
c.execute(idf_cmd)
text=c.fetchall()
numerator=len(text)
text=[''.join(x) for x in text]
for i in range(len(date)):
    for j in range(filt_num):
        if top_filt[i][j] not in idf_d:
            tmp_count=sum([1 if top_filt[i][j] in query else 0 for query in text])         
            #tmp_count=sum(tmp)
            idf_d[top_filt[i][j]]=tmp_count
        else:
            tmp_count=idf_d[top_filt[i][j]]
        count[i]+=log(numerator/(tmp_count+1),10)*fw[i][j]
print count
#[0.6017561140807253, 0.5598948843537359, 1.0, 0.9377961839530199, 0.39425172299306155, 0.29740884725124245, 0.2776232643221749, 0.2214848836985243, 0.14013356590000803, 0.1552230855563824, 0.18073387817853942, 0.2123713121812358, 0.20267789705491057, 0.15455745340046445, 0.12725565118250998, 0.09596037649014796, 0.10868157611522977, 0.11948797550515836, 0.11266231327021377, 0.09063398748813163]         
c.close()
db.commit()
db.close()
