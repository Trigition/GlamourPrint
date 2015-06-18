#!/usr/bin/env python

import GlamourPrint as gp
from math import floor
import re
import inspect

class Progress_Bar():

    def __init__(self, max_value, current_value=0, width=10, format_str="", complete=".", incomplete=" "):
        self.max_value = max_value
        self.current_value = current_value
        self.width = width
        self.format = format_str
        self.percent_format = "%6.2f%% "
        self.complete = complete
        self.incomplete = incomplete
        self.complete_color = None
        self.incomplete_color = None
        self.bar_format = self.__parse_format()

    def increment(self, amount):
        self.current_value += amount
        self.__print_bar()

    def set_current(self, amount):
        self.current_value = amount
        self.__print_bar()

    def __parse_format(self):
        """
        This method creates a list of operations to perform in order to update the progress
        bar. This list consists of string literals and function objects (which return strings)
        that are appended to each other to finalize the construction of the string.
        """
        bar_format = []
        regex = re.compile('\$\((.*?)\)')
        # Find format specifications
        operation_groups = re.finditer(regex, self.format)
        current_index = 0
        prev_group = None
        for group in operation_groups:
            string_literal = self.format[current_index : group.start()]
            # print "String Literal:", string_literal
            operation = self.determine_operation(group.group(0))
            bar_format.append(string_literal)
            bar_format.append(operation)
            prev_group = group
            current_index = group.end()
        if current_index < len(self.format) - 1:
            string_literal = self.format[current_index:]
            bar_format.append(string_literal)
        return bar_format

    def __create_bar(self):
        """
        This method constructs the progress bar string to be printed to standard out
        """
        progress = float(self.current_value) / float(self.max_value)
        num_completed = floor(progress * self.width)
        num_completed = int(num_completed)
        num_incomplete = self.width - num_completed
        complete_string = self.complete * num_completed
        incomplete_string = self.incomplete * num_incomplete
        # Color 'complete' characters, if specified
        if self.complete_color is not None:
            complete_string = gp.colored_string([complete_string], [self.complete_color])
        # Color 'incomplete' characters, if specified
        if self.incomplete_color is not None:
            incomplete_string = gp.colored_string([incomplete_string], [self.incomplete_color])

        progress_string = complete_string + incomplete_string
        return progress_string

    def __print_bar(self):
        """
        This method sends the constructed bar string to GlamourPrint to have standard out updated.
        """
        #@TODO Ensure that this will perform reliably on other terminals.
        bar = ""
        for bar_format in self.bar_format:
            if inspect.ismethod(bar_format):
                bar += bar_format()
            elif type(bar_format) is str:
                bar += bar_format
        gp.reprint(bar)

    def __update_percent(self):
        progress = float(self.current_value) / float(self.max_value) * 100
        return self.percent_format % progress

    def determine_operation(self, match):
        operation_dict = {"$(bar)": self.__create_bar, "$(percent)": self.__update_percent}
        match = match.lower().strip('\n')
        # print "Matching:", match
        try:
            return operation_dict[match]
        except KeyError:
            return None

    def set_complete_color(self, color):
        """
        This method sets the color for the characters representing completion
        on the progress bar.
        """
        self.complete_color = color

    def set_incomplete_color(self, color):
        """
        This method sets the color for the characters representing incomplete progress.
        """
        self.incomplete_color = color

    def set_complete_char(self, char):
        """
        This method sets the character representing completed progress. This method enforces single characters.
        """
        self.complete = char[0]

    def set_incomplete_char(self, char):
        """
        This method sets the character representing incomplete progress. This method enforces single characters.
        """
        self.incomplete = char[0]
