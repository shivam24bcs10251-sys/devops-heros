import json,urllib.request
alerts=json.load(urllib.request.urlopen('http://127.0.0.1:9090/api/v1/alerts'))['data']['alerts']
print(json.dumps([{'name':a['labels']['alertname'],'pod':a['labels'].get('pod'),'state':a['state'],'summary':a['annotations']['summary']} for a in alerts],indent=2))
