
## **基于树莓派的Socket和串口通讯程序**
---
*中文版*

---

### **简介**

本项目由服务端和客户端两部分组成，服务端运行于树莓派上，并且服务端和客户端需在同一局域网内。树莓派外接一块12864显示屏。服务端运行时，可以通过Socket从客户端获取数据，并且通过串口显示在12864显示屏上。服务端和客户端均由Python语言实现。

---
### **服务端**

服务端具有两大主要功能：通过Socket与客户端交换信息，通过串口向12864显示器写入数据。

#### **Socket部分**

* 导入socketserve和socket模块实现功能
* 定义一个继承自socketserver.BaseRequestHandler的类来响应socket请求，利用其中的handle()函数来响应
* 使用recv()函数和sendall()函数来收发数据,使用server.shutdown()和request.close()来关闭服务器
* 使用socketserver.ThreadingTCPServer()和serve_forever()函数实现并发处理客户端请求

#### **串口部分**

* 串口上连接了一块128*64的OLED显示屏，该显示器内置SSD1306驱动，并且包含GND、VCC、SCL和SDA四个引脚，分别对应树莓派的09、01、05、03引脚
* 导入Adafruit_GPIO.SPI和Adafruit_SSD1306两个模块来控制12864显示屏
* 导入PIL中的部分库，来生成需要现实内容的图片形式

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

客户端主要负责向服务端发送请求，接收并打印来自服务端的回复。

#### **Socket部分**

* 导入socket模块实现功能
* 使用recv()函数和sendall()函数来收发数据


#### **特点**

由于服务端的IP可能变化，程序利用os.popen()来执行 “arp -a”命令，分析回显的数据，通过不发生变化的树莓派MAC地址来查找服务端IP。
```python
def get_ip_by_mac(target_mac):
	for line in os.popen("arp -a"):
		if not line.startswith("  192.168"):
			continue
		ip = line[2:17]
		mac = line[24:41]
		if mac == target_mac:
			return ip
	return""
```

