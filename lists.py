#!/usr/bin/python3
# vim: ts=4 sw=4 et ft=py

import curses
import os

class Item:
    description = ""
    done = False
    due_date = ""
    prio = 0

    def __init__(self, desc):
        self.description = desc
        pass


class List(Item):
    dirname = ""
    lists = []
    items = []
    items_test = []
    is_topic_menu_active = True
    is_list_menu_active = False
    topic_menu_pos = 1
    list_menu_pos = 1


    def __init__(self):
        # get full folderpath
        self.dirname = os.path.join(os.path.dirname(__file__), "lists/")
        self.update_lists()
        self.show_list()


    def clear_lists(self):
        self.lists = []


    def update_lists(self):
        # get list names
        for filename in sorted(os.listdir(self.dirname)):
             self.lists.append(filename)


    def new_list(self, height, width):
        new_l = ""

        twin = curses.newwin(3, 50, (height // 2), (width // 2) - 25)
        twin.border()
        curses.echo()
        y, x = twin.getyx()
        twin.addstr(y + 1, x + 1, "New list: ")
        twin.refresh()

        # getstr() returns a byte object rather than a string
        # this means, it must be decoded first
        # python3 problem only
        new_l = twin.getstr().decode(encoding="utf-8")

        # create a new file
        filepath = filepath = os.path.join(self.dirname, new_l)
        if (new_l not in self.lists) and (new_l != "\n"):
            f = open(filepath, "w+")
            f.close()

        self.clear_lists()
        self.update_lists()


    def delete_list(self):
        filepath = os.path.join(self.dirname, self.lists[self.topic_menu_pos - 1])
        # TODO: double confirmation before delete
        os.remove(filepath)

        self.topic_menu_pos -= 1
        self.clear_lists()
        self.update_lists()


    def show_list(self):
        filepath = os.path.join(self.dirname, self.lists[self.topic_menu_pos - 1])
        self.items = []
        for line in open(filepath, "r"):
            if line not in self.items:
                self.items.append(line)


    def rename_list(self, height, width):
        old_file = os.path.join(self.dirname, self.lists[self.topic_menu_pos - 1])

        twin = curses.newwin(3, 50, (height // 2), (width // 2) - 25)
        twin.border()
        curses.echo()
        y, x = twin.getyx()
        twin.addstr(y + 1, x + 1, "New name: ")

        # getstr() returns a byte object rather than a string
        # this means, it must be decoded first
        # python3 problem only
        new_name = twin.getstr().decode(encoding="utf-8")
        new_file = os.path.join(self.dirname, new_name)

        os.rename(old_file, new_file)

        self.clear_lists()
        self.update_lists()


    def new_item(self, height, width):
        twin = curses.newwin(3, 50, (height // 2), (width // 2) - 25)
        twin.border()
        curses.echo()
        y, x = twin.getyx()
        twin.addstr(y + 1, x + 1, "Description: ")

        # getstr() returns a byte object rather than a string
        # this means, it must be decoded first
        # python3 problem only
        new_item = twin.getstr().decode(encoding="utf-8")
        self.items_test.append(Item(new_item))
        pass
