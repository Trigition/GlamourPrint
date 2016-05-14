#!/usr/bin/env python

import GlamourPrint as gp
from math import floor

class FuzzyBar():

    def __init__(self,
                 max_value=100, current_value=0,
                 delta=10,
                 format_str="Status: [$(bar)] $(status)",
                 status_message=["Little Progress", "Halfway there", "Nearly Done", "Overflow!"],
                 status_color = ["blue", "yellow", "green", "red"]):
        self.fuzzy_max = max_value
        self.current_value = current_value
        self.delta = delta
        self.format_str = format_str
        self.status_messages = status_message
        self.status_colors = status_color
        self.format = self.__parse_format()

    def increment(self, amount):
        self.current_value += amount

    def set_current(self, amount):
        self.current_value = amount

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
        # For each regex return, determine their format and if they are correct specifiers
        for group in operation_groups:
            string_literal = self.format[current_index : group.start()]
            operation = self.determine_operation(group.group(0))
            bar_format.append(string_literal)
            bar_format.append(operation)
            prev_group = group
            current_index = group.end()
        if current_index < len(self.format) - 1:
            string_literal = self.format[current_index:]
            bar_format.append(string_literal)
        return bar_format

    def __status(self):
        # Determine number of defined status messages
        num_status = len(self.status_messages)
        message_index = floor(num_status * self.__percent_done())

    def __percent_done(self):
        return float(self.current_value / self.max_value)

    def determine_operation(self, match):
        """This method determines the operations specified in the format string and returns the
           corresponding function.

        Keyword arguments:
        match   -- The string specifier to be matched with a function.
                    $(bar) : A progress bar
                    $(percent) : The percentage of completion
                    $(status) : The status message

        """
        operation_dict = {"$(bar)": self.__create_bar,
                          "$(status)": self.__update_percent,
                          "$(current)": self.__current}
        match = match.lower().strip('\n') # Sanitize the string
        try:
            return operation_dict[match]
        except KeyError:
            return None
