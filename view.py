from consolemenu import *
from consolemenu.items import *


class View:
    def print(self, data):
        titles, rows = data
        line_len = 30 * len(titles)

        self.print_separator(line_len)
        self.print_row(titles)
        self.print_separator(line_len)

        for row in rows:
            self.print_row(row)
        self.print_separator(line_len)

    @staticmethod
    def print_row(row):
        for col in row:
            print(str(col).rjust(26, ' ') + '   |', end='')
        print('')

    @staticmethod
    def print_separator(length):
        print('-' * length)
