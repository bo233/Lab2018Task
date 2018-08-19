c
*中文版*

---

### **简介**

本项目由服务端和客户端两部分组成，服务端运行于树莓派上，并且服务端和客户端需在同一局域网内。树莓派外接一块12864显示屏。服务端运行时，可以通过Socket从客户端获取数据，并且通过串口显示在12864显示屏上。服务端和客户端均由Python语言实现。

---
### **服务端**

服务端具有两大主要功能：通过Socket与客户端交换信息，通过串口向12864显示器写入数据。

#### **Socket部分**
* 使用socketserver模块实现功能
* 定义一个继承自socketserver.BaseRequestHandler的类来响应socket请求，利用其中的handle()函数来响应
* 使用recv()函数和sendall()函数来收发数据,使用server.shutdown()和request.close()来关闭服务器
* 使用socketserver.ThreadingTCPServer()和serve_forever()函数实现并发处理客户端请求

#### **串口部分**

#### **特点**
* 由于树莓派每次接入局域网所分配到的IP可能不同，程序中加入了能自动获取自身IP的功能。

```python
def get_host_ip():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 80))
		ip = s.getsockname()[0]
	finally:
		s.close()

	return ip
```
* 由于直接使用SocketServer.ThreadingTCPServer()会导致，每次关闭服务端程序后，地址会在几分钟内仍然保持占用状态，不便于服务端程序的调试，程序中定义了一个继承自socketserver.ThreadingTCPServer的类，并且将其中默认为False的allow_reuse_address值改为True，这样便解决了地址无法复用的问题。

```python
class EchoServer(socketserver.ThreadingTCPServer):
	allow_reuse_address = True
	daemon_threads = True
	def __init__(self, server_address, RequestHandlerClass):
		socketserver.ThreadingTCPServer.__init__(self, server_address, RequestHandlerClass)
```
---

### **客户端**