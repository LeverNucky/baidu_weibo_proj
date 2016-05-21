import jieba
import jieba.analyse
import json
from collections import OrderedDict

path="H:/SJTU/data/baidu/data/dongfangzhixing/dongfangzhixing_query_sample"
text_path="H:/SJTU/data/baidu/data/dongfangzhixing/text_data.txt"
with open(path,'rb') as f:
    data=f.readlines()

d=OrderedDict()
#text_data=open(text_path,'w')
#print type(data),data[0]
for each in data:
    contents=json.loads(each)
    result=jieba.lcut_for_search(contents['text'])
    for word in result:
        if word:
            if word in d:
                d[word]+=1
            else:
                d[word]=1
#bar=OrderedDict(sorted(d.items(), key=lambda x: x[1]))
bar=sorted(d.items(), key=lambda x: x[1],reverse=True)
top=(bar[:50])
for i in top:
    print i[0],i[1]

#print json.dumps(bar[:10],indent=4)
'''                
for k in d:
    print "dict[%s] =" % k,d[k]


for each in data:
    contents=json.loads(each)
    text_data.write(' '.join(jieba.cut_for_search(contents['text'])).encode('utf8'))
'''

