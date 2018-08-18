import socket
import os

obj = socket.socket()
mac_addr = "b8-27-eb-65-81-a4"#我的树莓派的mac地址

def get_ip_by_mac(target_mac):
	for line in os.popen("arp -a"):
		if not line.startswith("  192.168"):
			continue
		ip = line[2:17]#2~17
		mac = line[24:41]#24~41
		if mac == target_mac:
			return ip
	return""
			
			
host_ip = get_ip_by_mac(mac_addr)
if not host_ip.startswith("192.168"):
	host_ip = input("Fail to get the host's IP. Please input the correct IP:")


try:
	obj.connect((host_ip,8080))
except Exception as e:
	print("Fail to connect with the host. Please check the host.")
	print("except:",e)
	exit()

ret_bytes = obj.recv(1024)
ret_str = str(ret_bytes,encoding="utf-8")
print(ret_str)

while True:
	inp = input(">>>")
	obj.sendall(bytes(inp,encoding="utf-8"))
	if inp == "quit":
		break
	elif inp =="stop":
		break
	elif inp.startswith("display"):
		if not (inp.startswith("display -m") or inp.startswith("display -i")):
			ret_bytes = obj.recv(1024)
			ret_str = str(ret_bytes,encoding="utf-8")
			print(ret_str)
	else:
		ret_bytes = obj.recv(1024)
		ret_str = str(ret_bytes,encoding="utf-8")
		print(ret_str)