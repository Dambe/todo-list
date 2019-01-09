#!/usr/bin/python3
# vim: ts=4 sw=4 et ft=py

import curses
import datetime
import time
import os

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


l = List()
win = BaseWindow()

cmds = [ "^N", "^D", "^E", "^X" ]
cmds_txt = [ "New\t", "Delete\t", "Edit\t", "Exit\t" ]


def eval_usr_input(key):
    if (l.is_topic_menu_active == True):
        if (key == 14):                         # ^N
            l.new_list(win.h, win.w)
        elif (key == 4):                        # ^D
            l.delete_list()
        elif (key == 5):                        # ^E
            l.rename_list(win.h, win.w)
        elif key == ord('j') or key == curses.KEY_DOWN:
            l.topic_menu_pos += 1
            if (l.topic_menu_pos > len(l.lists)):
                l.topic_menu_pos = len(l.lists)
            l.show_list()
        elif key == ord('k') or key == curses.KEY_UP:
            l.topic_menu_pos -= 1
            if (l.topic_menu_pos < 1):
                l.topic_menu_pos = 1
            l.show_list()
        elif key == ord('l') or key == curses.KEY_RIGHT:
            l.is_topic_menu_active = False
            l.is_list_menu_active = True
        # no valid key for topic menu
        else:
            return

    if (l.is_list_menu_active == True):
        if (key == 27):                         # ESC
            l.is_list_menu_active = False
        if(key == 4):                           # ^D
            l.delete_item()
        elif (key == 14):                       # ^N
            l.new_item(win.h, win.w)
        elif key == ord('j') or key == curses.KEY_DOWN:
            l.list_menu_pos += 1
            if (l.list_menu_pos > len(l.items)):
                l.list_menu_pos = len(l.items)
        elif key == ord('k') or key == curses.KEY_UP:
            l.list_menu_pos -= 1
            if (l.list_menu_pos < 1):
                l.list_menu_pos = 1
        elif key == ord('h') or key == curses.KEY_LEFT:
            l.is_list_menu_active = False
            l.is_topic_menu_active = True
        # no valid key for topic menu
        else:
            return


def render_status_bar(usr_in):
    cursor_x = 0
    cursor_y = win.h - 1

    if l.is_topic_menu_active == True or l.is_list_menu_active == True:
        tmp_cmds = cmds
        tmp_cmds_txt = cmds_txt
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

    # user key, for debugging only
    win.stdscr.addstr(cursor_y, cursor_x, str(usr_in))


def render_topics():
    i = 1

    topic_win = curses.newwin(win.h - 1, win.w // 4, 0, 0)
    topic_win.border()

    for line in l.lists:
        if (i == l.topic_menu_pos) and (l.is_topic_menu_active == True):
            topic_win.attron(curses.color_pair(1))
            topic_win.addstr(i, 1, line.rstrip())
            topic_win.attroff(curses.color_pair(1))
        else:
            topic_win.addstr(i, 1, line.rstrip())
        i += 1

    topic_win.refresh()


def render_lists():
    i = 1

    list_win = curses.newwin(win.h - 1, (win.w // 4) * 3, 0, win.w // 4)
    list_win.border()

    for item in l.items_test:
        txt = item.get_item()
        if (i == l.list_menu_pos) and (l.is_list_menu_active == True):
            list_win.attron(curses.color_pair(1))
            list_win.addstr(i, 1, txt.rstrip())
            list_win.attroff(curses.color_pair(1))
        else:
            list_win.addstr(i, 1, txt.rstrip())
        i += 1

    list_win.refresh()


def todo(args):
    usr_in = 0

    while (usr_in != 24):   # 24 = ^X
        win.stdscr.clear()
        win.stdscr.refresh()
        win.h, win.w = win.stdscr.getmaxyx()

        render_status_bar(usr_in)
        render_topics()
        render_lists()

        # wait for user input
        usr_in = win.stdscr.getch()
        eval_usr_input(usr_in)


def main():
    curses.wrapper(todo)


if (__name__ == "__main__"):
    main()
    curses.endwin()
