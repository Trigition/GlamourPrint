#!/usr/bin/env python

import GlamourPrint as gp
from math import floor
import re
import inspect

class Progress_Bar():

    def __init__(self,
                 max_value, current_value=0,
                 width=10,
                 format_str="PROGRESS BAR V.01 $(percent): [$(bar)] $(status)",
                 complete=".", incomplete=" ",
                 current_message="", finish_message="Done!", overflow_message="Overflow!",
                 current_animation=None):
        """The constructor of a Progress Bar.

        Keyword arguments:
        max_value         -- The maximum value to be associated with the progress bar
        current_value     -- The current value for the progress bar, this can be over
                            the maximum value. An alert can be specified if this
                            occurs. (default 0)
        width             -- The character width of the progress bar. Must be a positive
                            integer. (default 10)
        format_str        -- This is a string formatter for the progress bar. This allows
                            specification of both string literals and operations. For
                            example "Static string $(bar)" will create a
                            progress bar that will have the format of
                            "Static string" [PROGRESS_BAR]. See the documentation for all
                            the operations available. Improper format names are handled.
                            (default "PROGRESS BAR V.01 $(percent): [$(bar)] $(status)")
        complete          -- The single character to represent progress completed in the bar.
                            Please note that non-ascii characters, specifically for left->right
                            oriented languages are not supported and may have undesirable output.
                            (default ".")
        incomplete        -- The single character to represent yet-to-be completed progress in
                            the progress bar. Please note that non-ascii characters are not
                            supported and may have undesirable output.
        current_message   -- The message to be printed while the progress bar is below 100%.
                            (default "")
        finish_message    -- The message to be printed once the progress bar reaches 100%.
                            (default "Done!")
        overflow_message  -- The message to be printed once the progress bar goes over 100%.
                            (default "Overflow!")
        current_aniamtion -- A list of characters for an animation to be played while progress
                            is less than 100%. WARNING: If specified, this animation will
                            override any messages specified for current_message.
                            (default None)

        """
        self.max_value = max_value
        self.current_value = current_value

        self.width = width
        self.format = format_str
        self.percent_format = "%6.2f%%"

        self.complete = complete
        self.incomplete = incomplete

        self.complete_color = None
        self.incomplete_color = None

        self.current_message = current_message
        self.finish_message = finish_message
        self.overflow_message = overflow_message

        # Determine order of strings and operations for progress bar.
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

    def __create_bar(self):
        """This method constructs the progress bar string to be printed to standard out
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

    def __status(self):
        """This method returns the status string"""
        progress = float(self.current_value) / float(self.max_value) * 100
        if progress < 100.0 and self.current_message is not None:
            return self.current_message
        elif progress == 100.0 and self.finish_message is not None:
            return self.finish_message
        elif progress > 100.0 and self.overflow_message is not None:
            return self.overflow_message
        # Corresponding message string is None.
        return ""

    def __print_bar(self):
        """This method sends the constructed bar string to GlamourPrint to have standard out updated."""
        #@TODO Ensure that this will perform reliably on other terminals.
        bar = ""
        for bar_format in self.bar_format:
            if inspect.ismethod(bar_format):
                bar += bar_format()
            elif type(bar_format) is str:
                bar += bar_format
        gp.reprint(bar)

    def __update_percent(self):
        """This method returns a percentage of completion as a string"""
        progress = float(self.current_value) / float(self.max_value) * 100
        return self.percent_format % progress

    def determine_operation(self, match):
        """This method determines the operations specified in the format string and returns the
           corresponding function.

        Keyword arguments:
        match   -- The string specifier to be matched with a function.
                    $(bar) : A progress bar
                    $(percent) : The percentage of completion
                    $(status) : The status message

        """
        operation_dict = {"$(bar)": self.__create_bar, "$(percent)": self.__update_percent, "$(status)": self.__status}
        match = match.lower().strip('\n') # Sanitize the string
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
