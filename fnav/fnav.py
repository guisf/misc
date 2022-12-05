#!/usr/bin/python2
# -*- coding: utf-8 -*-

"""fnav: file navigator

This is a simple file manager with curses interface. It should run
on a linux terminal like xterm or other terminals that support colors.

Send any bug or sugestion to the author's email.

"""

__author__ = 'Guilherme Starvaggi França <guifranca@gmail.com>'
__date__ = '2010-02-19'
__version__ = '0.1'

import sys
import os
import curses

import navigator

def main(stdscr, dir):
    curses.curs_set(0)
    nav = navigator.Navigator(stdscr, dir)
    try:
        nav.run()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    if len(sys.argv) > 1:
        dir = sys.argv[1]
        if not os.path.isdir(dir):
            print("Error: '%s' is not a directory" % dir)
            sys.exit(1)
    else:
        dir = os.getcwd()
    curses.wrapper(main, dir)

