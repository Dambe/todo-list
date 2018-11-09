#!/usr/bin/python3
# vim: ts=4 sw=4 et ft=py

import curses
import os


class Lists:
    filepath = ""
    num_items = 0
    items = []
    is_menu_active = False

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
