"""Constants for keep-cli"""

import os

# get width and height
WIDTH, HEIGHT = os.get_terminal_size()


# prompts
MAKE_NOTE =       '✎ Make a New Note ✎',
MAKE_LIST =       '✎ Make a New List ✎',
EDIT_NOTE =       'Edit a Note',
EXIT =            '⛔ Exit ⛔'
ADD_ITEM =        'Add a list item (Enter \'-\' to finish):'
MAKE_TITLE =      'What should the title be?'
PICK_NOTE =       'Please pick a note to edit:'
PICK_ITEM =       'Please pick a item to edit:'
CHECK_ITEMS =     'Check the items of this list ✎',
EDIT_ITEMS =      'Edit the items of this list ✎',
EDIT_TITLE =      'Edit the title of this note ✎',
DELETE_NOTE =     'Delete this note ⌫',
GO_BACK =         '⏎ Go Back ⏎'
EDIT_BODY =       'Edit the body of this note ✎',
EDIT_NOTE =       'What would you like to do to this note?'
PASSWORD_PROMPT = 'Please enter your password:'
USERNAME_PROMPT = 'Please enter your username:'
SAVE_PASSWORD =   'Would you like your password to be saved?'
SELECT_OPTION =   'Please select an option:'
ADD_ITEMS =       '+ Add Item/s +'
SELECT_ITEM =     'Please select a list item to edit:'


# colors
YELLOW_BOLD = '\033[1;33m'
YELLOW =      '\033[21;93m'
RED =         '\u001b[31m'