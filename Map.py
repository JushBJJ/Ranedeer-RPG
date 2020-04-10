import numpy as np
import sys
import subprocess
import Position

"""
ID 0: Nothing
ID 1: Border Block
ID 2: Player
"""

def clear_screen():
    OS=sys.platform
    subprocess.run("cls" if OS=="win32" else "clear", shell=True)
    Position.pos(1,1)

class Buffer:
    def __init__(self, cursor, F=sys.stdout):
        self.buffer=F
        self.buffer_X="\r"
        self.cursor=cursor
    
    def write(self, x):
        self.buffer.write(x)
        self.buffer.flush()

    def clear(self):
        self.buffer_X="\r"

    def bottom_write(self, msg):
        self.buffer_X+="\n"+msg
        self.cursor.save_pos("last_pos")
        self.cursor.load_pos("bottom")

        self.write(self.buffer_X+(" "*3))
        self.flush()

        self.cursor.load_pos("last_pos")

    def flush(self):
        self.buffer.flush()

class Map:
    def __init__(self, cursor, buffer):
        self.max_x=50
        self.max_y=20

        # Map Array is in Y,X order
        self.current_map=np.zeros((self.max_y+1, self.max_x+1), dtype=np.int)
        self.objects={" ":0, "#": 1, "P": 2}
        self.cursor=cursor
        self.buffer=buffer
    
    def place_object(self, x, y, id):
        if id not in self.objects.values():
            self.buffer.bottom_write(f"Invaild ID: {id}")
        elif x<self.max_x or y<self.max_y:
            self.cursor.pos(x,y)
            self.buffer.write(self.object_key(id))
            self.current_map[y][x]=id
        else:
            self.buffer.bottom_write(f"Position out of range.\nX: {x}\t Y: {y}\nMax X: {self.max_x}\tMax Y: {self.max_y}")

    def check_position(self, x, y):
        return self.current_map[y][x]

    def remove_object(self, x, y):
        if x<self.max_x or y<self.max_y:
            self.place_object(x,y, 0)
        else:
            self.buffer.bottom_write(f"Position out of range.\nX: {x}\t Y: {y}\nMax X: {self.max_x}\tMax Y: {self.max_y}")

    def generate_map(self):
        # Generate Border
        x=self.current_map

        for y in range(1,self.max_y):
            if y==self.max_y-1:
                break

            x[y][1]=1
            x[y][self.max_x-1]=1

        x[0:][1]=1
        x[0:][self.max_y-1]=1

        x[0:][1][0]=0
        x[0:][1][self.max_x]=0

        x[0:][self.max_y-1][0]=0
        x[0:][self.max_y-1][self.max_x]=0
        
    def object_key(self, id):
        if id not in self.objects.values():
            self.buffer.bottom_write("Unable to return key value of id ", id)
            return " "
        return list(self.objects.keys())[list(self.objects.values()).index(id)]

    def draw_map(self):
        self.cursor.pos(1,1)
        for y in range(self.max_y):
            for x in range(self.max_x):
                self.cursor.pos(x,y)
                self.buffer.write(self.object_key(self.current_map[y][x]))
        
        self.cursor.pos(1, self.max_y)
        self.cursor.save_pos("bottom")