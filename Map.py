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

        self.buffers={}
    
    def save_buffer_line(self, x, y):
        buffers_n=len(self.buffers)
        next_line=str(buffers_n)

        self.cursor.pos(x,y)
        self.cursor.save_pos(next_line)
        self.buffers[next_line]=""

    def clear_buffer_line(self, line):
        line=str(line)
        self.cursor.load_pos(line)

        for i in self.buffers[line]:
            self.write(" "*2)

        self.buffers[line]=""

    def write_buffer_line(self, line, msg):
        self.clear_buffer_line(line)
        self.buffers[str(line)]=msg

        self.cursor.load_pos(str(line))
        self.write(msg)

    def write(self, x):
        self.buffer.write(x)
        self.buffer.flush()

    def flush(self):
        self.buffer.flush()

class interactable_objects:
    def __init__(self):
        self.interactables={3:self.wooden_sword, 4:self.NPC}

    def wooden_sword(self):
        # 1=True
        # 0=False

        wooden_sword_details={
            "Weapon":1,
            "Equipable":1,
            "Consumeable":0,
            "Damage":10,
            "Breakable":1,
            "till_break":30,
            "Name":"Wooden Sword"
        }

        return True, wooden_sword_details
    
    def NPC(self):
        # TODO
        return False, None
    
class Map:
    def __init__(self, cursor, buffer):
        self.max_x=50
        self.max_y=20

        # Map Array is in Y,X order
        # Maximum of 87 objects

        self.current_map=np.zeros((self.max_y+1, self.max_x+1), dtype=np.int)
        
        self.objects={" ":0, "#": 1, "P": 2, "S": 3, "N": 4}
        self.interactables={"Wooden_Sword":3, "NPC":4}
        self.non_solid={0, 3}

        self.cursor=cursor
        self.buffer=buffer

        self.items=interactable_objects()
    
    def interact(self, x,y):
        z=check_position(x,y)
        if z in self.items.keys():
            return self.items.interactables[z]()

    def place_object(self, x, y, id):
        if id not in self.objects.values():
            self.buffer.write_buffer_line(0, f"Invaild ID: {id}")
        elif x<self.max_x or y<self.max_y:
            self.cursor.pos(x,y)
            self.buffer.write(self.object_key(id))
            self.current_map[y][x]=id
        else:
            self.buffer.write_buffer_line(0, f"Position out of range.\nX: {x}\t Y: {y}\nMax X: {self.max_x}\tMax Y: {self.max_y}")

    def check_position(self, x, y):
        return self.current_map[y][x]

    def remove_object(self, x, y):
        if x<self.max_x or y<self.max_y:
            self.place_object(x,y, 0)
        else:
            self.buffer.write_buffer_line(0, f"Position out of range.\nX: {x}\t Y: {y}\nMax X: {self.max_x}\tMax Y: {self.max_y}")

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
            self.buffer.write_buffer_line(0, "Unable to return key value of id ", id)
            return " "
        return list(self.objects.keys())[list(self.objects.values()).index(id)]

    def draw_map(self):
        clear_screen()
        self.cursor.pos(1,1)
        for y in range(self.max_y):
            for x in range(self.max_x):
                self.cursor.pos(x,y)
                self.buffer.write(self.object_key(self.current_map[y][x]))
        
        self.cursor.pos(1, self.max_y)
        self.buffer.save_buffer_line(self.cursor.x, self.cursor.y)

        self.cursor.pos(1, self.max_y+1)
        self.buffer.save_buffer_line(self.cursor.x, self.cursor.y)