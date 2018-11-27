#!/usr/bin/python3

import socket
import sys
import threading

clients_list = []

def lis(client_socket,addr,opt_b):
	while True:
		data = client_socket.recv(2048).decode()
		if not data:
			break
		elif opt_b == True:
			print(data)
			for client in clients_list:
				client.send(data.encode())
		else:
			print(data)
			client_socket.send(data.encode())

	print("***",addr,"disconnected***")
	clients_list.remove(client_socket)
	client_socket.close()

def start_server(server_socket,opt_b):
	print("+++ Hello, Server +++")
	print("+++ Press Ctrl-C to close server +++")
	try:
		while True:
			print("listening for connection")
			(client_socket,addr) = server_socket.accept()
			clients_list.append(client_socket)
			print("***",addr,"connected ***")
			t = threading.Thread(target = lis, args = (client_socket,addr,opt_b))
			t.start()

	except KeyboardInterrupt:
		print("\n--- Server Closed ---")
		for client in clients_list:
			client.send("terminate".encode())
			client.close()

		server_socket.close()
		sys.exit(1)


def main():
	opt_b = False
	if len(sys.argv) == 3 and sys.argv[2] == '-b':
		opt_b = True
	elif len(sys.argv) != 2:
		print("*** Syntax Error ***")
		print("Syntax: echoserver <port>")
		print("Sample: echoserver 8080")
		sys.exit(1)

	port = int(sys.argv[1])

	server_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind(('127.0.0.1',port))
	server_socket.listen(5)

	start_server(server_socket,opt_b)

	server_socket.close()

if __name__ == '__main__':
	main()


	



