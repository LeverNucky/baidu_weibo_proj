import sqlite3

db_path="H:/SJTU/data/baidu/data/dongfangzhixing/sample.db"

select_cmd="select * from query where create_time like '20150627%'"

db=sqlite3.connect(db_path)
c=db.cursor()

c.execute(select_cmd)
print(type(c))
#print(type(c.fetchall()))
ans=c.fetchall()
print ans[0]
c.close()

db.commit()
db.close()
