import urllib.request
# 使用get请求
# response = urllib.request.urlopen("http://www.baidu.com")
# print(response.read().decode('utf-8'))
# 获取post请求
import urllib.parse

# data =bytes(urllib.parse.urlencode({"hello":"world"}),encoding="utf-8")
# response =urllib .request.urlopen("http://httpbin.org/post",data=data,timeout=0.01)
# print(response.read())

url = "https://www.douban.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77"
}
req = urllib.request.Request(url,headers=headers)
response = urllib.request.urlopen(req)
print(response.read().decode("utf-8"))
