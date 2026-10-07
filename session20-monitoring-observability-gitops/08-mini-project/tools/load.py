"""Generate bounded CPU work against the local classroom demo."""
import time, urllib.request
until = time.monotonic() + 90
count = 0
while time.monotonic() < until:
    with urllib.request.urlopen('http://127.0.0.1:8084/work', timeout=5) as response:
        assert response.status == 200
        response.read()
    count += 1
print(f'Completed {count} real CPU-work requests over 90 seconds.')
