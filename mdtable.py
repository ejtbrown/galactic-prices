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
        self.__iter_row__ = -1

        if self.raw is not None:
            self.parse(self.raw)

    def __iter__(self):
        self.__iter_row__ = 0
        return self

    def __next__(self):
        if self.__iter_row__ >= len(self.table):
            raise StopIteration

        d_out = self.row(self.__iter_row__)
        self.__iter_row__ += 1
        return d_out

    def row(row_num):
        # Make a dict from the row, where names are keys
        d_out = dict()
        for i in range(0, len(self.header)):
            d_out[self.header[i]] = self.table[row_num][i]
        
        return d_out

    def find(index, match):
        # If index is a name, lookup the associated header
        if issubclass(type(index), str):
            for i in range(0, len(self.header)):
                if self.header[i] == index:
                    index = i
                    break

        # Find the matching row
        for i in range(0, len(self.table)):
            if self.table[i][index] == match:
                return self.row(i)

        return None

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

        if issubclass(type(md_file), str):
            lines = md_file.splitlines()
        else:
            lines = md_file.readlines()
            if len(lines) < 3:
                return

        line = 0
        accumulate = ''
        while line < len(lines):
            if len(lines[line]) > 0:
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


