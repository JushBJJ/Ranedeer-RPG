import numpy as np 
import RPG_Map
import RPG_Buffer
import RPG_Position
import RPG_Player

class World:
    def __init__(self):
        self.maps={}
        self.current_map=None

    def create_map(self, width, height):
        return np.zeros((height, width))

    def insert_map(self, name, map_class):
        try:
            self.maps[name]={"class": map_class, "map": map_class.map, "width": map_class.map.shape[1], "height": map_class.map.shape[0]}
        except Exception as e:
            print("Unable to insert map. Error: ", e)
    
    def draw_map(self, name):
        self.maps[name].draw_map()
    
    def delete_map(self, name):
        try:
            del self.maps[name]
        except Exception as e:
            print("Map does not exist: ", e)
    
    def switch_map(self, name):
        self.set_current_map(name)
        return get_current_map()

    def get_current_map(self):
        return self.current_map
    
    def set_current_map(self, name):
        self.current_map=self.maps[name]

    def create_town(self):
        cursor, buffer=self.new_info()
        x=RPG_Map.Map(cursor, buffer, dungeon=False)
        map_x=x.map

        self.maps["Town"]={"class": x, "map":map_x, "width":map_x.shape[1], "height":map_x.shape[0]}
    
    def create_dungeon(self):
        cursor, buffer=self.new_info()
        x=RPG_Map.Map(cursor, buffer, dungeon=True)
        map_x=x.map

        self.maps["Dungeon"]={"class": x, "map":map_x, "width":map_x.shape[1], "height":map_x.shape[0]}

    def new_info(self):
        cursor=RPG_Position.cursor()
        buffer=RPG_Buffer.Buffer(cursor)

        return cursor, buffer