from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from dateutil import parser
import datetime

hostName = "localhost"
serverPort = 9123

def read_file(filename):
	f = open(filename, "r")
	t = f.read()
	f.close()
	return t

def write_file(filename, content):
	f = open(filename, "w")
	f.write(content)
	f.close()

def get(path):
	if path == "/":
		return {
			"status": 200,
			"headers": {
				"Content-Type": "application/json"
			},
			"content": read_file("commits.json")
		}
	else:
		return {
			"status": 404,
			"headers": {
				"Content-Type": "text/html"
			},
			"content": f"<html><head><title>Task Manager</title></head>\n<body>\n\
<h1>Not Found</h1><p><a href='/' style='color: rgb(0, 0, 238);'>Return home</a></p>\
\n</body></html>"
		}

def post(path, body):
	if path == "/write":
		try:
			c = json.dumps(json.loads(body), sort_keys=True, indent=4).replace("    ", "\t")
			write_file("commits.json", c)
			return {
				"status": 200,
				"headers": {},
				"content": ""
			}
		except:
			return {
				"status": 400,
				"headers": {
					"Content-Type": "text/plain"
				},
				"content": "Malformed request"
			}
	else:
		return {
			"status": 404,
			"headers": {
				"Content-Type": "text/html"
			},
			"content": f"<html><head><title>Task Manager</title></head>\n<body>\n\
<h1>Not Found</h1><p><a href='/' style='color: rgb(0, 0, 238);'>Return home</a></p>\
\n</body></html>"
		}

class MyServer(BaseHTTPRequestHandler):
	def do_GET(self):
		res = get(self.path)
		self.send_response(res["status"])
		for h in res["headers"]:
			self.send_header(h, res["headers"][h])
		self.end_headers()
		self.wfile.write(res["content"].encode("utf-8"))
	def do_POST(self):
		body_len = int(self.headers.get('Content-Length'))
		body = self.rfile.read(body_len).decode("utf-8")
		res = post(self.path, body)
		self.send_response(res["status"])
		for h in res["headers"]:
			self.send_header(h, res["headers"][h])
		self.end_headers()
		self.wfile.write(res["content"].encode("utf-8"))
	def log_message(self, format: str, *args) -> None:
		print(args[0].split(" ")[0], "request to", args[0].split(" ")[1], "(status code:", args[1] + ")")
		# don't output requests

if __name__ == "__main__":
	webServer = HTTPServer((hostName, serverPort), MyServer)
	print("Server started http://%s:%s" % (hostName, serverPort))
	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		pass
	webServer.server_close()
	print("Server stopped.")
