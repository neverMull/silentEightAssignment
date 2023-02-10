class Strip:
    def __init__(self, start, stop, state, island_index):
        self.start = start
        self.stop = stop
        self.state = state
        self.island_index = island_index

    def explore(self, arr):
        while self.stop < len(arr):
            next_step = self.stop + 1
            if next_step >= len(arr):
                return self
            if arr[next_step] == 0:
                return self
            if arr[next_step] == 1:
                self.stop = next_step

    def is_touching(self, strip):
        min_range = max(self.start - 1, 0)
        max_range = self.stop + 2

        if strip.start in range(min_range, max_range):
            return True
        if strip.stop in range(min_range, max_range):
            return True

        return False


def strip_finder(arr):
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
    :return: a tuple with the updated top row and bottom row respectively
    """
    updated_bottom_row = []

    for current_strip in top_row:
        for bottom_strip in bottom_row:
            if current_strip.is_touching(bottom_strip):
                current_strip.state = 'open'
                # if the current strip is touching a bottom strip with an existing island index
                # it inherits that island index since it is connected to that island via the bottom strip
                if bottom_strip.island_index:
                    current_strip.island_index = bottom_strip.island_index
                else:
                    bottom_strip.island_index = current_strip.island_index
                continue
            # if the bottom strip is fully to the left of the current strip it will
            # be to the left of all other strips in the top row
            if current_strip.start > bottom_strip.stop:
                irrelevant = bottom_row.pop(0)
                updated_bottom_row.append(irrelevant)
                continue

            if current_strip.stop < bottom_strip.start:
                break

    updated_bottom_row = updated_bottom_row + bottom_row

    return top_row, updated_bottom_row


def island_counter(row):
    islands = set()
    open_islands = set()
    for strip in row:
        islands.add(strip.island_index)
        if strip.state == 'open':
            open_islands.add(strip.island_index)

    islands_explored: int = len(islands) - len(open_islands)

    return islands_explored


def solution(filename):
    total_islands = 0
    max_island_index = 0
    top_row = []

    with open(filename) as contents:
        for line in contents:
            processed_line = [int(char) for char in line.strip()]
            bottom_row = strip_finder(processed_line)
            top_row, bottom_row = strip_state_finder(top_row, bottom_row)
            total_islands += island_counter(top_row)
            for element in bottom_row:
                if not element.island_index:
                    element.island_index = max_island_index
                    max_island_index += 1
            top_row, bottom_row = bottom_row, []

        total_islands += island_counter(top_row)

    return total_islands
