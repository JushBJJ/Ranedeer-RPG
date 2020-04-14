import colorama
import Input
import Player
import Map
import Position
import Buffer

if __name__=="__main__":
    colorama.init()
    Map.clear_screen()

    cur=Position.cursor()
    Buffer=Buffer.Buffer(cur)

    map=Map.Map(cur, Buffer)
    map.generate_new_map()
    map.draw_map(map.map)

    player=Player.Player(map, Buffer, cur)

    Buffer.write_buffer_line(0, "WASD or Arrow keys to move  |  Press C to show controls")
    map.place_object(10,10, 3)
    while True:
        player.Move_Player(Input.get_c(Buffer))