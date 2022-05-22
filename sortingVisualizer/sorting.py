import curses
import time
import sorts
from random import shuffle
from math import floor

SORTING_ALGS = ["bubble", "insertion", "selection"]


# delay between bar highlights in ms
DELAY = 5
def visualize(sortI, length) :
    scr = curses.newwin(20, 0)
    scr_y, scr_x = scr.getmaxyx() 
    scr.nodelay(True)
    
    output = curses.newwin(1, 0, 10, 0)
    
    # array length
    if length <= 0 or length > STD_X :
        length = STD_X + 1
        
        
    arr = [*range(1, length + 1)]
    shuffle(arr)
    
    
    # sorting algorithms
    sort = f"sorts.{SORTING_ALGS[sortI]}({arr})"
    states, pointers = eval(sort)
    
    mid = scr_x // 2 
    bar_mid = mid - len(states[0]) // 2
    
    start_time = time.time()
    # bar visualization
    for i, (bars, points) in enumerate(zip(states, pointers)) :
        for j, bar_height in enumerate(bars) :
            if j in points :
                col = curses.color_pair(2)
            else :
                col = curses.color_pair(1)
            
            # priting a 11-length vertical bar
            # (final product will be 10 tall but curses-win is dumb and wont
            # let me print a 0 length vline >:[ )
            scr.vline(0, bar_mid + j, " ", 11, col)
            
            # deleting some part of the printed bar
            # =====================================
            # determining the height of the bar
            # height = floor(maxBarHeight - barHeight / highestValue * maxBarHeight) + 1
            height = floor(10 - bar_height / length * 10) + 1
            scr.vline(0, bar_mid + j, " ", height)

            key = scr.getch()
            if key in (81, 113) :
                output.addstr(0, 0, "List has been stopped")
                output.refresh()
                return

            elif key == 27 :
                exit()
                
            
        scr.refresh()
        
        # showcasing the unsorted list for a lil
        if i == 0 :
            curses.napms(500)
            continue
            
        curses.napms(DELAY)
    
    # time lel
    end_time = time.time()
    sort_time = round(end_time - start_time, 3)
            
    # final touches when the list is sorted
    # looping the final state
    for i, bar_height in enumerate(states[-1]) :
        color = curses.color_pair(3)
        scr.vline(0, bar_mid + i, " ", 11, color)
        
        height = floor(10 - bar_height / length * 10) + 1
        scr.vline(0, bar_mid + i, " ", height)
        
        scr.refresh()
        curses.napms(DELAY * 2)
    
    attr = curses.color_pair(3) | curses.A_REVERSE
    out_txt = f"List is sorted in {sort_time} seconds!"
    out_mid = mid - len(out_txt) // 2
    
    output.addstr(0, out_mid, out_txt, attr)
    output.refresh() 


def menu() :
    total_sorts = len(SORTING_ALGS)
    scr = curses.newwin(0, 0)
    
    # header
    txt = (
        "Use 'W' or 'S' or up/down arrow keys"
        + " to choose your sorting algorithm."
    )
    # custom line breaker
    for word in txt.split(" ") :
        txtY, txtX = scr.getyx()
        
        if txtX + len(f"{word}") > STD_X :
            txtY, txtX = txtY + 1, 0
            
        space = "" if txtX == 0 else " "
        scr.addstr(txtY, txtX, space + word)

    menuY = txtY + 2
    
    default_attr = curses.color_pair(5) | curses.A_BOLD

    # sorting algs list
    x = "\n".join(SORTING_ALGS)
    scr.addstr(menuY, 0, x, default_attr)

    # seperator
    for i in range(3) :
        scr.addstr(i + menuY, 10, "|", default_attr)
    

    # sorting algorithm chooser
    arrowY, arrowX = 0, 12
    while True :
        # sorting algortihms seletor
        for i, algs in enumerate(SORTING_ALGS) :
            if i == arrowY :
                attr = curses.A_NORMAL
                arrow = "<"
            else :
                attr = curses.color_pair(5) | curses.A_BOLD
                arrow = " "
            
            scr.addstr(i + menuY, 0, algs, attr)
            scr.addstr(i + menuY, arrowX, arrow) # remove the arrow

        key = scr.getch()
        # lowercase'd
        if key in (87, 83) :
            key += 32

        # w
        if key in (119, ) :
            arrowY -= 1
        # s
        elif key in (115, ) :
            arrowY += 1
        # enter    
        elif key == 10 :
            return arrowY
            
        if arrowY < 0 :
            arrowY = total_sorts - 1
            
        elif arrowY > total_sorts - 1 :
            arrowY = 0


def main(stdscr) :
    curses.curs_set(0)

    # black fg
    curses.init_pair(1, 0, curses.COLOR_WHITE)
    curses.init_pair(2, 0, curses.COLOR_RED)
    curses.init_pair(3, 0, curses.COLOR_GREEN)
    curses.init_pair(4, 0, curses.COLOR_YELLOW)
    curses.init_pair(5, 0, curses.COLOR_BLACK)
    
    global STD_Y, STD_X
    STD_Y, STD_X = stdscr.getmaxyx()
    STD_Y, STD_X = STD_Y - 1, STD_X - 1
    
    key_win = curses.newwin(0, 0, 16, 16)
    
    sortI = menu()
    stdscr.refresh()
    
    length = 0
    while True :
        # list length
        key_win.move(0, 0)
        key_win.clrtoeol()
        key_win.addstr(str(length), curses.color_pair(5) | curses.A_BOLD)
        
        # header
        stdscr.addstr(
            12, 0, 
            "Type in the list length.\n" +
            "Press q to re-open the menu.\n", 
            curses.A_UNDERLINE
        )
        stdscr.addstr(
            14, 0,
            f"\nSelected sort : \n" +
            "List Length   : "
        )
        stdscr.addstr(
            15, 16,
            f"{SORTING_ALGS[sortI]} sort",
            curses.color_pair(5) | curses.A_BOLD
        )
        stdscr.refresh()
        
        key = key_win.getch()
        char = chr(key)
        
        # if number > 0 keys are pressed
        if 48 <= key <= 57 :
            length = length * 10 + int(char)
            
        # if backspace or delete key is pressed
        elif key in (8, 127) :
            length = length // 10
            
        # if enter key is pressed
        elif key == 10  :
            stdscr.clear()
            stdscr.refresh()
            
            visualize(sortI, length)
            length = 0
            continue
            
        # if Q key is pressed
        elif key in (113, 81) :
            sortI = menu()
            stdscr.clear()
            stdscr.refresh()
        
        elif key == 27 :
            exit()

        else :
            continue
        


curses.wrapper(main)