#!/usr/bin/python3
# vim: ts=4 sw=4 et ft=py

import curses
import os


class Topics:
    filepath = ""
    num_topics = 0
    topic_names = []
    is_menu_active = False
    menu_pos = 0


    def __init__(self):
        self.update_topics()


    def update_topics(self):
        # get full filepath
        dirname = os.path.dirname(__file__)
        self.filepath = os.path.join(dirname, "topics")

        # get topics from file
        for line in open(self.filepath, "r"):
            self.topic_names.append(line)

        # get num of topics
        self.num_topics = len(self.topic_names)


    def new_topic(self, height, width):
        new_t = ""

        twin = curses.newwin(3, 50, (height // 2), (width // 2) - 25)
        twin.border()
        curses.echo()
        y, x = twin.getyx()
        twin.addstr(y + 1, x + 1, "New topic: ")
        twin.refresh()

        # getstr() returns a byte object rather than a string
        # this means, it must be decoded first
        # python3 problem only
        new_t = twin.getstr().decode(encoding="utf-8") + '\n'

        # write new topic to file
        f = open(self.filepath, "a")
        f.write(new_t)
        f.close()

        self.update_topics()
