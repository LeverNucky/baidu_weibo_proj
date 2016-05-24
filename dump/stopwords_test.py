stopwords=[]

test=[line.strip() for line in open('dict/stopwords.txt','rb').readlines()]

for i in range(len(test)):
    test[i]=test[i].decode('utf8')
    #print i
print(type(test))
print(type(test[0]))
print test[1]
print test[2]
print isinstance(u',',unicode)
print isinstance(u'.',unicode)
print isinstance(u'"',unicode)
print isinstance(u'?',unicode)
print isinstance(u' ',unicode)
print isinstance(test[1],unicode)
print isinstance(test[2],unicode)

