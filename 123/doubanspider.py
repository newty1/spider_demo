from bs4 import BeautifulSoup  # 网页解析，数据获取
import re  # 正则表达式
import urllib.request, urllib.error  # 制定URL 获取url
import xlwt  # excel操作
import sqlite3  # sqilte操作





def main():
    baseurl = "https://movie.douban.com/top250?start="
    savepath = r"豆瓣电影Top250.xls"
    dbpath="movie.db"
    datalist = getData(baseurl)
   # saveData(datalist,savepath) #储存在xls表里
    saveData2(datalist,dbpath) #存储在sqlite数据库里
    print("爬取完毕")

# 正则规则
# 影片详情的链接的规则
findlink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象，表示规则（字符串的模式） 全局变量
# 影片的图片的
findimgsrc = re.compile(r'<img.*src="(.*?)"', re.S)  # re.S 让换行符包含在字符中
# 影片的片名
findtitle = re.compile(r'<span class="title">(.*)</span>')
# 影片评分
findrating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 评价人数
findjudge = re.compile(r'<span>(\d*)人评价</span>')
# 找到概况
findinq = re.compile(r'<span class="inq">(.*)</span>')
# 找到影片的相关内容
findbd = re.compile(r'<p class="">(.*?)</p>', re.S)  # 忽视换行符 加上问号 为懒惰模式 不加问号为贪婪模式


# 爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0, 10):  # 调用获取页面信息的函数
        url = baseurl + str(i * 25)
        html = askURL(url)  # 获取网页源码
        # 2 逐一解析
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all("div", class_="item"):  # 查找符合要求的字符串形成列表
            # print(item)# 测试： 查看电影item全部信息
            data = []  # 保存一步电影的所有信息
            item = str(item)  # 转成字符串，使用re库
            # 获取到影片详情的超链接
            link = re.findall(findlink, item)[0]  # re库用正则表达式来查找对应的字符串
            data.append(link)

            imgsrc =re.findall(findimgsrc,item)[0] # 添加图片
            data.append(imgsrc)

            titles = re.findall (findtitle,item) # 添加title
            if(len(titles)==2):
                ctitle=titles[0]
                data.append(ctitle) # 添加中文名
                otitle= titles[1].replace("/","") #去掉无关符号
                data.append(otitle) #添加外国名
            else:
                data.append(titles[0])
                data.append(" ")# 留空
            rating= re.findall(findrating,item)[0] # 添加评分
            data.append(rating)

            judgenum=re.findall(findjudge,item)[0]  #添加评价人数
            data.append(judgenum)

            inq =re.findall(findinq,item) # 添加概述
            if len(inq) !=0 :
                inq=inq[0].replace("。","")  #去掉句号
                data.append(inq)
            else:
                data.append(" ")            #留空

            bd=re.findall(findbd,item)[0]
            bd=re.sub('<br(\s+)?/>(\s+)?'," ",bd) #去掉<br/>
            bd=re.sub('/'," ",bd) #替换斜杠
            data.append(bd.strip()) # 去掉前后的空格

            datalist.append(data) # 把处理好的一部电影信息放入到datalist
            #print(datalist) #测试
    return datalist


# 得到指定一个URL的网页内容
def askURL(url):
    head = {  # 伪装头部
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77"
    }  # 用户代理告诉服务器，接受什么水平的内容
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except Exception as e:
        print(1123)
        if hasattr(e, "code"):  # 有这个code
            print(e.code)
        if hasattr(e, "reason"):  # 如果结果中包含reasson
            print(e.reason)
    return html


# 存储数据
def saveData(datalist,savepath):
    print("saving---")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)  # 创建workbook 对象
    sheet = book.add_sheet("豆瓣电影Top250",cell_overwrite_ok=True)  # 创建工作表
    col =("电影详情链接","图片链接","影片中文名","影片外国名","评分","评价数","概况","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i])#写入列名
    for i in range(0,250):
        print("第%d条"%i)
        data =datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])   #数据
    book.save(savepath)  # 保存数据表

def saveData2(datalist,dbpath):  #保存数据到sqllite数据库里
    init_db(dbpath)
    conn=sqlite3.connect(dbpath)
    cursor= conn.cursor()
    for data in datalist:
        for index in range(len(data)):
            if(index==4 or index ==5):
                pass
            else:
                data[index]='"'+data[index]+'"'
        sql='''
                insert into movie250(
                info_link,pic_link,cname,ename,score,rated,instroduction,info)
                values (%s)'''%",".join(data) #字符串用占位符填充
        print(sql)
        cursor.execute(sql)
        conn.commit()
    cursor.close()
    conn.close()
def init_db(dbpath):
    sql = '''
            create table if not exists movie250 
            (
            id integer primary key autoincrement,
            info_link text,
            pic_link text,
            cname varchar,
            ename varchar,
            score numeric,
            rated numeric,
            instroduction text,
            info text 
            )
    '''     #创建数据表
    conn =sqlite3.connect(dbpath)
    cursor=conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

if __name__ == "__main__":

   main()
# 调用函数
