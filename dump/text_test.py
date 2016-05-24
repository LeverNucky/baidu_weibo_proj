text_path="H:/SJTU/data/baidu/data/dongfangzhixing/text_data.txt"
with open(text_path,'rb') as f:
    d=f.readlines()
print d[0][1:4]
print type(d),type(d[0])
