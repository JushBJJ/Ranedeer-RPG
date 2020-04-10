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

def get_c(buffer):
	whitelisted_keys={
        b"H": 0, b"P": 1, b"K": 2, b"M": 3, 
        b"w": 0, b"s": 1, b"a": 2, b"d": 3
    }

	whitelisted_keys_linux={
		65:0, 66:1, 68:2, 67:3,
		119:0, 115:1, 97:2, 100:3
	}

	other_controls={
		ord("e"):4, ord("i"):5, ord("c"):6, ord("q"):7
	}

	getchx=get_key()
	while True:
		x=getchx()

		if sys.platform=="win32":
			if x==b"\x00":
				x=getchx()
				if x in whitelisted_keys.keys():
					return whitelisted_keys[x]
			else:
				if x in whitelisted_keys.keys():
					return whitelisted_keys[x]

		elif sys.platform=="linux":
			x=ord(x)
			if x==27:
				x=ord(getchx())
				if x==91:
					x=ord(getchx())

					if x in whitelisted_keys_linux.keys():
						return whitelisted_keys_linux[x]

			elif x in whitelisted_keys_linux.keys():
				return whitelisted_keys_linux[x]

		if sys.platform=="linux" or sys.platform=="win32":
			x=ord(x) if type(x)!=int else x

			if x in other_controls.keys():
				return other_controls[x]