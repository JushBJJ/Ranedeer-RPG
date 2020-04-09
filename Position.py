from colorama import Cursor

up=lambda n=1: print(Cursor.UP(n), end="")
down=lambda n=1: print(Cursor.DOWN(n), end="")
left=lambda n=1: print(Cursor.BACK(n), end="")
right=lambda n=1: print(Cursor.FORWARD(n), end="")
pos=lambda x,y: print(f"\033[{y};{x}H", end="")

class cursor:
    def __init__(self):
        pos(0,0)
        self.x=0
        self.y=0
    
        self.saved_positions={}

    def down(self, n=1):
        self.y+=n
        pos(self.x, self.y)
    
    def up(self, n=1):
        self.y-=n
        pos(self.x, self.y)
    
    def right(self, n=1):
        self.x+=n
        pos(self.x, self.y)

    def left(self, n=1):
        self.x-=n
        pos(self.x, self.y)

    def pos(self, x,y):
        self.x=x
        self.y=y

        pos(self.x, self.y)

    def save_pos(self, name):
        self.saved_positions[str(name)]=[self.x,self.y]

    def load_pos(self, name):
        x=self.saved_positions[str(name)][0]
        y=self.saved_positions[str(name)][1]

        self.pos(x,y)

    def del_pos(self, name):
        del self.saved_positions[str(name)]