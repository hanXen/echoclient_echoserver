#!/usr/bin/python3

import socket
import sys
import os
import threading
import time

def check_receive(client_socket):
	while True:
		try:
			data = client_socket.recv(2048)
			if not data:
				break
			elif data.decode() == "terminate":
				break
			print("*** received from server ***")
			print(data.decode())
			print("Input Request >> ")
		except:
			pass

	print("--- Server closed. Sorry :( ---")
	client_socket.close()
	os._exit(1)

def start_client(client_socket ,addr):
	print("+++ Hello, Client +++")
	print('+++ Press Ctrl-C or Enter "exit plz" to exit program +++')
	print("***",addr, "connected ***")

	try:
		t = threading.Thread(target = check_receive, args = (client_socket,))
		t.daemon = True
		t.start()
		print("Input Request >> ")
		while True:
			data = input()
			client_socket.send(data.encode())
			if(data == "exit plz"):
				break
			time.sleep(0.1)		

	except KeyboardInterrupt:
		pass

	finally:
		print("\n***", addr, "disconnected ***")
		client_socket.close()
		sys.exit(0)

def main():
	if len(sys.argv) != 3:
		print("*** Syntax Error ***")
		print("Syntax: echoclient <host> <port>")
		print("Sample: echoclient 127.0.0.1 6969")
		sys.exit(1)
	host = sys.argv[1]
	port = int(sys.argv[2])
	addr = (host,port)
	try:
		client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		client_socket.connect(addr)
	except Exception as e:
		print("*** Failed to connect ***")
		print(e)
		sys.exit(1)

	start_client(client_socket , addr)

if __name__=='__main__':
	main()
