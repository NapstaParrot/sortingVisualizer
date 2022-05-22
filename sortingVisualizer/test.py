import curses

def main(stdscr) :
    stdscr.vline(0, 0, "H", 0)
    stdscr.refresh()


curses.wrapper(main)
