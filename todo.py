#!/usr/bin/python3
# vim: ts=4 sw=4 et ft=py

import curses
import datetime
import time

cmds = [ "^X", "^A", "^B" ]
cmds_txt = [ "Exit\t", "A\t", "B\t" ]


def todo(args):
    stdscr = curses.initscr()

    stdscr.clear()
    stdscr.refresh()

    cursor_x = 0
    cursor_y = 0
    usr_in = 0

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    while (usr_in != 24):   # 24 = ^X
        stdscr.clear()

        height, width = stdscr.getmaxyx()

        stdscr.move(0, 0)
        stdscr.addstr(str(usr_in))

        # render status bar
        cursor_x = 0
        cursor_y = height - 1
        for i in range(0, len(cmds)):
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(cursor_y, cursor_x, cmds[i])
            stdscr.attroff(curses.color_pair(1))
            cursor_x += len(cmds[i]) + 1
            stdscr.addstr(cursor_y, cursor_x, cmds_txt[i])
            cursor_x += len(cmds_txt[i]) + 1

        stdscr.refresh()

        # render topic list
        topic_win = curses.newwin(height - 1, width // 4, 0, 0)
        topic_win.border()
        topic_win.addstr(1, 1, "This is a test")
        topic_win.refresh()

        # render todo list
        todo_win = curses.newwin(height - 1 , (width // 4) * 3, 0, width // 4)
        todo_win.border()
        todo_win.addstr(1, 1, "This is a test")
        todo_win.refresh()

        # wait for user input
        usr_in = stdscr.getch()


def main():
    curses.wrapper(todo)


if (__name__ == "__main__"):
    main()
    curses.endwin()
