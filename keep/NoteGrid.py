"""Helper functions for printing out grid of notes or just one note. These
functions assist with the printing of a grid of notes in tandem with a Google
Keep object and a nested list of notes.

Author: Zachary Ashen
Date: June 3rd 2020
"""

import re
from textwrap import fill
import os

import gkeepapi

columns, rows = os.get_terminal_size()
width = columns

columnEndPos = 0


def listify_google_notes(google_notes):
    """Returns: a nested list from a Google Note object. Checked items are removed from the list.

    Example: Google Note object with list titled 'Foo List' and items:
    'get apples', "pick up groceries" and a note titled 'Foo Note' with text:
    'Garbage in garbage out the end of this note', becomes:
    [[["Foo List"], ["get apples"], ["pick up gorceries"]],
    [["Foo Note"], ["Garbage in garbage out"], ["the end of this note"]]

    Precondition: googleNote is a list containing either items of type
    'gkeepapi.node.List' or 'gkeepapi.node.Note'"""

    # This is the list accumulator that recieves the parsed Google Notes
    note_list = []
    for index in range(len(google_notes)):
        # execute if note is a list
        if type(google_notes[index]) == gkeepapi.node.List:
            # Only retrieve unchecked list items
            unchecked_list = google_notes[index].unchecked
            note_title = google_notes[index].title
            # get the string text of the list and change the list item to the string
            for i in range(len(unchecked_list)):
                unchecked_list[i] = '□  ' + unchecked_list[i].text
            note_list.append(unchecked_list)
            unchecked_list.insert(0, note_title)
        # execute of note is a note
        else:
            note = google_notes[index]
            note_title = note.title
            note = note.text.split('\n')
            note_list.append(note)
            note.insert(0, note_title)
    return note_list


def wrap_text(nested_list):
    for index in range(len(nested_list)):
        for i in range(len(nested_list[index])):
            if len(nested_list[index][i]) > (width - 25):

                nested_list[index][i] = fill(nested_list[index][i], width=(width - 22))

                unwrapped_text = nested_list[index][i]

                # nestedList[index][i][width-30:width-20].split(' ')
                wrapped_text_list = nested_list[index][i].split('\n')
                # print(wrapped_text_list)
                for a in range(len(wrapped_text_list)):
                    nested_list[index].insert(i + (a), wrapped_text_list[a])
                nested_list[index].remove(str(unwrapped_text))

    return nested_list


def add_list_border(nested_list):
    """Returns: a ragged list with ASCII borders. The nested lists will have borders.
    Precondition: list is a nested list and all items in the nested list are strings"""
    for index in range(len(nested_list)):
        list_item = nested_list[index]
        border_width = max(len(s) for s in list_item)

        # add top border
        top_border = ['┌' + '─' * border_width + '┐']
        top_border = re.sub("['',]", '', str(top_border)).strip('[]')
        nested_list[index].insert(0, top_border)

        # iterate over middle lines and add border there
        for i in range(len(list_item)):
            if i == 1:
                list_item[i] = '│' + (' ' * ((border_width - len(list_item[i])) // 2)) + (list_item[i] + ' ' * (
                            (1 + border_width - len(list_item[i])) // 2))[:border_width] + '│'
            elif i >= 2:
                list_item[i] = '│' + (list_item[i] + ' ' * border_width)[:border_width] + '│'

        # add bottom border
        bottom_border = ['└' + '─' * border_width + '┘']
        bottom_border = re.sub("['',]", '', str(bottom_border)).strip('[]')
        nested_list[index].append(bottom_border)
    return nested_list


def remove_list_border(nested_list):
    for index in range(len(nested_list)):
        nested_list[index].pop(0)
        nested_list[index].pop(len(nested_list[index]) - 1)

    for index in range(len(nested_list)):
        for i in range(len(nested_list[index])):
            nested_list[index][i] = re.sub("[│□]", '', str(nested_list[index][i])).rstrip(' ').lstrip(' ')
    return nested_list


def print_grid(nested_list, continue_printing_row, start_pos=0):
    max_nested_list_length = max(len(i) for i in nested_list)
    nested_list_item_width_accumulator = 0
    found_column_count = False

    global columnEndPos

    row_position = range(len(nested_list))

    # ------ Find columnEndPos ------
    for index in row_position[start_pos:]:
        nested_list_item = nested_list[index]

        note_width = max(len(s) for s in nested_list_item)
        nested_list_item_width_accumulator += note_width
        if nested_list_item_width_accumulator > (width - 20) and not found_column_count:
            columnEndPos = (nested_list.index(nested_list[index - 1]))
            found_column_count = True
        elif index == max(row_position[start_pos:]) and not found_column_count and nested_list_item_width_accumulator < width:
            columnEndPos = len(nested_list)
            # return
            continue_printing_row = False
            found_column_count = True
    # ------ End Find columnEndPos ------

    # ------ Add spaces below note to make rectangular row of characters ------
    if columnEndPos == start_pos:
        max_nested_list_length = len(nested_list[columnEndPos])
    elif columnEndPos == len(nested_list):
        max_nested_list_length = max(len(i) for i in nested_list[start_pos:columnEndPos])
    else:
        max_nested_list_length = max(len(i) for i in nested_list[start_pos:columnEndPos + 1])

    for index in row_position[start_pos:columnEndPos + 1]:
        nested_list_item = nested_list[index]
        note_width = max(len(s) for s in nested_list_item)
        for i in range(len(nested_list_item)):
            if len(nested_list_item) < max_nested_list_length:
                for x in range(max_nested_list_length - len(nested_list_item)):
                    nested_list_item.append(' ' * note_width)
    # ------ End add spaces below note to make rectangular row of characters ------

    if (columnEndPos + 1) == start_pos:
        nested_list_formatted = nested_list[columnEndPos + 1]
    else:
        nested_list_row = nested_list[start_pos:columnEndPos + 1]

        nested_list_formatted = zip(*nested_list_row)

        nested_list_formatted = list(nested_list_formatted)

    # ------ Center Notes ------
    center_space_count = round(abs((width - len(''.join(nested_list_formatted[0]))) / 2))

    for i in range(len(nested_list_formatted)):
        print('\u001b[0;33m', end='')
        if i == 1:
            print('\u001b[1;33m', end='')
        string_line = ''.join(nested_list_formatted[i])
        print((center_space_count * ' '), string_line)
    if continue_printing_row:
        print_grid(nested_list, continue_printing_row, columnEndPos + 1)
