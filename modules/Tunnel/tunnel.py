import requests;
import os;

'''
FORMAT:
	- action: "tunnel"
	- sub-action: "get"|"post"|"session"|"login_session"
'''

class Tunnel:
	
	def __init__(self,url=None):
		self.url="https://www.google.com";
		self.session = None; #to be a requests.session object
		return;
		
	def get(self,url=None):
		if url == None:
			url=self.url;
		resp=None;
		try:
			resp = requests.get(url);
		except requests.exceptions.SSLError:
			resp = requests.get(url,verify=False);
		return(resp.content); 
		
	def post(self,url=None):
		if url == None:
			url=self.url;
		resp=None;
		try:
			resp = requests.post(url);
		except requests.exceptions.SSLError:
			resp = requests.post(url,verify=False);
		return(resp.content);
		
	def session(self,url=None):
		if url == None:
			url = self.url;
		if self.session == None:
			return(self.start_session(url).content);
		else:
			ret = None;
			try:
				ret = self.session.get(url).content;
			except requests.exceptions.SSLError:
				ret = self.session.get(url,verify=False).content;
			return(ret);
		
	def login_session(self,url=None,data=None):
		if url == None:
			url = self.url;
		if self.session == None:
			return(self.start_session(url,data).content);
		else:
			ret = None;
			try:
				ret = self.session.get(url).content;
			except requests.exceptions.SSLError:
				ret = self.session.get(url,verify=False).content;
			return(ret);
	
	''' supplementary methods '''
	
	def start_session(self,url,data=None):
		self.session = requests.Session();
		ret = None; #returning data
		if data != None:
			try:
				ret = self.session.post(url,data=data);
			except requests.exceptions.SSLError:
				ret = self.session.post(url,data=data,verify=False);
		else:
			try:
				ret = self.session.get(url);
			except requests.exceptions.SSLError:
				ret = self.session.get(url);
		return(ret);
	

''' MAIN '''
if __name__ == "__main__":
	t = Tunnel("http://moodle.dbit.in");
	t.get();
	data = t.login_session("https://moodle.dbit.in/login/index.php",{"username":"213uzair3413","password":"aaaaa"});
	f = open("op.html","wb");
	f.write(data);
	f.close();
	os.system("xdg-open op.html 1> /dev/null");
