import sys

class Buffer:
    def __init__(self, cursor, F=sys.stdout):
        self.buffer=F
        self.buffer_X="\r"
        self.cursor=cursor

        self.buffers={}
    
    def save_buffer_line(self, x, y):
        buffers_n=len(self.buffers)
        next_line=str(buffers_n)

        self.cursor.pos(x,y)
        self.cursor.save_pos(next_line)
        self.buffers[next_line]=""

    def clear_buffer_line(self, line):
        line=str(line)
        self.cursor.load_pos(line)

        for _ in self.buffers[line]:
            self.write(" "*2)

        self.buffers[line]=""

    def write_buffer_line(self, line, msg):
        self.clear_buffer_line(line)
        self.buffers[str(line)]=msg

        self.cursor.load_pos(str(line))
        self.write(msg)

    def write(self, x, flush=True):
        self.buffer.write(x)
        self.buffer.flush() if flush==True else None

    def flush(self):
        self.buffer.flush()