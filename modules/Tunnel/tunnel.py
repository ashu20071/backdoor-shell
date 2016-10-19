import requests;

def get(url):
	if "http://" not in url:
		url = "http://"+url;
	resp = requests.get(url);
	return(resp.content);
