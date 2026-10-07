import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from app.calculator import add, subtract, multiply, divide

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        try:
            if url.path == "/health":
                payload = {"status": "ok"}
            elif url.path == "/calculate":
                query = parse_qs(url.query)
                operations = {"add": add, "subtract": subtract, "multiply": multiply, "divide": divide}
                payload = {"result": operations[query["op"][0]](float(query["a"][0]), float(query["b"][0]))}
            else:
                self.send_error(404)
                return
        except (KeyError, ValueError) as error:
            self.send_error(400, str(error))
            return
        data = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
