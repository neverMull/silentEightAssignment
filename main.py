import sys
import getopt


class Strip:
    def __init__(self, start, stop, state, island_index):
        self.start = start
        self.stop = stop
        self.state = state
        self.island_index = island_index

    def explore(self, arr):
        """
        traverses a row to find where a given strip ends and records that ending index
        :param arr: the row that is being explored
        :return: a strip with an updated ending index
        """
        while self.stop < len(arr):
            next_step = self.stop + 1
            if next_step >= len(arr):
                return self
            if arr[next_step] == 0:
                return self
            if arr[next_step] == 1:
                self.stop = next_step

    def is_touching(self, strip):
        """
        :param strip: the strip one strip is being compared against
        :return: If the two strips are in contact with each other
        """
        top_span = set(range(self.start-1, self.stop+2))
        bottom_span = set(range(strip.start, strip.stop+1))
        if top_span & bottom_span:
            return True
        return False


def strip_finder(arr):
    """
    :param arr:
    :return: A list of strips found in a given line
    """
    row_len = len(arr)
    index = 0
    strips = []

    while index < row_len:
        value = arr[index]
        if value == 1:
            new_strip = Strip(start=index, stop=index, state='closed', island_index=None)
            new_strip.explore(arr)
            strips.append(new_strip)
            index = new_strip.stop + 1
        else:
            index += 1

    return strips


def strip_state_finder(top_row, bottom_row):
    """
    This function compares all strips of lands in the top row against all strips of land
    in the bottom row to determine if the strip of land terminates or extends into the row
    bellow it.
    :param top_row: the row being actively explored
    :param bottom_row: the row bellow the row that is being explored
    :return: a tuple with the updated top and bottom row in that order
    """
    bottom_row = bottom_row
    updated_top_row = []

    for top_strip in top_row:
        start = 0
        for i in range(start, len(bottom_row)):
            bottom_strip = bottom_row[i]
            if top_strip.is_touching(bottom_strip):
                top_strip.state = 'open'
                # if the current strip is touching a bottom strip with an existing island index
                # it inherits that island index since it is connected to that island via the bottom strip
                if bottom_strip.island_index:
                    top_strip.island_index = bottom_strip.island_index
                else:
                    bottom_strip.island_index = top_strip.island_index

                bottom_row[i] = bottom_strip

            # if the bottom strip is fully to the left of the current strip it will
            # be to the left of all other strips in the top row
            elif bottom_strip.stop + 1 < top_strip.start:
                start += 1

            elif bottom_strip.start + 1 > top_strip.stop:
                break

        updated_top_row.append(top_strip)

    return updated_top_row, bottom_row


def island_counter(row):
    """
    :param row: A list of strips belonging to a line of text
    :return: The number of islands fully explored in a line
    """
    islands = set()
    open_islands = set()
    for strip in row:
        islands.add(strip.island_index)
        if strip.state == 'open':
            open_islands.add(strip.island_index)

    islands_explored: int = len(islands) - len(open_islands)

    return islands_explored


def solve(filename):
    """
    Takes in a file path, and counts the number of distinct islands found
    :param filename: the file path to be explored
    :return: the number of islands found
    """
    total_islands = 0
    max_island_index = 0
    top_row = []

    with open(filename) as contents:
        for index, line in enumerate(contents):
            try:
                processed_line = [int(char) for char in line.strip()]
            except:
                sys.exit(f'non integer character at line {index+1}')
            for element in top_row:
                if not element.island_index:
                    element.island_index = max_island_index
                    max_island_index += 1
            bottom_row = strip_finder(processed_line)
            top_row, bottom_row = strip_state_finder(top_row, bottom_row)
            total_islands += island_counter(top_row)
            top_row, bottom_row = bottom_row, []

        total_islands += island_counter(top_row)

    sys.stdout.write(str(total_islands))


if __name__ == "__main__":
   solve(sys.argv[1])