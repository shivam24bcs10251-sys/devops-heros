"""Exercise the real PostgreSQL-backed app. Creates labeled synthetic records."""
import argparse,json,uuid,urllib.request,urllib.error
from concurrent.futures import ThreadPoolExecutor
p=argparse.ArgumentParser();p.add_argument('--base',default='http://127.0.0.1:3021');p.add_argument('--version');args=p.parse_args()
def call(method,path,data=None):
    request=urllib.request.Request(args.base+path,method=method,data=None if data is None else json.dumps(data).encode(),headers={'Content-Type':'application/json','X-Request-ID':'labledger-live-verify'})
    try:
        with urllib.request.urlopen(request,timeout=15) as response: return response.status,json.load(response) if response.status!=204 else None
    except urllib.error.HTTPError as error:return error.code,json.load(error)
code,health=call('GET','/health');assert code==200 and health['status']=='UP'
if args.version:assert health['version']==args.version,health
assert call('GET','/ready')[0]==200
print('PASS health, expected release and PostgreSQL readiness')
tag='VERIFY-'+uuid.uuid4().hex[:8].upper()
code,asset=call('POST','/api/assets',{'asset_tag':tag,'name':'Verification equipment','category':'Tools','total':3});assert code==201,asset
id=asset['id'];path=f'/api/assets/{id}'
assert call('GET',path)[1]['available']==3
assert call('PUT',path,{'name':'Verified equipment'})[1]['name']=='Verified equipment'
print('PASS create, read and edit inventory')
code,loan=call('POST','/api/loans',{'asset_id':id,'borrower':'Synthetic verification','quantity':2});assert code==201
assert call('GET',path)[1]['available']==1
assert call('POST','/api/loans',{'asset_id':id,'borrower':'Synthetic overflow','quantity':2})[0]==409
assert call('PUT',path,{'total':1})[0]==409
print('PASS checkout decrements stock; insufficient stock and unsafe edits return 409')
assert call('PUT',f'/api/loans/{loan["id"]}/return')[0]==200
assert call('PUT',f'/api/loans/{loan["id"]}/return')[0]==409
assert call('GET',path)[1]['available']==3
assert call('DELETE',path)[0]==409
print('PASS return restores stock once; lending history is retained')
code,one=call('POST','/api/assets',{'asset_tag':tag+'-ONE','name':'Concurrent checkout test','category':'Tools','total':1});assert code==201
with ThreadPoolExecutor(max_workers=2) as pool:
    results=list(pool.map(lambda borrower:call('POST','/api/loans',{'asset_id':one['id'],'borrower':borrower}),['Synthetic A','Synthetic B']))
assert sorted(r[0] for r in results)==[201,409],results
assert call('GET',f'/api/assets/{one["id"]}')[1]['available']==0
winner=next(r[1] for r in results if r[0]==201)
assert call('PUT',f'/api/loans/{winner["id"]}/return')[0]==200
print('PASS concurrent PostgreSQL checkouts cannot oversubscribe a single unit')
code,temporary=call('POST','/api/assets',{'asset_tag':tag+'-TEMP','name':'Disposable verification','category':'Tools','total':1});assert code==201
assert call('DELETE',f'/api/assets/{temporary["id"]}')[0]==204
assert call('GET',f'/api/assets/{temporary["id"]}')[0]==404
print('PASS delete unused inventory and missing-record behavior')
assert call('GET','/api/stats')[0]==200 and call('GET','/api/loans')[0]==200
print('ALL LIVE BUSINESS CHECKS PASSED')
