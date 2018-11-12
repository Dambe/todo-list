#!/usr/bin/python3
# vim: ts=4 sw=4 et ft=py

import curses
import datetime
import time
import os

from topics import *
from lists import *


class BaseWindow:

    def __init__(self):
        self.h = 0
        self.w = 0

        self.stdscr = curses.initscr()

        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        self.h, self.w = self.stdscr.getmaxyx()

        # render topic list
        self.topic_win = curses.newwin((self.h - 1), (self.w // 4), 0, 0)
        self.topic_win.border()


t = Topics()
l = Lists()
win = BaseWindow()

cmds = [ "^X", "^L", "^E" ]
cmds_txt = [ "Exit\t", "Topics menu\t", "Edit\t" ]


def eval_usr_input(key):
    if (t.is_menu_active == True):
        if (key == 10):                         # RETURN
            t.is_menu_active = False
        elif (key == 14):                       # ^N
            t.new_topic(win.h, win.w)
        elif (key == 4  ):                      # ^D
            t.delete_topic()
        elif key == ord('j') or key == curses.KEY_DOWN:
            t.menu_pos += 1
            if (t.menu_pos > t.num_topics):
                t.menu_pos = t.num_topics
        elif key == ord('k') or key == curses.KEY_UP:
            t.menu_pos -= 1
            if (t.menu_pos < 1):
                t.menu_pos = 1
        # no valid key for topic menu
        return

    if (l.is_menu_active == True):
        if (key == 14):
            l.new_item(win.h, win.w)
        elif key == ord('j') or key == curses.KEY_DOWN:
            l.menu_pos += 1
            if (l.menu_pos > l.num_items):
                l.menu_pos = l.num_items
        elif key == ord('k') or key == curses.KEY_UP:
            l.menu_pos -= 1
            if (l.menu_pos < 1):
                l.menu_pos = 1
        # no valid key for topic menu
        else:
            return

    if (key == 5):                              # ^E
        l.is_menu_active = True

    if (key == 12):                             # ^L
        t.is_menu_active = True
        t.menu_pos = 1


def render_status_bar():
    cursor_x = 0
    cursor_y = win.h - 1

    if t.is_menu_active == True:
        tmp_cmds = t.cmds
        tmp_cmds_txt = t.cmd_txt
    else:
        tmp_cmds = cmds
        tmp_cmds_txt = cmds_txt

    for i in range(0, len(tmp_cmds)):
        win.stdscr.attron(curses.color_pair(1))
        win.stdscr.addstr(cursor_y, cursor_x, tmp_cmds[i])
        win.stdscr.attroff(curses.color_pair(1))
        cursor_x += len(tmp_cmds[i]) + 1
        win.stdscr.addstr(cursor_y, cursor_x, tmp_cmds_txt[i])
        cursor_x += len(tmp_cmds_txt[i]) + 1


def render_topics():
    i = 1

    topic_win = curses.newwin(win.h - 1, win.w // 4, 0, 0)
    topic_win.border()

    for line in t.topic_names:
        if (i == t.menu_pos) and (t.is_menu_active == True):
            topic_win.attron(curses.color_pair(1))
            topic_win.addstr(i, 1, line.rstrip())
            topic_win.attroff(curses.color_pair(1))
        else:
            topic_win.addstr(i, 1, line.rstrip())
        i += 1

    topic_win.refresh()


def render_lists(usr_in):
    i = 1

    list_win = curses.newwin(win.h - 1, (win.w // 4) * 3, 0, win.w // 4)
    list_win.border()
    list_win.addstr(i, 1, str(usr_in))
    i += 1

    for line in l.items:
        if (i == l.menu_pos) and (l.is_menu_active == True):
            list_win.attron(curses.color_pair(1))
            list_win.addstr(i, 1, line.rstrip())
            list_win.attroff(curses.color_pair(1))
        else:
            list_win.addstr(i, 1, line.rstrip())
        i += 1

    list_win.refresh()


def todo(args):
    usr_in = 0

    while (usr_in != 24):   # 24 = ^X
        win.stdscr.clear()
        win.stdscr.refresh()
        win.h, win.w = win.stdscr.getmaxyx()

        render_status_bar()
        render_topics()
        render_lists(usr_in)

        # wait for user input
        usr_in = win.stdscr.getch()
        eval_usr_input(usr_in)


def main():
    curses.wrapper(todo)


if (__name__ == "__main__"):
    main()
    curses.endwin()
