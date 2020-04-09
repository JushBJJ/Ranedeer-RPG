class Player:
    def __init__(self, map_, buffer, cursor):
        self.x=20
        self.y=10

        self.map=map_
        self.map.place_object(self.x, self.y, 2)

        self.buffer=buffer
        self.cursor=cursor

        self.xz=0
        self.yz=0

        self.cursor.pos(self.x, self.y)

    def Move_Player(self, n):
        positions={0: self.up, 1: self.down, 2: self.left, 3: self.right}

        if n in positions.keys():
            positions[n]()

        self.buffer.bottom_write(f"X: {self.x}\nY: {self.y}")

    def up(self):
        if not self.map.check_position(self.x, self.y-1):
            self.map.remove_object(self.x, self.y)
            self.y-=1
            self.map.place_object(self.x, self.y, 2)

    def down(self):
        if not self.map.check_position(self.x, self.y+1):
            self.map.remove_object(self.x, self.y)
            self.y+=1
            self.map.place_object(self.x, self.y, 2)

    def left(self):
        if not self.map.check_position(self.x-1, self.y):
            self.map.remove_object(self.x, self.y)
            self.x-=1
            self.map.place_object(self.x, self.y, 2)

    def right(self):
        if not self.map.check_position(self.x+1, self.y):
            self.map.remove_object(self.x, self.y)
            self.x+=1
            self.map.place_object(self.x, self.y, 2)