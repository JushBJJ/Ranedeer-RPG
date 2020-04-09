from msvcrt import getch
from Map import clear_screen

def get_arrow_key(buffer):
    whitelisted_keys={
        b"H": 0, b"P": 1, b"K": 2, b"M": 3, 
        b"w": 0, b"s": 1, b"a": 2, b"d": 3
    }

    while True:
        x=getch()

        if x==b"\x00":
            x=getch()

            buffer.clear()
            buffer.bottom_write(f"Key: {x}")
            
            if x in whitelisted_keys.keys():
                return whitelisted_keys[x]
        else:
            buffer.clear()
            buffer.bottom_write(f"Key: {x}")
            
            if x in whitelisted_keys.keys():
                return whitelisted_keys[x]
            if x==b"q":
                clear_screen()
                exit()
            