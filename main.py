import curses
import time
import logging
from database import letters, padding, letter_height
logging.basicConfig(filename='.log', filemode='w+', format="%(levelname)s: %(message)s", level=logging.DEBUG)

last_text = ""
last_terminal_size = (0, 0)

def render(src, new):
    global last_text, cleared, last_terminal_size
    
    terminal_size = src.getmaxyx()
    y, x = (x//2 for x in terminal_size)
    y -= letter_height // 2
    x -= sum([((len(letters[x]) // letter_height) // 2) + padding for x in new if x in letters])

    if len(new) > len(last_text):
        for _ in range(len(new)):
            last_text += " "
    

    for _, [item, last] in enumerate(zip(new, last_text)):
        if not item in letters:
            continue
        
        tx, ty = 0, 0
        
        for index, signal in enumerate(letters[item]):
            ty = y + (index % letter_height)
            tx = x + (index // letter_height)
            
            if item != last:
                src.addstr(ty, tx, " ", curses.A_REVERSE if signal > 0 else curses.A_NORMAL)
                src.timeout(1)
                src.getch()
            
            src.refresh()

        x += (len(letters[item]) // letter_height) + padding

        # slow buffer updating effect
    
    last_text = new
    last_terminal_size = terminal_size[:]

CURSES_ERROR_MESSAGE = "Cannot render in this size"

def main(src):
    err = True

    while True:
        text = time.strftime('%H:%M:%S')
        try:
            if err:
                src.nodelay(True)
                src.clear()
                err = False
            render(src, text)
        except curses.error:
            err = True
            src.nodelay(False)
            try:
                y, x = (x//2 for x in src.getmaxyx())
                x -= len(CURSES_ERROR_MESSAGE) // 2
                src.clear()
                src.addstr(y, x, "Cannot render in this size")
                src.refresh()
            except curses.error:
                pass
            src.getch()


c = curses.initscr()
curses.curs_set(0)

try:
    curses.wrapper(main)
except KeyboardInterrupt:
    pass
