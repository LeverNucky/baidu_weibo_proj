import jieba
import sqlite3
import networkx as nx
from cosine import get_cosine
from collections import OrderedDict,Counter

db_path="H:/SJTU/data/baidu/data/dongfangzhixing/baidu_sample.db"


#start date 20150612
#end date 20150701
date=range(20150612,20150631)+[20150701]
#count to record daily popularity

pr=[]
#print 'test1'
stopwords=[line.strip() for line in open('dict/stopwords.txt','rb').readlines()]
for i in range(len(stopwords)):
    stopwords[i]=stopwords[i].decode('utf8')
jieba.load_userdict("dict/event.txt")

select_cmd=[None]*len(date)

select_cmd="select text from query where create_time like '%d%%'"%date[5]

db=sqlite3.connect(db_path)
c=db.cursor()

c.execute(select_cmd)
ans=c.fetchall()
ans=[''.join(x) for x in ans]
print len(set(ans))
result=[jieba.lcut(each) for each in ans]
print len(result)

result=result[:1000]
for j in range(len(result)):
    result[j]=[word for word in result[j] if word not in [u' ']+stopwords]
#print get_cosine(Counter(result[0]),Counter(result[1]))
print 'select finished...'
G=nx.Graph()
print len(result)
for x in range(len(result)):
    for y in range(x,len(result)):
        if get_cosine(Counter(result[x]),Counter(result[y])) != 0.0:
        #edges.append((x,y,get_cosine(Counter(result[x]),Counter(result[y]))))
            G.add_weighted_edges_from([(x,y,x+y)])

print 'graph edges added...'
pr=nx.pagerank(G)
print 'pagerank calculated...'
#get_cosine(ans[0],ans[1])                      
print pr

print 'Done!'
c.close()
db.commit()
db.close()
