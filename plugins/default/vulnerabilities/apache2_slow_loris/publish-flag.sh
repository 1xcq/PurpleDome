import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHTTPHandler(BaseHTTPRequestHandler):
    def check_apache(self):
        try:
            r = requests.get("http://127.0.0.1", timeout=3)
            return True
        except Exception as e:
            print(e)
            return False

    def do_GET(self):
        flag = self.check_apache() and "____" or "flag{123456}"
        print(flag)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Flag Publishing Service</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes(f"<p>The Flag is: {flag}</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer(('0.0.0.0', 8080), SimpleHTTPHandler)
    print("Server started.")
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

