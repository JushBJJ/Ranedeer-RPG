import numpy as np
import sys
import subprocess
import RPG_Position
import shutil
import random
import RPG_Buffer

def clear_screen():
    OS=sys.platform
    subprocess.run("cls" if OS=="win32" else "clear", shell=True)
    RPG_Position.pos(1,1)

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
        info=shutil.get_terminal_size()
    
        self.width=info.columns
        self.height=info.lines-2
        self.objects={" ":-1,".":0, "#": 1, "^": 2, "S": 3, "N": 4}

        self.floor=self.objects["."]
        self.borders=self.objects["#"]
        self.void=self.objects[" "]
        self.player_object=self.objects["^"]
        self.non_solid={self.objects["S"], self.floor}

        self.cursor=cursor
        self.buffer=buffer

        self.map=np.zeros((self.height-2, self.width-2), dtype=np.int)
        self.item_map=None

        self.old_map=None
        self.rooms={}
        self.items=interactable_objects()
        self.interactables=self.items.interactables

        self.generate_new_map()
    
    def generate_new_map(self):
        # Generate Borders
        self.map.fill(self.void)
        self.map=np.pad(self.map, (1,1), constant_values=self.void)
    
        # Generate Different rooms
        i=0
        for _ in range(300):
            if self.add_room(i):
                i+=1
        
        # Connect all rooms
        self.join_rooms()
        self.item_map=np.array(self.map)

        # TODO: AutoSpawn Items
        # TODO: Randomized Player spawn
        # TODO: Generate Town

    def add_room(self, id):
        i=0
        j=0

        room_width=random.randrange(4,6)
        room_height=random.randrange(6,10)

        room=np.zeros((room_height, room_width), dtype=np.int)
        room.fill(self.floor)
        room=np.pad(room, (1,1), constant_values=self.borders)

        room_x=random.randrange(1, self.width-room.shape[1])
        room_y=random.randrange(1, self.height-room.shape[0])

        if self.width-room.shape[1]-1<=0 or self.height-room.shape[1]-1<=0:
            return False

        for y in range(room_y, room_y+room.shape[0]):
            for x in range(room_x, room_x+room.shape[1]):
                if self.map[y][x]==self.floor:
                    return False

        for y in range(room_y, room_y+room.shape[0]):
            i=0
            for x in range(room_x, room_x+room.shape[1]):
                if j==1 and i==1:
                    self.rooms[id]={"x":x,"y":y}
                self.map[y][x]=room[j][i]
                i+=1
            j+=1
        return True

    def join_rooms(self):
        last_room=self.rooms[0]

        for i in range(1, len(self.rooms)):
            backwards_x=False
            backwards_y=False

            room=self.rooms[i]

            if last_room["x"]<room["x"]:
                backwards_x=True
            
            if last_room["y"]<room["y"]:
                backwards_y=True

            y=room["y"]
            x=0

            for x in range(room["x"], last_room["x"], -1 if backwards_x else 1):
                self.map[y,x]=self.floor

                if self.map[y+1, x]==self.void:
                    self.map[y+1, x]=self.borders
                
                if self.map[y-1, x]==self.void:
                    self.map[y-1, x]=self.borders

            for y in range(room["y"], last_room["y"], -1 if backwards_y else 1):
                self.map[y,x]=self.floor
            
                if self.map[y, x+1]==self.void:
                    self.map[y, x+1]=self.borders

                if self.map[y, x-1]==self.void:
                    self.map[y, x-1]=self.borders

            last_room=room
    def interact(self, x,y):
        z=self.item_map[y][x]
        if z in self.items.interactables.keys():
            return self.items.interactables[z]()

    def place_object(self, x, y, id):
        if id not in self.objects.values():
            self.buffer.write_buffer_line(0, f"Invaild ID: {id}")
        elif x<self.width or y<self.height:
            self.cursor.pos(x,y)
            self.buffer.write(self.object_key(id), flush=False)
            self.buffer.flush()

            if id==2:
                self.map[y][x]=id
            else:
                self.item_map[y][x]=id
                self.map[y][x]=id

        else:
            self.buffer.write_buffer_line(0, f"Position out of range.\nX: {x}\t Y: {y}\nMax X: {self.width}\tMax Y: {self.height}")

    def check_position(self, x, y):
        return self.map[y][x]

    def remove_object(self, x, y):
        if x<self.width or y<self.height:

            if self.check_position(x,y)==self.player_object and self.item_map[y][x]!=self.void:
                self.place_object(x,y, self.item_map[y][x])
            else:
                self.place_object(x,y,self.void)
                self.item_map[y][x]=self.void

        else:
            self.buffer.write_buffer_line(0, f"Position out of range.\nX: {x}\t Y: {y}\nMax X: {self.width}\tMax Y: {self.height}")
        
    def object_key(self, id):
        if id not in self.objects.values():
            self.buffer.write_buffer_line(0, f"Unable to return key value of id {id}")
            return " "
        return list(self.objects.keys())[list(self.objects.values()).index(id)]

    def draw_map(self, map_):
        clear_screen()
        self.cursor.pos(1,1)
        for y in range(1,self.height):
            for x in range(1,self.width):
                self.buffer.write(self.object_key(map_[y][x]), flush=False)
            self.buffer.write("\n", flush=False)
        self.buffer.flush()
        
        self.cursor.pos(1, self.height)
        self.buffer.save_buffer_line(self.cursor.x, self.cursor.y)

        self.cursor.pos(1, self.height+1)
        self.buffer.save_buffer_line(self.cursor.x, self.cursor.y)
