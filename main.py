import colorama
import Input
import Player
import Map
import Position

if __name__=="__main__":
    colorama.init()
    Map.clear_screen()

    cur=Position.cursor()
    Buffer=Map.Buffer(cur)

    Current_Map=Map.Map(cur, Buffer)
    Current_Map.generate_map()
    Current_Map.draw_map()

    player=Player.Player(Current_Map, Buffer, cur)

    while True:
        player.Move_Player(Input.get_arrow_key(Buffer))