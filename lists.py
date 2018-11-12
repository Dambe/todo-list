#!/usr/bin/python3
# vim: ts=4 sw=4 et ft=py

import curses
import os


class Lists:
    filepath = ""
    num_items = 0
    items = []
    is_menu_active = False
    menu_pos = 0


    def __init__(self):
        self.update_topics()


    def clear_topics(self):
        self.num_items = 0
        self.items = []


    def update_topics(self):
        dirname = os.path.dirname(__file__)
        self.filepath = os.path.join(dirname, "dummy")

        # get todo items from file
        for line in open(self.filepath, "r"):
            if line not in self.items:
                self.items.append(line)

        # get num of todo items
        self.num_items = len(self.items)


    def new_item(self, height, width):
        new_i = ""

        iwin = curses.newwin(3, 50, (height // 2), (width // 2) - 25)
        iwin.border()
        curses.echo()
        y, x = iwin.getyx()
        iwin.addstr(y + 1, x + 1, "New item: ")
        iwin.refresh()

        # getstr() returns a byte object rather than a string
        # this means, it must be decoded first
        # python3 problem only
        new_i = iwin.getstr().decode(encoding="utf-8") + '\n'

        # write new topic to file if topic does not exist yet
        # and string not empty
        if (new_i not in self.items) and (new_i != "\n"):
            f = open(self.filepath, "a")
            f.write(new_i)
            f.close()

        self.update_topics()


    def delete_item(self):
        new_items = []

        delitem = self.items[self.menu_pos - 1]

        for i in self.items:
            if (i != delitem):
                new_items.append(i)

        f = open(self.filepath, "w")
        for ni in new_items:
            f.write(ni)
        f.close()

        self.menu_pos -= 1
        self.clear_topics() #TODO rename
        self.update_topics() #TODO rename
