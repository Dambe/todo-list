#!/usr/bin/python3
# vim: ts=4 sw=4 et ft=py

import os

class Topics:
    filepath = ""
    num_topics = 0
    topic_names = []
    is_menu_active = False
    menu_pos = 0

    def __init__(self):
        # get full filepath
        dirname = os.path.dirname(__file__)
        self.filepath = os.path.join(dirname, "topics")

        # get topics from file
        for line in open(self.filepath, "r"):
            self.topic_names.append(line)

        # get num of topics
        self.num_topics = len(self.topic_names)

    def new_topic(self):
        new_t = input("Topic name: ")

        f = open(self.filepath, "a")
        f.write(new_t)
        f.close()
