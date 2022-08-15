import re
# create  parten object

pat = re.compile("AA")# 这里的aa是正则表达式，用来验证其他的字符串
#m = pat.search("CBA")# 被校验的内容 serch进行比对查找只能前面的第一个
m = pat.search("AABCAADDCCAA")

m = re.search("asd","Asdasd")#这个是前面正则规则，后面查找
print(m)
print(re.findall("[A-Z]+","ASdadsadf"))
print(re.sub("a","A","adfc")) #substitute 替换  找到 a替换为A
a=123
print("%d"%a)