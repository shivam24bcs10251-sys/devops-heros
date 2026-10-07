import json, os, resource, time, uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
VERSION = os.getenv('APP_VERSION', 'v1')
POD = os.getenv('HOSTNAME', 'unknown')
requests = 0
healthy = True
class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args): pass
    def do_GET(self):
        global requests, healthy
        start = time.monotonic()
        path = urlparse(self.path).path
        trace = self.headers.get('X-Trace-ID', uuid.uuid4().hex)
        status = 200
        if path == '/metrics':
            usage = resource.getrusage(resource.RUSAGE_SELF)
            rss = int(Path('/proc/self/statm').read_text().split()[1]) * os.sysconf('SC_PAGE_SIZE')
            values = {'demo_requests_total': ('counter',requests),
                      'process_cpu_seconds_total': ('counter', usage.ru_utime + usage.ru_stime),
                      'process_resident_memory_bytes': ('gauge',rss),
                      'demo_dependency_healthy': ('gauge',int(healthy))}
            body = ''.join(f'# TYPE {key} {kind}\n{key} {value}\n' for key,(kind,value) in values.items()).encode()
            content_type = 'text/plain; version=0.0.4'
        else:
            requests += 1
            if path == '/demo/fail': healthy = False
            elif path == '/demo/recover': healthy = True
            elif path == '/work':
                until = time.monotonic() + 0.25
                while time.monotonic() < until: sum(i*i for i in range(500))
            elif path not in ['/', '/health']: status = 404
            if path == '/health' and not healthy: status = 503
            body = json.dumps({'session':20,'version':VERSION,'pod':POD,'healthy':healthy,'trace_id':trace}).encode()
            content_type = 'application/json'
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('X-Trace-ID',trace)
        self.end_headers(); self.wfile.write(body)
        if path != '/metrics':
            print(json.dumps({'event':'http_request','path':path,'status':status,'version':VERSION,
                              'pod':POD,'trace_id':trace,'duration_ms':round((time.monotonic()-start)*1000,3)}),flush=True)
from pathlib import Path
print(json.dumps({'event':'startup','session':20,'version':VERSION,'pod':POD}),flush=True)
ThreadingHTTPServer(('0.0.0.0',8080), Handler).serve_forever()
