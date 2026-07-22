import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleProxy(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            req = urllib.request.Request(
                "https://ll.thespacedevs.com/2.2.0/launch/upcoming/?limit=1",
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req) as response:
                data = response.read()
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))

httpd = HTTPServer(('', 8080), SimpleProxy)
print("Starting transparent API proxy on port 8080...")
httpd.serve_forever()
