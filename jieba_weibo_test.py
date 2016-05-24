import jieba
import jieba.analyse
import json
from collections import OrderedDict


path="H:/SJTU/data/baidu/data/dongfangzhixing/dongfangzhixing_weibo_sample"

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
    result=jieba.lcut(contents['text'])+jieba.lcut(contents['rt_text'])
    for word in result:
        if word:
            if word in d:
                d[word]+=1
            else:
                d[word]=1
#bar=OrderedDict(sorted(d.items(), key=lambda x: x[1]))
bar=sorted(d.items(), key=lambda x: x[1],reverse=True)
print(type(bar))
top=(bar[:40])

top_filt=[]
for x,y in top:
    if x not in [u' ']+stopwords:
        print x,y
        top_filt.append(x)
print top_filt
hotwords=[i.encode('utf8')+'\n' for i in top_filt]
fout=open('hotwords_weibo.txt','w')

fout.writelines(hotwords)

fout.close()
#print json.dumps(bar[:10],indent=4)
'''                
for k in d:
    print "dict[%s] =" % k,d[k]


for each in data:
    contents=json.loads(each)
    text_data.write(' '.join(jieba.cut_for_search(contents['text'])).encode('utf8'))
'''

