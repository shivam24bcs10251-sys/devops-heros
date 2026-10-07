"""Live checks; requires app/Prometheus/Grafana port-forwards and kubectl."""
import json, subprocess, urllib.error, urllib.parse, urllib.request
APP='http://127.0.0.1:8084'
def get(url):
    with urllib.request.urlopen(url,timeout=10) as response: return response.read()
def query(expr):
    response=json.loads(get('http://127.0.0.1:9090/api/v1/query?'+urllib.parse.urlencode({'query':expr})))
    assert response['status']=='success' and response['data']['result'],response
    return [float(row['value'][1]) for row in response['data']['result']]
health=json.loads(get(APP+'/health'))
assert health['healthy'] is True and health['version']=='v2',health
print('PASS: HTTP application health and Git release version v2')
req=urllib.request.Request(APP+'/work',headers={'X-Trace-ID':'session20-final-verify'})
with urllib.request.urlopen(req) as response:
    body=json.load(response)
    assert body['trace_id']=='session20-final-verify' and response.headers['X-Trace-ID']==body['trace_id']
print('PASS: request correlation ID in response and header')
try: get(APP+'/missing')
except urllib.error.HTTPError as error: assert error.code==404
else: raise AssertionError('Unknown route should return 404')
print('PASS: unknown route returns 404')
metrics=get(APP+'/metrics').decode()
assert 'process_cpu_seconds_total' in metrics and 'process_resident_memory_bytes' in metrics
assert int(next(line.split()[1] for line in metrics.splitlines() if line.startswith('process_resident_memory_bytes ')))>0
print('PASS: real CPU counter and nonzero Linux resident memory')
assert len(query('up{job="session20-app"}'))==2 and all(v==1 for v in query('up{job="session20-app"}'))
assert query('sum(demo_dependency_healthy{job="session20-app"})')==[2]
assert query('sum(process_resident_memory_bytes{job="session20-app"})')[0]>0
print('PASS: Prometheus scrapes two healthy application targets and memory')
alerts=json.loads(get('http://127.0.0.1:9090/api/v1/alerts'))['data']['alerts']
assert not alerts,alerts
print('PASS: all demo alerts resolved')
assert json.loads(get('http://127.0.0.1:3004/api/health'))['database']=='ok'
dash=json.loads(get('http://127.0.0.1:3004/api/dashboards/uid/session20'))
assert len(dash['dashboard']['panels'])==6
print('PASS: Grafana health and six provisioned dashboard panels')
application=json.loads(subprocess.check_output(['kubectl','--context','devops-assignment','get','application','session20-mini','-n','session20-argocd','-o','json']))
assert application['status']['sync']['status']=='Synced' and application['status']['health']['status']=='Healthy'
assert application['status']['operationState']['operation']['initiatedBy']['automated'] is True
assert application['spec']['syncPolicy']['automated']['selfHeal'] is True
print('PASS: Argo CD Synced/Healthy, automated delivery and self-heal enabled')
deployment=json.loads(subprocess.check_output(['kubectl','--context','devops-assignment','get','deploy','session20-mini','-n','session20','-o','json']))
assert deployment['spec']['replicas']==2 and deployment['status']['readyReplicas']==2
assert deployment['spec']['template']['spec']['containers'][0]['env'][0]['value']=='v2'
print('PASS: final Git desired state has two ready replicas / v2')
logs=subprocess.check_output(['kubectl','--context','devops-assignment','logs','-n','session20','-l','app=session20-mini','--tail=100']).decode()
assert 'session20-final-verify' in logs
print('PASS: matching correlation ID in real Kubernetes logs')
print('ALL 10 LIVE CHECKS PASSED')
