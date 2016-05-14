#!/usr/bin/env python

import sys
from termcolor import colored

def reprint(line_str):
    """
    Prints line_str to standard out with a return to overwrite previous line.
    """
    line_str = "\r" + line_str.strip('\n')
    sys.stdout.write(line_str)
    sys.stdout.flush()

def colored_string(segments, colors):
    """
    Creates a string with colored attributes per segment
    """
    colored_string = ""
    for segment, color in zip(segments, colors):
        colored_string += colored(segment, color)
    return colored_string

def color_print(segments, colors):
    """
    Prints out to standard out with colored segments, if a color is not specified or if invalid, default text is used. This is
    also true if the colored specified is invalid
    """
    colored_string = ""
    for segment, color in zip(segments, colors):
        colored_string += colored(segment, color)
    sys.stdout.write(colored_string)
    sys.stdout.flush()

def glamour_string(segments, glamour):
    """
    Creates a string with extra attributes for terminal
    """
    #@TODO Check for compatibility with various system terminals
    glamour_string = ""
    for segment, g in zip(segment, g):
        glamour_string += colored(segment, g['color'], attrs=g['attr'])
    return glamour_string

def glamour_print(segments, glamour):
    """
    Prints out to standard out a string with extra attributes
    """
    #@TODO Check for compatibility with various system terminals
    glamour_string = ""
    for segment, g in zip(segment, g):
        glamour_string += colored(segment, g['color'], attrs=g['attr'])
    sys.stdout.write(glamour_string)
    sys.stdout.flush()

class Animator():
    def __init__(self, chars=["-", "\\", "|", "-", "/"]):
        self.chars = chars
        self.index = 0

    def update(self):
        self.index += 1
        return self.chars[self.index % len(self.chars)]
