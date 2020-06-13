"""
Keep-CLI
Author: Zachary Ashen
Date: May 15th 2020
Description: A CLI version of Google Keep which is a
note taking/list making website developed by Google.
Contact: zachary.h.a@gmail.com
"""

import os
from time import sleep
import re
from textwrap import fill

import gkeepapi
from pyfiglet import Figlet
from PyInquirer import prompt
import argparse
import keyring

from . import NoteGrid


columns, rows = os.get_terminal_size()
width = columns

columnEndPos = 0
continuePrintingRow = True

fig = Figlet(font='larry3d', justify='center', width=width)

keep = gkeepapi.Keep()


def note_view():
    """Displays the notes from your Google Keep account in a grid view with borders."""
    google_notes = keep.all()

    os.system('clear')
    print('\033[1;33m')
    print(fig.renderText('Keep...'))

    if len(google_notes) == 0:
        print('\u001b[1;31m', end='')
        print('You don\'t have any notes!'.center(width))
        choices = [
            '✎ Make a New Note ✎',
            '✎ Make a New List ✎',
            '⛔ Exit ⛔'
        ]
        note_list = []
    else:
        global continuePrintingRow

        note_list = NoteGrid.listify_google_notes(google_notes)
        note_list = NoteGrid.wrap_text(note_list)
        note_list = NoteGrid.add_list_border(note_list)
        NoteGrid.print_grid(note_list, continuePrintingRow)
        print('\n')
        continuePrintingRow = True
        choices = [
            '✎ Make a New Note ✎',
            '✎ Make a New List ✎',
            'Edit a Note',
            '⛔ Exit ⛔']

    initial_prompt = [
        {
            'type': 'list',
            'name': 'options',
            'message': 'Please select an option:',
            'choices': choices
        }]
    initial_selection = prompt(initial_prompt)

    if initial_selection.get('options') == '✎ Make a New Note ✎':
        make_a_note(note_list)
    elif initial_selection.get('options') == '✎ Make a New List ✎':
        make_a_list(note_list)
    elif initial_selection.get('options') == 'Edit a Note':
        edit_note_selector_view(note_list, google_notes)
    elif initial_selection.get('options') == '⛔ Exit ⛔':
        return


def make_a_list(noteList, displayNoteView=True):
    """Prompts the user to make a new list by going through prompts for title and list items...
    @param noteList: a ragged list of notes with the format: [[['note tile'], ['item 1'], ['item 2']], [['note title'],
    ['body of note random text etc...']]
    @param displayNoteView: If true after creating a list note_view() is called after, but if False it simply creates
    the list and returns. It is only false when the argument --list is used.
    """
    list_title_prompt = [
        {
            'type': 'input',
            'name': 'noteTitle',
            'message': 'What should the title of the list be?',
        }]

    list_title_answer = prompt(list_title_prompt)

    list_title = list_title_answer.get('noteTitle')

    list_finished = False
    list_items = []
    while not list_finished:
        add_list_item = [
            {
                'type': 'input',
                'name': 'list_item',
                'message': 'Add a list item (Enter \'-\' to finish):',
            }]

        list_item_answer = prompt(add_list_item)

        list_item = (list_item_answer.get('list_item'), False)

        list_items.append(list_item)

        if list_item_answer.get('list_item') == '-':
            list_items.pop(len(list_items) - 1)
            list_finished = True

    gnote = keep.createList(list_title, list_items)
    keep.sync()
    if displayNoteView:
        note_view()
    else:
        return


def make_a_note(note_list, display_note_view=True):
    """Prompts the user to make a new note by going through prompts for title and body uses the $EDITOR env variable...
    @param note_list: a ragged list of notes with the format: [[['note tile'], ['item 1'], ['item 2']], [['note title'],
    ['body of note random text etc...']]
    @param display_note_view: If true after creating a list note_view() is called after, but if False it simply creates
    the list and returns. It is only false when the argument --list is used.
    """
    note_title_prompt = [
        {
            'type': 'input',
            'name': 'note_title',
            'message': 'What should the title of the note be?',
        }]

    note_title_answer = prompt(note_title_prompt)

    note_title = note_title_answer.get('note_title')

    os.system('$EDITOR note')

    with open('note', 'r') as file:
        note_text = file.read()

    os.system('rm note')

    gnote = keep.createNote(note_title, note_text)
    keep.sync()
    if display_note_view:
        note_view()
    else:
        return


def edit_note_selector_view(note_list, google_notes):
    """A view of all the possible notes to edit and allows the user to select a note. This note item has an index which
    is then passed to the note_edit_view() to display that note for editing.
    @param note_list: a ragged list of notes with the format: [[['note tile'], ['item 1'], ['item 2']], [['note title'],
    ['body of note random text etc...']]
    @param google_notes: A gkeepapi object which contains a list of keep objects such as lists and notes.
    """
    global continuePrintingRow

    title_list = []
    for i in range(len(note_list)):
        title_list.append(re.sub("[│]", '', str(note_list[i][1])).rstrip(' ').lstrip(' '))

    title_list.append('⏎ Go Back ⏎')

    list_prompt = [
        {
            'type': 'list',
            'name': 'options',
            'message': 'Please pick an note to edit:',
            'choices': title_list
        }]

    list_selection = prompt(list_prompt)

    if list_selection.get('options') == '⏎ Go Back ⏎':
        note_view()

    notes = []
    for i in range(len(note_list)):
        for index in range(len(note_list[i])):
            title = list(filter(lambda x: list_selection.get('options') in note_list[i][index], note_list[i][index]))
            title_string = ''
            for y in range(len(title)):
                title_string += title[y]

            if title_string != '':
                notes.append(title_string)

    note_to_edit = []

    for index in range(len(note_list)):
        for i in range(len(note_list[index])):
            try:
                if len(note_list) == 1:
                    note_to_edit.append(note_list[0])
                    index_of_note = 0
                else:
                    test_note_existence = note_list[i][index].index(notes[0])
                    note_to_edit.append(note_list[i])
                    index_of_note = i
            except:
                pass

    delete_white_space = False

    note_to_edit_accumulator = []

    for note in range(len(note_to_edit)):
        for item in range(len(note_to_edit[note])):
            if not delete_white_space:
                note_to_edit_accumulator.append(note_to_edit[note][item])
                if '┘' in note_to_edit[note][item]:
                    delete_white_space = True
            else:
                pass

    note_to_edit = [note_to_edit_accumulator]
    note_edit_view(note_to_edit, google_notes, note_list, index_of_note)


def note_edit_view(note_to_edit, google_notes, note_list, index_of_note):
    """Displays options for editing a note or list depending on the type. Such as deleting the note or editing and
    checking the items of the list etc...
    @param note_to_edit: a nested list containing the specific note that is meant to edit in the format: [['note tile'],
    ['item 1'], ['item 2']]
    @param google_notes: A gkeepapi object which contains a list of keep objects such as lists and notes.
    @param note_list: a ragged list of notes with the format: [[['note tile'], ['item 1'], ['item 2']], [['note title'],
    ['body of note random text etc...']]
    @param index_of_note: the index of the note that is mean to be edited in the googleNotes list and ragged noteList.
    """
    os.system('clear')
    print('\033[1;33m')
    print(fig.renderText('keep...'))
    global continuePrintingRow

    NoteGrid.print_grid(note_to_edit, continuePrintingRow)
    continuePrintingRow = True

    gnote = google_notes[index_of_note]

    if type(google_notes[index_of_note]) == gkeepapi.node.List:
        choices = [
            'Check the items of this list ✎',
            'Edit the items of this list ✎',
            'Edit the title of this note ✎',
            'Delete this note ⌫',
            '⏎ Go Back ⏎'
        ]
    else:
        choices = [
            'Edit the title of this note ✎',
            'Edit the body of this note ✎',
            'Delete this note ⌫',
            '⏎ Go Back ⏎'
        ]

    edit_options = [
        {
            'type': 'list',
            'name': 'options',
            'message': 'What would you like to do to this note?',
            'choices': choices
        }]
    list_selection = prompt(edit_options)

    if list_selection.get('options') == 'Delete this note ⌫':
        note_to_delete = google_notes[index_of_note]
        note_to_delete.delete()
        keep.sync()
        note_view()
    elif list_selection.get('options') == 'Edit the title of this note ✎':
        new_title_prompt = [
            {
                'type': 'input',
                'name': 'noteTitle',
                'message': 'What should the title of the note be?',
            }]

        new_title_answer = prompt(new_title_prompt)

        new_title = new_title_answer.get('noteTitle')

        gnote.title = new_title

        keep.sync()

        borderWidth = len(note_to_edit[0][1])
        note_to_edit[0][1] = new_title

        note_to_edit = NoteGrid.remove_list_border(note_to_edit)

        if type(google_notes[index_of_note]) == gkeepapi.node.List:
            for index in range(len(note_to_edit[0])):
                if index > 0:
                    note_to_edit[0][index] = '□ ' + note_to_edit[0][index]

        note_to_edit = NoteGrid.add_list_border(note_to_edit)

        note_edit_view(note_to_edit, google_notes, note_list, index_of_note)
    elif list_selection.get('options') == 'Edit the body of this note ✎':
        os.system('touch note')

        note_body_file = open('note', "w")
        text_body = note_body_file.write(gnote.text)
        note_body_file.close()

        os.system('$EDITOR note')

        with open('note', 'r') as file:
            note_text = file.read()

        os.system('rm ' + 'note')

        gnote.text = note_text
        keep.sync()
        note_view()
    elif list_selection.get('options') == 'Edit the items of this list ✎':
        item_list = []
        for index in range(len(note_list[index_of_note])):
            # if index > 1 and index < (len(noteList[indexOfNote])-1):
            if '□' in note_list[index_of_note][index]:
                item_list.append(re.sub("[│]", '', str(note_list[index_of_note][index])).rstrip(' ').lstrip(' '))

        item_list.append('...+ Add Item/s +')
        item_list.append('...⏎ Go Back ⏎')

        item_to_edit = [
            {
                'type': 'list',
                'name': 'item',
                'message': 'Please select a list item to edit:',
                'choices': item_list
            }]

        item_to_edit_answer = prompt(item_to_edit)

        if item_to_edit_answer.get('item') == '...+ Add Item/s +':
            list_finished = False
            list_items = []
            while not list_finished:
                add_list_item = [
                    {
                        'type': 'input',
                        'name': 'list_item',
                        'message': 'Add a list item (Enter \'-\' to finish):',
                    }]

                list_item_answer = prompt(add_list_item)

                list_item = (list_item_answer.get('list_item'), False)

                list_items.append(list_item)

                if list_item_answer.get('list_item') == '-':
                    list_items.pop(len(list_items) - 1)
                    list_finished = True

            for index in range(len(list_items)):
                gnote.add(list_items[index][0], list_items[index][1])

            keep.sync()

            note_list = NoteGrid.listify_google_notes(google_notes)
            note_list = NoteGrid.add_list_border(note_list)
            note_to_edit[0] = note_list[index_of_note]
            note_edit_view(note_to_edit, google_notes, note_list, index_of_note)

        elif item_to_edit_answer.get('item') == '...⏎ Go Back ⏎':
            note_edit_view(note_to_edit, google_notes, note_list, index_of_note)
        else:
            glistitem = gnote.unchecked[item_list.index(item_to_edit_answer.get('item'))]

            edit_item_prompt = [{
                'type': 'input',
                'name': 'itemEdited',
                'message': 'Edit the item (Delete all text to delete item):',
                'default': glistitem.text
            }]

            edit_item_answer = prompt(edit_item_prompt)

            if edit_item_answer.get('itemEdited') != '':
                glistitem.text = edit_item_answer.get('itemEdited')
                keep.sync()

                note_to_edit = NoteGrid.remove_list_border(note_to_edit)
                for index in range(len(note_to_edit[0])):
                    if index > 0:
                        note_to_edit[0][index] = '□ ' + note_to_edit[0][index]
                note_to_edit[0][(item_list.index(item_to_edit_answer.get('item'))) + 1] = '□ ' + edit_item_answer.get(
                    'itemEdited')
                note_to_edit = NoteGrid.add_list_border(note_to_edit)
                note_list[index_of_note] = note_to_edit[0]
            else:
                # Add delete item
                pass

        note_edit_view(note_to_edit, google_notes, note_list, index_of_note)
    elif list_selection.get('options') == 'Check the items of this list ✎':
        # Select list item to edit ==> options: check or uncheck, edit item
        item_list = []
        item_choices = []
        for index in range(len(note_list[index_of_note])):
            if '□' in note_list[index_of_note][index]:
                item_string = re.sub("[│]", '', str(note_list[index_of_note][index])).rstrip(' ').lstrip(' ')
                item_dict = dict.fromkeys([item_string], 'name')
                item_dict_inverted = dict(map(reversed, item_dict.items()))
                item_choices.append(item_dict_inverted)

        listItemsPrompt = [
            {
                'type': 'checkbox',
                'name': 'options',
                'message': 'Please pick a item to edit:',
                'choices': item_choices
            }]

        list_items_selection = prompt(listItemsPrompt)

        checked_items = list_items_selection.get('options')

        for index in range(len(checked_items)):
            checked_items[index] = re.sub("[□]", '', str(checked_items[index])).rstrip(' ').lstrip(' ')
        note_to_edit = NoteGrid.remove_list_border(note_to_edit)
        for index in range(len(checked_items)):
            try:
                note_to_edit[0].index(checked_items[index])
                google_list = gnote.unchecked
                google_list[index].checked = True
                keep.sync()
            except:
                pass
        google_notes = keep.all()
        note_list = NoteGrid.listify_google_notes(google_notes)
        note_list = NoteGrid.add_list_border(note_list)
        note_to_edit[0] = note_list[index_of_note]
        note_edit_view(note_to_edit, google_notes, note_list, index_of_note)
    elif list_selection.get('options') == '⏎ Go Back ⏎':
        edit_note_selector_view(note_list, google_notes)


def login():
    """Prompts the user to login and logs them in."""
    print('\033[21;93m')
    print('Please Login: \n \n')
    username_prompt = [
        {
            'type': 'input',
            'name': 'username',
            'message': 'Please enter your username:',
        }]
    username_credentials = prompt(username_prompt)

    username = username_credentials['username']
    password = keyring.get_password('google-keep', username)

    if isinstance(password, type(None)):
        password_credentials = [
            {
                'type': 'password',
                'name': 'password',
                'message': 'Please enter your password:',
            },
            {
                'type': 'confirm',
                'name': 'confirm-save',
                'message': 'Would you like your password to be saved?'
            }]

        password_credentials = prompt(password_credentials)
        password = password_credentials['password']

        try:
            keep.login(username, password)
        except:
            print('\u001b[31m', end='')
            print("Your login credentials were incorrect!\n")
            return

        if password_credentials['confirm-save']:
            keyring.set_password('google-keep', username, password)
    else:
        keep.login(username, password)


def animate_welcome_text():
    """Animates the welcome keepd text in ASCII font and welcome paragraph."""

    welcome_text = 'keepd...'

    text = ''

    for character in welcome_text:
        os.system('clear')
        text += character
        print('\033[1;33m')
        print(fig.renderText(text))
        sleep(0.1)

    print('\n')

    paragraph_text = 'Hello! This is a terminal based Google Keep Program. It is still in development so feel free to ' \
                     'leave comments or suggestions on the github page: https://github.com/zack-ashen/keep-cli. In ' \
                     'addition, not all features from the true Google Keep are included. However, if there is ' \
                     'something you want to see feel free to make a request on github or email: ' \
                     'zachary.h.a@gmail.com. Thanks! \n '

    paragraph_strings = []

    if width < 100:
        print(paragraph_text)
    else:
        paragraph_text = str(fill(paragraph_text, width / 2))
        paragraph_text_list = paragraph_text.split('\n')
        for index in range(len(paragraph_text_list)):
            print(paragraph_text_list[index].center(width))
        print('\n')

        line = ''
        for index in range(width):
            line += '─'
        print(line)


def parse_arguments():
    """Parses arguments and calls the subsequent methods.
        --list: Creates a new list
        --note: Creates a new note
        --quick: skips the intro animation
    """
    parser = argparse.ArgumentParser(description='keep-cli is a command line version of Google Keep. You can add, '
                                                 'view, edit and delete notes.')

    parser.add_argument('--quick', help='Skips the intro animation and gets directly to login.', action='store_true')
    parser.add_argument('--note', help='Make a note...', action='store_true')
    parser.add_argument('--list', help='Make a list...', action='store_true')
    args = parser.parse_args()

    if args.quick:
        login()
        note_view()
    elif not args.quick and not args.note and not args.list:
        animate_welcome_text()
        login()
        note_view()
    if args.note:
        login()
        google_notes = keep.all()
        note_list = [[]]
        make_a_note(note_list, False)

    elif args.list:
        google_notes = keep.all()
        note_list = [[]]
        make_a_list(note_list, False)


def main():
    parse_arguments()


if __name__ == '__main__':
    main()
