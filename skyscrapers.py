"""
LAB1 TASK1
GitHub: https://github.com/S-Daria/Lab0_Task1.git
"""


def read_input(path: str):
    """
    Read game board file from path.
    Return list of str.
    >>> read_input("check.txt")
    ['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***']
    """
    lines_list = []
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            lines_list.append(line[:-1])
    return lines_list


def split_board(lines_list: list) -> list:
    """
    splits str lines and return list of tuples,
    where each tuple except first and last contains
    first element is left visibility
    second element is right visibility
    third element is tuple with elements in line

    first and last tuples contain splitted line from 1st to 5th element

    >>> split_board(['***21**', '452453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    [('*', '*', '2', '1', '*'), ('4', '*', ('5', '2', '4', '5', '3')), \
('4', '*', ('2', '3', '1', '4', '5')), ('*', '5', ('5', '4', '3', '2', '1')), \
('*', '*', ('3', '5', '2', '1', '4')), ('*', '*', ('4', '1', '5', '3', '2')), \
('2', '*', '1', '*', '*')]
    >>> split_board(['452453*'])
    [('5', '2', '4', '5', '3')]
    """
    splitted_board = []
    for index, line in enumerate(lines_list):
        if index % 6 == 0:
            line_tuple = tuple(line[1:-1])
        else:
            line_tuple = (line[0], line[-1], tuple(line[1:-1]))
        splitted_board.append(line_tuple)
    return splitted_board


def left_to_right_check(input_line: str or tuple, pivot: int):
    """
    Check row-wise visibility from left to right.
    Return True if number of building from the left-most hint is visible looking to the right,
    False otherwise.

    input_line - representing board row as a string or as a tuple of elements in row
    pivot - number on the left-most hint of the input_line.

    >>> left_to_right_check("412453*", 4)
    True
    >>> left_to_right_check("452453*", 5)
    False
    """
    if pivot == "*":
        return True
    pivot = int(pivot)
    if isinstance(input_line, str):
        line = split_board([input_line])[0]
    else:
        line = input_line
    max_num = 0
    visible_counter = 0
    for _, number in enumerate(line):
        if int(number) > max_num:
            visible_counter += 1
            max_num = int(number)
    if visible_counter == pivot:
        return True
    return False


def check_not_finished_board(board: list):
    """
    Check if skyscraper board is not finished, i.e., '?' present on the game board.

    Return True if finished, False otherwise.

    >>> check_not_finished_board(['***21**', '4?????*', '4?????*', \
        '*?????5', '*?????*', '*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*', \
        '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*', \
        '*5?3215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    for line in board:
        if '?' in line:
            return False
    return True


def check_uniqueness_in_rows(board: list):
    """
    Check buildings of unique height in each row.

    Return True if buildings in a row have unique length, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', \
        '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*', \
        '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', \
        '*553215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    if len(board) == 5:
        splitted_board = board
    else:
        splitted_board = split_board(board)[1: -1]
    for line in splitted_board:
        if {'1', '2', '3', '4', '5'} != set(line[2]):
            return False
    return True


def check_horizontal_visibility(board: list):
    """
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
     i.e., for line 412453* , hint is 4, and 1245 are the four buildings
      that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', \
        '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', \
        '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', \
        '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    if len(board) == 5:
        splitted_board = board
    else:
        splitted_board = split_board(board)[1: -1]
    for line in splitted_board:
        if not left_to_right_check(line[2], line[0]) or \
                not left_to_right_check(tuple(reversed(line[2])), line[1]):
            return False
    return True


def invert_board(board: list):
    """
    inverts board that all columns become lines
    >>> invert_board(['***21**', '452453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***'])
    [('*', '2', ('5', '2', '5', '3', '4')), ('*', '*', ('2', '3', '4', '5', '1')), \
('2', '1', ('4', '1', '3', '2', '5')), ('1', '*', ('5', '4', '2', '1', '3')), \
('*', '*', ('3', '5', '1', '4', '2'))]
    """
    splitted_board = split_board(board)
    new_splitted_board = []
    for column_indx, _ in enumerate(splitted_board[1: -1][0][2]):
        line_from_column_list = []
        for line in splitted_board[1: -1]:
            line_from_column_list.append(line[2][column_indx])
        new_splitted_board.append((splitted_board[0][column_indx],
                                   splitted_board[-1][column_indx],
                                   tuple(line_from_column_list)))
    return new_splitted_board


def check_columns(board: list):
    """
    Check column-wise compliance of the board
    for uniqueness (buildings of unique height)
    and visibility (top-bottom and vice versa).

    Same as for horizontal cases,
    but aggregated in one function for vertical case, i.e. columns.

    >>> check_columns(['***21**', '412453*', '423145*', \
        '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_columns(['***21**', '412453*', '423145*', \
        '*543215', '*35214*', '*41232*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*', \
        '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    splitted_inverted_board = invert_board(board)
    if not check_uniqueness_in_rows(splitted_inverted_board) or \
            not check_horizontal_visibility(splitted_inverted_board):
        return False
    return True


def check_skyscrapers(input_path: str):
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.

    >>> check_skyscrapers("check.txt")
    True
    """
    board = read_input(input_path)
    if not check_not_finished_board(board) or \
        not check_uniqueness_in_rows(board) or \
        not check_horizontal_visibility(board) or \
            not check_columns(board):
        return False
    return True


if __name__ == "__main__":
    print(check_skyscrapers("check.txt"))
