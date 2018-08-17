import  socketserver
import socket

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

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
		# Raspberry Pi pin configuration:
		RST = None     # on the PiOLED this pin isnt used
		# Note the following are only used with SPI:
		DC = 23
		SPI_PORT = 0
		SPI_DEVICE = 0
		# 128x64 display with hardware I2C:
		disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
		# Initialize library.
		disp.begin()
		# Clear display.
		disp.clear()
		disp.display()

		# Create blank image for drawing.
		# Make sure to create image with mode '1' for 1-bit color.
		width = disp.width
		height = disp.height
		image = Image.new('1', (width, height))

		# Get drawing object to draw on image.
		draw = ImageDraw.Draw(image)
		# Draw a black filled box to clear the image.
		draw.rectangle((0,0,width,height), outline=0, fill=0)

		# Draw some shapes.
		# First define some constants to allow easy resizing of shapes.
		padding = -2
		top = padding
		bottom = height-padding
		# Move left to right keeping track of the current x position for drawing shapes.
		x = 0

		# Load default font.
		font = ImageFont.load_default()
		
		
		global host_ip
		conn = self.request
		conn.sendall(bytes("From"+host_ip+":Connected successfully.",encoding="utf-8"))
		print(self.client_address[0]+":"+str(self.client_address[1])+" is connected.")
		while True:
			ret_bytes = conn.recv(1024)
			ret_str = str(ret_bytes,encoding="utf-8")
			if ret_str == "quit":
				print(self.client_address[0]+":"+str(self.client_address[1])+" is disconnected.")
				break
			elif ret_str == "stop":
				self.server.shutdown()
				self.request.close()
				break
			elif ret_str == "help":
				conn.sendall(bytes("quit:disconnecte with host\nstop:turn off the server",encoding="utf-8"))
			elif ret_str == "display":
				# Draw a black filled box to clear the image.
				draw.rectangle((0,0,width,height), outline=0, fill=0)
				
				draw.text((x, top),"Hello,world",  font=font, fill=255)
				# Display image.
				disp.image(image)
				disp.display()
				conn.sendall(bytes("ok",encoding="utf-8"))
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
		server.serve_forever()
	except Exception as e:
		print('except:', e)