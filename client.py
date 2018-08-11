import socket

obj = socket.socket()

obj.connect(("192.168.1.3",8080))
#obj.connect(("172.0.0.1",8080))

ret_bytes = obj.recv(1024)
ret_str = str(ret_bytes,encoding="utf-8")
print(ret_str)

while True:
	inp = input(">>>")
	if inp == "quit":
		obj.sendall(bytes(inp,encoding="utf-8"))
		break
	elif inp =="stop":
		obj.sendall(bytes(inp,encoding="utf-8"))
		break
	else:
		obj.sendall(bytes(inp, encoding="utf-8"))
		ret_bytes = obj.recv(1024)
		ret_str = str(ret_bytes,encoding="utf-8")
		print(ret_str)