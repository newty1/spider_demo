import sqlite3

conn= sqlite3.connect("test.db") # 打开或创建数据库文件
print("Opened database successsfully")
c=conn.cursor() #获取游标
sql='''
    create table kkkk
        ( id int primary key not null,
        name text not null,
        age int not null,
        address char(50),
        salary real);
        
    '''
c.execute(sql)  #执行sql语句
conn.commit()  # 提交数据库
conn.close()   #关闭数据库链接
print("Created tables successsfully")