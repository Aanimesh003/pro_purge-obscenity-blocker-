import http.server
import socketserver


class DummyHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        response = "This is a dummy response from the server!"  # Response on dummy server
        self.wfile.write(response.encode())

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        response = "Notification received!"
        self.wfile.write(response.encode())

def run_server():
       PORT = 8000
       with socketserver.TCPServer(("", PORT), DummyHandler) as httpd:
           print(f"Serving at port {PORT}")
           httpd.serve_forever()


if __name__ == "__main__":
    run_server()
