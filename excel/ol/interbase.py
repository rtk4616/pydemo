import os,sys,json
import requests
import bs4

playload={'name':'中文','ie':'UTF-8'}
print(json.dumps(playload,ensure_ascii=False))
r=requests.post('http://127.0.0.1:8080/test',json=playload)
print(r.text)

