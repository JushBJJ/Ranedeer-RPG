import colorama
import RPG_Input
import RPG_Player
import RPG_Map
import RPG_Position
import RPG_Buffer
import multiprocessing

def main():
    colorama.init()
    RPG_Map.clear_screen()

    p=multiprocessing.Process(target=RPG_Map.print_loading, args=("Loading...",))
    p.start()

    cur=RPG_Position.cursor()
    Buffer=RPG_Buffer.Buffer(cur)

    Dungeon=RPG_Map.Map(cur, Buffer, dungeon=True)
    Town=RPG_Map.Map(cur, Buffer, dungeon=False)
    player=RPG_Player.Player(Town, Buffer, cur)

    p.kill()

    Town.draw_map(Town.map)
    Town.buffer.write_buffer_line(0, "WASD or Arrow keys to move  |  Press C to show controls")
    player.spawn()
    
    while True:
        player.Move_Player(RPG_Input.get_c(Buffer))

if __name__=="__main__":
    main()