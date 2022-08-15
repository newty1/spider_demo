#beautifulsoup 将html文档转化为树形结构，每个节点都是python对象，归纳为四种
#tag  标签及其内容navistring  标签里的内容 beautifulsoup comment

from bs4 import BeautifulSoup
file = open("./baidu.html","rb")
html=file.read()
bs= BeautifulSoup(html,"html.parser")
print(bs.head)
print(bs.title.string)
print(bs.a.attrs)# 属性键值对
print(type(bs))
print(bs.a.string)#特殊的navistring


#文档搜索
# find_all
#字符串过滤，查找与字符串完全匹配的内容
t_list= bs.find_all("a")
#正则表达式
import re
t_list =bs.find_all(re.compile("a"))