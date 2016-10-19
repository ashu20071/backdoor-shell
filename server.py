#!/usr/bin/python3

ADDRESS = "";
PORT = 1337;

import http.server as hs;
from modules.Tunnel import tunnel;
from urllib.parse import urlparse;
import json;

class CustomRequestHandler(hs.BaseHTTPRequestHandler):

	def do_GET(self):
		print("\n\n");
		self.send_response(200);
		self.send_header("Content-Type","text/JSON");
		self.send_header("Content-Encoding","ASCII");
		self.end_headers();

		#stuff goes here
		#headers = self.headers;
		#print(headers);
		#print(self.content);
		data = self.rfile.read(int(self.headers["content-length"]));
		data = str(data).strip("b'").strip("'");
		data = json.loads(data);
		
		res = self.execute(data);
		
		#self.wfile.write(b"GET-ed Successfully!");
		self.wfile.write(res);
		return;

	def execute(self,data):
		print("GOT ",data);
		action = data["action"];
		value = data["value"];
		
		if action == "tunnel":
			return(tunnel.get(value));
		

	def do_POST(self):
		self.send_response(200);
		self.send_header("Content-Type","text/JSON");
		self.send_header("Content-Encoding","ASCII");
		self.wfile.write(b"POST-ed Successfully!");
		return;

if __name__ == "__main__":
	server_addr = (ADDRESS,PORT);
	request_handler = CustomRequestHandler;
	http_daemon = hs.HTTPServer(server_addr,request_handler);

	try:
		print("Starting server on port "+str(PORT));
		http_daemon.serve_forever();
	except KeyboardInterrupt:
		print("\n\nKilling Server...");
		exit();
