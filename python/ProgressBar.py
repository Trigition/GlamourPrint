#!/usr/bin/env python

import GlamourPrint as gp
import re
import inspect
import time
from math import floor
from math import sqrt

class Progress_Bar():

    def __init__(self,
                 max_value, current_value=0,
                 width=10,
                 format_str="PROGRESS BAR V.01 $(percent): [$(bar)] $(status)",
                 current=">", complete="=", incomplete=" ",
                 current_message="", finish_message="Complete", overflow_message="Overflow!",
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
        current           -- The single character to represent the current index of progress.
                            (default ">")
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
                            (default "Complete")
        overflow_message  -- The message to be printed once the progress bar goes over 100%.
                            (default "Overflow!")
        current_animation -- A list of characters for an animation to be played while progress
                            is less than 100%. WARNING: If specified, this animation will
                            override any messages specified for current_message.
                            (default None)

        """
        self.max_value = max_value
        self.current_value = current_value

        self.width = width
        self.format = format_str
        self.percent_format = "%6.2f%%"

        self.current = current
        self.complete = complete
        self.incomplete = incomplete

        self.complete_color = None
        self.incomplete_color = None

        self.current_message = current_message
        self.finish_message = finish_message
        self.overflow_message = overflow_message

        if (current_animation is not None):
            self.animation = gp.Animator(current_animation)
        else:
            self.animation = None

        # Determine order of strings and operations for progress bar.
        self.bar_format = self.__parse_format()

        # Create time instanced
        self.begin_time = time.time()
        self.prev_time = self.begin_time
        self.total_time = 0
        self.total_square_time = 0

    def increment(self, amount):
        """This method increments the current_value by a specified amount

        Keyword arguments:
        amount  -- The amount to increment current_value by. Allowed to be
                   negative. If the amount would push current_value negative,
                   then the current_value is simply rounded to 0.
        """
        if self.current_value + amount < 0:
            self.current_value = 0
        else:
            self.current_value += amount
        self.__print_bar()

    def set_current(self, value):
        """This method sets the current_value to a specified value.

        Keyword arguments:
        value -- The value to set to current_value. Not allowed to be negative.
                 Any negative values will be rounded to 0.
        """
        if value < 0:
            self.current_value = 0
        else:
            self.current_value = value
        self.__print_bar()

    def set_percent_done(self, percent):
        """This method allows specification of how much progress has been made.

        Keyword arguments:
        percent -- A value in the range of [0.0, 1.0]. Values above 100.0 are supported.
                   However, negative values are not and will subsequently be treated as 0.
        """
        if percent < 0.0:
            self.current_value = 0
        else:
            self.current_value = percent * self.max_value
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
        """This method constructs the progress bar string to be printed to standard out"""
        progress = float(self.current_value) / float(self.max_value)
        num_completed = floor(progress * self.width)
        num_completed = int(num_completed)
        num_incomplete = self.width - num_completed
        # Add a current index character if specified and if progress is not complete
        if self.current is not None and num_completed < self.width:
            complete_string = (self.complete * num_completed) + self.current
            incomplete_string = self.incomplete * (num_incomplete - 1)
        else:
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
            if self.animation is None:
                return self.current_message
            # Animation has been specified
            return self.animation.update()
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

    def __time_estimate(self):
        """This method performs a Monte Carlo esque estimation of time to completion"""
        #@TODO Implement time estimates
        #@TODO Currently I need a better way of keeping track of a starting time and calculating
        # elapsed time....
        # Perform updates on time values
        current_time = time.time()
        elapsed_time = int((current_time - self.prev_time))
        self.prev_time = current_time
        self.total_time += elapsed_time
        self.total_square_time += elapsed_time**2
        # Estimate time remaining
        if self.current_value is 0:
            # No progress has been made
            return "INF"
        sigma = sqrt(abs(self.total_square_time - (self.total_time**2)))
        scaling = float(self.max_value - self.current_value) / float(self.current_value)
        lower_bound = self.total_time * scaling - 3 * sigma * sqrt(scaling)
        upper_bound = self.total_time * scaling + 3 * sigma * sqrt(scaling)
        time_string = "Upper: %ds, Lower: %ds, Sigma:%d, Scale:%f" % (upper_bound, lower_bound, sigma, scaling)
        return time_string

    def __current(self):
        """This method returns the current value"""
        #@TODO Allow specification of a unit associated with the value
        return str(self.current_value)

    def determine_operation(self, match):
        """This method determines the operations specified in the format string and returns the
           corresponding function.

        Keyword arguments:
        match   -- The string specifier to be matched with a function.
                    $(bar) : A progress bar
                    $(percent) : The percentage of completion
                    $(status) : The status message
                    $(time) : A time estimate for completion
                    $(current) : The current value

        """
        operation_dict = {"$(bar)": self.__create_bar,
                          "$(percent)": self.__update_percent,
                          "$(status)": self.__status,
                          "$(time)": self.__time_estimate,
                          "$(current)": self.__current}
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
