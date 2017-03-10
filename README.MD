## 基础数据准备  

```
# scrapy crawl useragent -o useragents.json

关闭settings.py中的ProxyMiddleware中间件
# scrapy crawl hideproxy -o proxylist.json
```

注意修改settings.py中的中间件名