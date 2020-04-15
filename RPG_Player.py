import sys
import RPG_Input
from RPG_Map import clear_screen

class Player:
    def __init__(self, map_, buffer, cursor):
        self.x=map_.rooms[0]["x"]
        self.y=map_.rooms[0]["y"]

        self.last_face=0

        self.map=map_
        self.map.place_object(self.x, self.y, 2)

        self.buffer=buffer
        self.cursor=cursor

        self.cursor.pos(self.x, self.y)
        self.inventory={}

    def Move_Player(self, n):
        reprint_top=False

        positions={0:(self.x, self.y-1, "^"), 1: (self.x, self.y+1, "v"), 2: (self.x-1, self.y, "<"), 3: (self.x+1,self.y, ">")}
        controls={4: self.interact, 5: self.show_inventory, 7:self.quit, 6:self.show_controls}
        
        if n in positions.keys():
            del self.map.objects[positions[self.last_face][2]]
            self.last_face=n
            self.map.objects[positions[self.last_face][2]]=2

            object=self.map.check_position(positions[n][0], positions[n][1])

            if object in self.map.non_solid:
                self.map.remove_object(self.x, self.y)
                
                self.x=positions[n][0]
                self.y=positions[n][1]

                self.map.place_object(self.x, self.y, 2)
            else:
                self.map.place_object(self.x, self.y, 2)
                return # More cheaper
            
        elif n in controls.keys():
            reprint_top=controls[n]()

        self.buffer.write_buffer_line(1, f"X: {self.x}\tY: {self.y}")

        if reprint_top:
            self.buffer.write_buffer_line(0, "WASD or Arrow keys to move  |  Press C to show controls")

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
            if RPG_Input.get_c(self.buffer)==7:
                self.map.draw_map(self.map.map)
                return True

    def interact(self):
        x=self.x
        y=self.y

        if self.last_face==0: y=self.y-1
        elif self.last_face==1: y=self.y+1
        elif self.last_face==2: x=self.x-1
        elif self.last_face==3: x=self.x+1

        object_on_top=self.map.item_map[self.y,self.x]
        object=self.map.item_map[y,x]

        if object in self.map.interactables.keys() or object_on_top in self.map.interactables.keys():
            if object_on_top in self.map.interactables.keys():
                in_inventory, info=self.map.interact(self.x, self.y)
            else:
                in_inventory, info=self.map.interact(x,y)

            if in_inventory:
                if info["Name"] in self.inventory.keys():
                    self.buffer.write_buffer_line(0, "Item already in your inventory.")
                else:
                    self.inventory[info["Name"]]=info

                    if object_on_top not in self.map.interactables.keys():
                        self.map.remove_object(x,y)  
                    else:
                        self.map.item_map[self.y,self.x]=0

                    self.buffer.write_buffer_line(0, "Collected Item.")
        else:
            self.buffer.write_buffer_line(0, "Nothing to interact.")

    def show_inventory(self):
        clear_screen()
        self.cursor.pos(1,1)

        for item_num, name in enumerate(self.inventory):
            self.buffer.write(f"{item_num}) {name}\n")
        
        self.buffer.write("Press Q to exit.")

        while True:
            if RPG_Input.get_c(self.buffer)==7:
                self.map.draw_map(self.map.map)
                return True

        # TODO Add equip
    
    def quit(self):
        clear_screen()
        sys.exit(0)
    
if __name__=="__main__":
    import RPG_main
    RPG_main.main()