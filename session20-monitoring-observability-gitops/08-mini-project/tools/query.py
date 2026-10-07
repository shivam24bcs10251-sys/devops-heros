import json,sys,urllib.parse,urllib.request
query = sys.argv[1]
url = 'http://127.0.0.1:9090/api/v1/query?' + urllib.parse.urlencode({'query':query})
result = json.load(urllib.request.urlopen(url))
assert result['status']=='success',result
print('PromQL:',query)
for row in result['data']['result']: print(json.dumps({'labels':row['metric'],'value':row['value'][1]},sort_keys=True))
assert result['data']['result'], 'No metric samples returned'
