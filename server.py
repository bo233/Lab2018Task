import  socketserver
import socket

def get_host_ip():
	"""
	查询本机ip地址
	:return: ip
	"""
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 80))
		ip = s.getsockname()[0]
	finally:
		s.close()

	return ip

'''
def get_host_ip():
	#获取本机电脑名
	myname = socket.getfqdn(socket.gethostname(  ))
	#获取本机ip
	myaddr = socket.gethostbyname(myname)
	return myaddr
'''
	
host_ip = get_host_ip()
	
class Myserver(socketserver.BaseRequestHandler):

	def handle(self):
		global host_ip
		conn = self.request
		conn.sendall(bytes("From"+host_ip+":Connected successfully.",encoding="utf-8"))
		print(self.client_address[0]+":"+str(self.client_address[1])+" is connected.")
		while True:
			ret_bytes = conn.recv(1024)
			ret_str = str(ret_bytes,encoding="utf-8")
			if ret_str == "quit":
				print(self.client_address[0]+":"+str(self.client_address[1])+" is disconnected.")
				conn.sendall(bytes(" ",encoding="utf-8"))
				break
			elif ret_str == "stop":
				self.server.shutdown()
				self.request.close()
				conn.sendall(bytes(" ",encoding="utf-8"))
				break
			elif ret_str == "help":
				conn.sendall(bytes("quit:disconnecte with host\nstop:turn off the server",encoding="utf-8"))
			else:
				conn.sendall(bytes("Please input correct commends, type 'help' for details.",encoding="utf-8"))


#为了复用地址，自定义一个类以设置allow_reuse_address = True
class EchoServer(socketserver.ThreadingTCPServer):
	allow_reuse_address = True
	daemon_threads = True
	def __init__(self, server_address, RequestHandlerClass):
		socketserver.ThreadingTCPServer.__init__(self, server_address, RequestHandlerClass)
			
if __name__ == "__main__":
	try:
		server = EchoServer((host_ip,8080),Myserver)
		#server = socketserver.ThreadingTCPServer(('192.168.1.9',8080),Myserver)
		server.serve_forever()
	except Exception as e:
		print('except:', e)