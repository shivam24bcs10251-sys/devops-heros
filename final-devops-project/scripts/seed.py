"""Create clearly synthetic presentation inventory; idempotent by asset tag."""
import json,sys,urllib.request
base=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:3021'
def get(path):return json.load(urllib.request.urlopen(base+path))
def post(path,data):
    request=urllib.request.Request(base+path,data=json.dumps(data).encode(),headers={'Content-Type':'application/json'})
    return json.load(urllib.request.urlopen(request))
assets=get('/api/assets');tags={a['asset_tag'] for a in assets}
items=[('LAB-001','Arduino starter kit','Electronics',6,'Board, sensors & USB cable'),('LAB-002','Sony mirrorless camera','Media',3,'Camera body & 24–70 mm lens'),('LAB-003','Digital multimeter','Electronics',8,'Probes & protective case'),('LAB-004','Precision tool set','Tools',5,'32-piece electronics toolkit'),('LAB-005','Raspberry Pi 5','Computing',4,'8 GB board & power supply')]
for tag,name,category,total,description in items:
 if tag not in tags:post('/api/assets',dict(asset_tag=tag,name=name,category=category,total=total,description=description))
assets=get('/api/assets');loans=get('/api/loans')
for tag,borrower,quantity in [('LAB-001','Aarav · Demo borrower',2),('LAB-002','Meera · Demo borrower',1),('LAB-005','Kabir · Demo borrower',1)]:
 asset=next(a for a in assets if a['asset_tag']==tag)
 if not any(l['asset_id']==asset['id'] and l['borrower']==borrower for l in loans):post('/api/loans',dict(asset_id=asset['id'],borrower=borrower,quantity=quantity))
print('Five presentation assets and three synthetic checkouts ready')
