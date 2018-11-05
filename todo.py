#!/usr/bin/python3
# vim: ts=4 sw=4 et ft=py

import curses
import datetime
import time
import os

cmds = [ "^X", "^L", "^B" ]
cmds_txt = [ "Exit\t", "Topics menu\t", "B\t" ]

topic_menu_active = False
topic_menu_pos = 1
num_topics = 99

def eval_usr_input(key):
    # TODO: remove global, good time to introduce classes
    global topic_menu_active
    global topic_menu_pos

    if key == 10:   # RETURN
        if topic_menu_active == True:
            topic_menu_active = False
    elif key == 12:   # ^L
        topic_menu_active = True
    elif key == ord('j') or key == 258:      # down
        topic_menu_pos += 1
        if (topic_menu_pos > num_topics):
            topic_menu_pos = num_topics
    elif key == ord('k') or key == 259:    # up
        topic_menu_pos -= 1
        if (topic_menu_pos < 1):
            topic_menu_pos = 1


def render_topics(win):
    # TODO: remove global
    global num_topics

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "topics")

    # get num of topics
    num_topics = sum(1 for l in open(filename, "r"))

    # file is automatically closed after previos iteration, needs re-open
    fd = open(filename, "r")

    i = 1
    for line in open(filename, "r"):
        if (i == topic_menu_pos) and (topic_menu_active == True):
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
