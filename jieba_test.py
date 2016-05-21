import jieba
import jieba.analyse
import json
from collections import OrderedDict


path="H:/SJTU/data/baidu/data/dongfangzhixing/dongfangzhixing_query_sample"
text_path="H:/SJTU/data/baidu/data/dongfangzhixing/text_data.txt"
with open(path,'rb') as f:
    data=f.readlines()

d=OrderedDict()

#jieba.analyse.set_stop_words("dict/stopwords.txt")

stopwords=[line.strip() for line in open('dict/stopwords.txt','rb').readlines()]

for i in range(len(stopwords)):
    stopwords[i]=stopwords[i].decode('utf8')
    
jieba.load_userdict("dict/event.txt")
#text_data=open(text_path,'w')
#print type(data),data[0]
for each in data:
    contents=json.loads(each)
    result=jieba.lcut(contents['text'])
    for word in result:
        if word:
            if word in d:
                d[word]+=1
            else:
                d[word]=1
#bar=OrderedDict(sorted(d.items(), key=lambda x: x[1]))
bar=sorted(d.items(), key=lambda x: x[1],reverse=True)
print(type(bar))
top=(bar[:50])
for i in top:
    if i[0] not in [u' ',u',',u'"',u'.',u'?']+stopwords:
        print i[0],i[1]

#print json.dumps(bar[:10],indent=4)
'''                
for k in d:
    print "dict[%s] =" % k,d[k]


for each in data:
    contents=json.loads(each)
    text_data.write(' '.join(jieba.cut_for_search(contents['text'])).encode('utf8'))
'''

