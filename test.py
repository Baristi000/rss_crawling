import requests

res = requests.get("http://25.14.42.2:9200/_cat/allocation?format=json")
print(res.json()[0]["disk.indices"])