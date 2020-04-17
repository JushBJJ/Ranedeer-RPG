import colorama
import RPG_Input
import RPG_Player
import RPG_World
import RPG_Map
import multiprocessing
import sys

def main():
    p=multiprocessing.Process(target=RPG_Map.print_loading, args=("Loading...",))
    p.start()

    colorama.init(wrap=True, convert=True)
    RPG_Map.clear_screen()

    World1=RPG_World.World()

    World1.create_dungeon()
    World1.create_town()

    World1.set_current_map("Town")
    Local_Map=World1.get_current_map()["class"]
    
    Buffer=Local_Map.buffer
    Cursor=Local_Map.cursor

    player=RPG_Player.Player(World1, Local_Map, Buffer, Cursor)
    p.kill()

    Local_Map.draw_map()
    Local_Map.buffer.write_buffer_line(0, "WASD or Arrow keys to move  |  Press C to show controls")
    player.spawn(Local_Map)
    
    while True:
        player.Move_Player(RPG_Input.get_c(Local_Map.buffer))

if __name__=="__main__":
    main()