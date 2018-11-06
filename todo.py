#!/usr/bin/python3
# vim: ts=4 sw=4 et ft=py

import curses
import datetime
import time
import os

from topics import *

t = Topics()
cmds = [ "^X", "^L", "^N" ]
cmds_txt = [ "Exit\t", "Topics menu\t", "New topic\t" ]

def eval_usr_input(key):

    if key == 10:   # RETURN
        if t.is_menu_active == True:
            t.is_menu_active = False
    elif key == 12: # ^L
        t.is_menu_active = True
        t.menu_pos = 1
    elif key == 14: # ^N
        t.new_topic(80, 80)
    elif key == ord('j') or key == 258:      # down
        t.menu_pos += 1
        if (t.menu_pos > t.num_topics):
            t.menu_pos = t.num_topics
    elif key == ord('k') or key == 259:    # up
        t.menu_pos -= 1
        if (t.menu_pos < 1):
            t.menu_pos = 1


def render_topics(win):
    i = 1

    for line in t.topic_names:
        if (i == t.menu_pos) and (t.is_menu_active == True):
            win.attron(curses.color_pair(1))
            win.addstr(i, 1, line.rstrip())
            win.attroff(curses.color_pair(1))
        else:
            win.addstr(i, 1, line.rstrip())
        i += 1


def todo(args):
    stdscr = curses.initscr()

    stdscr.clear()
    stdscr.refresh()

    usr_in = 0

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    while (usr_in != 24):   # 24 = ^X
        stdscr.clear()

        eval_usr_input(usr_in)

        height, width = stdscr.getmaxyx()

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

        render_topics(topic_win)

        topic_win.refresh()

        # render todo list
        todo_win = curses.newwin(height - 1, (width // 4) * 3, 0, width // 4)
        todo_win.border()
        todo_win.addstr(1, 1, str(usr_in))
        todo_win.refresh()

        # wait for user input
        usr_in = stdscr.getch()


def main():
    curses.wrapper(todo)


if (__name__ == "__main__"):
    main()
    curses.endwin()
