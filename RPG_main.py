import colorama
import RPG_Input
import RPG_Player
import RPG_Map
import RPG_Position
import RPG_Buffer

def main():
    colorama.init()
    RPG_Map.clear_screen()

    cur=RPG_Position.cursor()
    Buffer=RPG_Buffer.Buffer(cur)

    map_=RPG_Map.Map(cur, Buffer)
    map_.generate_new_map()
    map_.draw_map(map_.map)

    player=RPG_Player.Player(map_, Buffer, cur)

    map_.buffer.write_buffer_line(0, "WASD or Arrow keys to move  |  Press C to show controls")
    map_.place_random_item()
    while True:
        player.Move_Player(RPG_Input.get_c(Buffer))

if __name__=="__main__":
    main()