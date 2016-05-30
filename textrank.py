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
count=[0]*len(date)
pr=[[]]*len(date)

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
    result=[jieba.lcut(each) for each in ans]
    for j in range(len(result)):
        result[j]=[word for word in result[j] if word not in [u' ']+stopwords]
    #print get_cosine(Counter(result[0]),Counter(result[1]))
    G=nx.Graph()
    for k in range(len(result)):
        G.add_node(k)
    for x in range(len(result)):
        for y in range(x,len(result)):
            G.add_weighted_edges_from([(x,y,get_cosine(Counter(result[x]),Counter(result[y])))])                          
    pr[i]=nx.pagerank(G)
    #get_cosine(ans[0],ans[1])
print pr[0]
c.close()
db.commit()
db.close()
