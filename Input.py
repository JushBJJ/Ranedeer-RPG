import sys
from Map import clear_screen

class get_key:
	def __init__(self):
		OS=sys.platform

		if OS=="linux":
			self.call=get_key_linux()
		elif OS=="win32":
			self.call=get_key_windows()

	def __call__(self):
		return self.call()

class get_key_linux:
	def __init__(self):
		import tty
		import termios
		
	def __call__(self):
		import tty
		import termios

		fd=sys.stdin.fileno()
		current=termios.tcgetattr(fd)

		try:
			tty.setraw(sys.stdin.fileno())
			ch=sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, current)
		
		return ch

class get_key_windows:
	def __init__(self):
		import msvcrt
	
	def __call__(self):
		import msvcrt
		return msvcrt.getch()

def get_arrow_key(buffer):
	whitelisted_keys={
        b"H": 0, b"P": 1, b"K": 2, b"M": 3, 
        b"w": 0, b"s": 1, b"a": 2, b"d": 3
    }

	whitelisted_keys_linux={
		65:0, 66:1, 68:2, 67:3,
		119:0, 115:1, 97:2, 100:3
	}

	getchx=get_key()
	buffer.clear()

	while True:
		x=getchx()
		
		if sys.platform=="win32":
			if x==b"\x00":
				x=getchx()
				if x in whitelisted_keys.keys():
					buffer.bottom_write(f"Key: {x}")
					return whitelisted_keys[x]
			else:
				
				
				if x in whitelisted_keys.keys():
					buffer.bottom_write(f"Key: {x}")
					return whitelisted_keys[x]

				elif x==b"q":
					clear_screen()
					exit()

		elif sys.platform=="linux":
			x=ord(x)
			if x==27:
				x=ord(getchx())
				if x==91:
					x=ord(getchx())

					if x in whitelisted_keys_linux.keys():
						buffer.bottom_write(f"Key: {x}")
						return whitelisted_keys_linux[x]

			elif x in whitelisted_keys_linux.keys():
				buffer.bottom_write(f"Key: {x}")
				return whitelisted_keys_linux[x]
			elif x==113:
				clear_screen()
				exit()

            
