import jieba
import sqlite3
import networkx as nx
from cosine import get_cosine
from collections import OrderedDict,Counter

db_path="H:/SJTU/data/baidu/data/dongfangzhixing/baidu_sample.db"


#start date 20150612
#end date 20150701
date=range(20150612,20150631)+[20150701]
hour=range(24)
#count to record daily popularity

pr=[]
count=[0 for i in range(len(date))]

#print 'test1'
stopwords=[line.strip() for line in open('dict/stopwords.txt','rb').readlines()]
for i in range(len(stopwords)):
    stopwords[i]=stopwords[i].decode('utf8')
jieba.load_userdict("dict/event.txt")

select_cmd=[[0 for h in range(len(hour))] for d in range(len(date))]
for d in range(len(date)):
    for h in range(len(hour)):
        select_cmd[d][h]="select text from query where create_time like '%d%02d%%'"%(date[d],hour[h])

db=sqlite3.connect(db_path)
c=db.cursor()
for d in range(len(date)):
    print date[d]
    for h in range(len(hour)):
        c.execute(select_cmd[d][h])
        ans=c.fetchall()
        ans=[''.join(x) for x in ans]
        ans_dict=OrderedDict()
        for i in ans:
            ans_dict[i]=ans_dict.get(i,0)+1
        result=[jieba.lcut(each) for each in ans_dict.keys()]
        print len(result)
        if not result:
            continue
        for j in range(len(result)):
            result[j]=[word for word in result[j] if word not in [u' ']+stopwords]
        #print get_cosine(Counter(result[0]),Counter(result[1]))
        #print 'select finished...'
        G=nx.Graph()
        #print len(result)
        for x in range(len(result)):
            for y in range(x,len(result)):
                if get_cosine(Counter(result[x]),Counter(result[y])) != 0.0:
                #edges.append((x,y,get_cosine(Counter(result[x]),Counter(result[y]))))
                    G.add_weighted_edges_from([(x,y,ans_dict.values()[x]*ans_dict.values()[y]*get_cosine(Counter(result[x]),Counter(result[y])))])
        #print 'graph edges added...'
        pr=nx.pagerank(G)
        #print type(pr)
        #print pr
        pr_max=max(pr.values())
        for k in pr.keys():
            pr[k]=pr[k]/pr_max
        #pr_sort=sorted(pr.items(), key=lambda x: x[1],reverse=True)
        #pr_max_index=pr_sort[0][0]
        for k in range(len(result)):
            count[d]+=ans_dict.values()[k]*pr.values()[k]
            #count[d]+=ans_dict.values()[x]*ans_dict.values()[y]*get_cosine(Counter(result[pr_max]),Counter(result[k]))
        #print 'pagerank calculated...'
        #get_cosine(ans[0],ans[1])                      
        #print pr
print '------------------------------'
print count
print 'Done!'
c.close()
db.commit()
db.close()
#count:[7071.240260182336, 6922.617909962594, 25389.030852076266, 24517.05906176026, 4240.953282597996, 3395.8986262513495, 3299.2529717794673, 2830.696203626632, 1636.1704946203547, 1684.9956628372097, 1789.9062372398905, 2125.793506623668, 2074.2533742862847, 1768.4481554909314, 1442.6430915059425, 1187.365254779591, 1207.5984000435396, 1247.2006996235991, 1206.8898789065643, 1029.8443530069044]
