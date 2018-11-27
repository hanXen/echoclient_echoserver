import socket
import sys
import os
import threading
import time


def receive(client_socket):
	while True:
		try:
			data = client_socket.recv(2048)
			if not data:
				break
			elif data.decode() == "terminate":
				break
			print("***received from server***")
			print(data.decode())
			print("Input Request >> ")
		except:
			pass

	print("---Server closed. Sorry :(---")
	client_socket.close()
	os._exit(1)


def client(client_socket):
	try:
		t = threading.Thread(target = receive, args = (client_socket,))
		t.daemon = True
		t.start()
		print("Input Request >> ")
		while True:
			data = input()
			client_socket.send(data.encode())
			if(data == "/exit"):
				break
			time.sleep(0.1)		
	except :
		pass

	finally:
		print("***disconnected***")
		client_socket.close()
		sys.exit(0)


def main():
	if len(sys.argv) != 3:
		print("***Syntax Error***")
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
		print("***Failed to connect***")
		print(e)
		sys.exit(1)

	client(client_socket)


if __name__=='__main__':
	main()
