#!/usr/bin/python
from mod.Win import *
from os import mkdir

def create_dir(directory):
    try:
        mkdir(directory)
    except:
        pass

create_dir("data")
create_dir("data/tileset")
create_dir("data/map")
create_dir("data/sprite/")
create_dir("data/sprite/enemy/")
create_dir("data/sprite/element/")
create_dir("data/core/")
create_dir("data/event/")

app = qt.QApplication(argv)

win = Win()
win.show()

exit(app.exec_())
