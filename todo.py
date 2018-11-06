#!/usr/bin/python3
# vim: ts=4 sw=4 et ft=py

import curses
import datetime
import time
import os

from topics import *


class BaseWindow:

    def __init__(self):
        self.h = 0
        self.w = 0

        self.stdscr = curses.initscr()

        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)


t = Topics()
win = BaseWindow()

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


def render_status_bar():
    cursor_x = 0
    cursor_y = win.h - 1

    for i in range(0, len(cmds)):
        win.stdscr.attron(curses.color_pair(1))
        win.stdscr.addstr(cursor_y, cursor_x, cmds[i])
        win.stdscr.attroff(curses.color_pair(1))
        cursor_x += len(cmds[i]) + 1
        win.stdscr.addstr(cursor_y, cursor_x, cmds_txt[i])
        cursor_x += len(cmds_txt[i]) + 1


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
    usr_in = 0

    while (usr_in != 24):   # 24 = ^X
        win.stdscr.clear()

        eval_usr_input(usr_in)

        win.h, win.w = win.stdscr.getmaxyx()

        render_status_bar()

        win.stdscr.refresh()

        # render topic list
        topic_win = curses.newwin(win.h - 1, win.w // 4, 0, 0)
        topic_win.border()

        render_topics(topic_win)

        topic_win.refresh()

        # render todo list
        todo_win = curses.newwin(win.h - 1, (win.w // 4) * 3, 0, win.w // 4)
        todo_win.border()
        todo_win.addstr(1, 1, str(usr_in))
        todo_win.refresh()

        # wait for user input
        usr_in = win.stdscr.getch()


def main():
    curses.wrapper(todo)


if (__name__ == "__main__"):
    main()
    curses.endwin()
