import sys
import Input
from Map import clear_screen

class Player:
    def __init__(self, map_, buffer, cursor):
        self.x=20
        self.y=10

        self.last_face=0

        self.map=map_
        self.map.place_object(self.x, self.y, 2)

        self.buffer=buffer
        self.cursor=cursor

        self.cursor.pos(self.x, self.y)
        self.inventory={}

    def Move_Player(self, n):
        positions={0: self.up, 1: self.down, 2: self.left, 3: self.right}
        controls={4: self.interact, 5: self.show_inventory, 7:self.quit, 6:self.show_controls}

        if n in positions.keys():
            positions[n]()
        elif n in controls.keys():
            controls[n]()

        self.buffer.write_buffer_line(1, f"X: {self.x}\tY: {self.y}")
        self.buffer.clear_buffer()

    def show_controls(self):
        clear_screen()
        self.cursor.pos(1,1)
        print("""
Movement:
    W or Up Arrow       -> Move Up
    A or Left Arrow     -> Move Left
    S or Right Arrow    -> Move Down
    D or Down Arrow     -> Move Right

Other:
    E                   -> Interact
    C                   -> Controls
    Q                   -> Quit
        """)

        self.buffer.write("Press Q to exit.")

        while True:
            if Input.get_c(self.buffer)==7:
                self.map.draw_map()
                return

    def interact(self):
        x=self.x
        y=self.y

        if self.last_face==0: y=self.y-1
        elif self.last_face==1: y=self.y+1
        elif self.last_face==2: x=self.x-1
        elif self.last_face==3: x=self.x+1

        object=self.map.check_position(x,y)
        self.buffer.clear()
        if object in self.map.interactables.values():
            in_inventory, info=self.map.interact(x,y)

            if in_inventory:
                if info["Name"] in self.inventory.keys():
                    self.buffer.write_buffer_line(0, "Item already in your inventory.")
                else:
                    self.inventory[info["Name"]]=info
                    self.map.remove_object(x,y)
                    self.buffer.write_buffer_line(0, "Collected Item.")
        else:
            self.buffer.write_buffer_line(0, "Nothing to interact.")

    def show_inventory(self):
        clear_screen()
        self.cursor.pos(1,1)

        for item_num, name in enumerate(self.inventory):
            name=name["Name"]
            self.buffer.write(f"{item_num}: {name}\n")
        
        self.buffer.write("Press Q to exit.")

        while True:
            if Input.get_c(self.buffer)==7:
                self.map.draw_map()
                return

        # TODO Add equip
    
    def quit(self):
        clear_screen()
        sys.exit(0)

    def up(self):
        object=self.map.check_position(self.x, self.y-1)
        if object in self.map.non_solid:
            last_y=self.y

            self.map.remove_object(self.x, self.y)
            self.y-=1
            self.map.place_object(self.x, self.y, 2)
            self.map.place_object(self.x, last_y, object)

    def down(self):
        object=self.map.check_position(self.x, self.y+1)
        if object in self.map.non_solid:
            last_y=self.y

            self.map.remove_object(self.x, self.y)
            self.y+=1
            self.map.place_object(self.x, self.y, 2)
            self.map.place_object(self.x, last_y, object)

    def left(self):
        object=self.map.check_position(self.x-1, self.y)
        if object in self.map.non_solid:
            last_x=self.x

            self.map.remove_object(self.x, self.y)
            self.x-=1
            self.map.place_object(self.x, self.y, 2)
            self.map.place_object(last_x, self.y, object)

    def right(self):
        object=self.map.check_position(self.x+1, self.y)
        if object in self.map.non_solid:
            last_x=self.x

            self.map.remove_object(self.x, self.y)
            self.x+=1
            self.map.place_object(self.x, self.y, 2)
            self.map.place_object(last_x, self.y, object)