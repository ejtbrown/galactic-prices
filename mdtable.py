#!/usr/bin/env python3
"""
mdtable.py - parser for tables in markdown format

Authors:
  Erick Brown

Copyright:
  2022, Erick Brown

Warranty:
  None - use this software at your own risk!
"""

class MdTable(object):
    def __init__(self, parse=None):
        self.raw = parse
        self.table = list()
        self.header = list()
        self.title = ''

        if self.raw is not None:
            self.parse(self.raw)

    def parse(self, raw):
        self.raw = raw
        lines = self.raw.splitlines()

        # Find the first line of the table
        start_of_table = -1
        for line in range(0, len(lines)):
            if len(lines[line]) > 0:
                if lines[line][0] == '|':
                    start_of_table = line
                    break

        if start_of_table == -1:
            return False

        # See if there's a title available
        for line in range(start_of_table - 1, -1, -1):
            if lines[line].strip() != '':
                self.title = lines[line].strip().replace('*', '')

        # Parse the header line
        for cell in lines[start_of_table].split('|')[1:-1]:
            self.header.append(cell.strip().replace('*', ''))

        # Parse the body of the table
        if len(lines) < start_of_table + 2:
            # Nothing to parse; this is an empty table
            return True

        for row in range(start_of_table + 2, len(lines)):
            self.table.append(list())
            for cell in lines[row].split('|')[1:-1]:
                self.table[-1].append(cell.strip().replace('*', ''))

    def rc(self, row, column):
        if row < 0 or column < 0:
            raise IndexError('row and column cannot be below 0')

        if row >= len(self.table):
            raise IndexError('row ' + str(row) + ' out of range (' + str(len(self.table)) + ')')

        if column >= len(self.table[row]):
            raise IndexError('column ' + str(column) + ' out of range (' + str(len(self.table[row])) + ')')

        return self.table[row][column]


class MdFile(object):
    def __init__(self, md_file):
        self.tables = list()

        if issubclass(str, md_file):
            lines = md_file.splitlines()
        else:
            lines = md_file.readlines()
            if len(lines) < 3:
                return

        line = 0
        accumulate = ''
        while line < len(lines):
            if lines[line][0] == '|':
                accumulate = '\n'.join(lines[line-2:line-1])
                while line < len(lines):
                    if len(lines[line]) > 0:
                        if lines[line][0] == '|':
                            accumulate += lines[line]
                        else:
                            self.tables.append(MdTable(accumulate))
                            accumulate = ''
                            break
                    line += 1

            line += 1
            if accumulate != '':
                self.tables.append(MdTable(accumulate))


