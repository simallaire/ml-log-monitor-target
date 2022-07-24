import http.server as HTTPServer
import socketserver as SocketServer
import threading
import time
import os

hostName = "0.0.0.0"

serverPort = 8080
if "PORT" in os.environ:
    serverPort = int(os.environ["PORT"])

class SimpleHTTPRequestHandler(HTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(self.server.context, "utf-8"))


class MyServer():
    def __init__(self) -> None:
        self.server = ThreadingSimpleServer((hostName, serverPort), SimpleHTTPRequestHandler)
        self.thread = threading.Thread(target = self.server.serve_forever)
        self.thread.daemon = True
        self.server.context = ""
        self.thread.start()

    def write(self, data):
        self.server.context = str(data)

        
class ThreadingSimpleServer(SocketServer.ThreadingMixIn,HTTPServer.HTTPServer):
    pass

