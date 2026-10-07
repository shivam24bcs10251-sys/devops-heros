"""Bounded, read-only HTTP traffic for the lab HPA demonstration."""
import argparse, concurrent.futures, json, threading, time, urllib.request
p=argparse.ArgumentParser();p.add_argument('--base',default='http://labledger.localhost:8086');p.add_argument('--seconds',type=int,default=90);p.add_argument('--workers',type=int,default=8);p.add_argument('--interval',type=float,default=0.05);a=p.parse_args()
if not 1<=a.seconds<=300 or not 1<=a.workers<=64 or not 0<=a.interval<=5:p.error('seconds must be 1..300, workers 1..64 and interval 0..5')
end=time.monotonic()+a.seconds;lock=threading.Lock();counts={'ok':0,'errors':0}
def worker():
 while time.monotonic()<end:
  try:
   with urllib.request.urlopen(a.base.rstrip('/')+'/api/assets',timeout=5) as r:r.read();key='ok' if r.status==200 else 'errors'
  except Exception:key='errors'
  with lock:counts[key]+=1
  time.sleep(a.interval)
print(f'Read-only inventory traffic: {a.workers} workers for {a.seconds}s',flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:list(pool.map(lambda _:worker(),range(a.workers)))
print(json.dumps({**counts,'seconds':a.seconds,'workers':a.workers}),flush=True)
