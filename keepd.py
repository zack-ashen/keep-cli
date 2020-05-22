#!/usr/bin/env python3

"""
Keepd
Author: Zachary Ashen
Date: May 15th 2020
Description: A CLI version of Google Keep which is a
note taking/list making website developed by Google.
Contact: zachary.h.a@gmail.com
"""

from __future__ import print_function, unicode_literals
import gkeepapi
from pyfiglet import Figlet
import sys
from time import sleep
import os

# Testing column view packages
from PyInquirer import prompt, print_json
from beautifultable import BeautifulTable
from prettytable import PrettyTable
from tabulate import tabulate

# Enter your credentials here to save them
username = 'zachary.h.a@gmail.com'
password = 'sbrhcbprueopksqq'

#username = 'example@gmail.com'
#password = 'password'

columns, rows = os.get_terminal_size(0)
width = columns

keep = gkeepapi.Keep()


def bordered(text):
    """Returns: a string with a ASCII border around it.
    Precondition: text is a string.
    Parameter: the string to put a border around."""

    lines = text.splitlines()
    borderWidth = max(len(s) for s in lines)

    # Add border on top
    borderText = ['┌' + '─' * borderWidth + '┐']

    # Add border on sides
    for s in lines:
        borderText.append('│' + (s + ' ' * borderWidth)[:borderWidth] + '│')

    # Add bottom border
    borderText.append('└' + '─' * borderWidth + '┘')

    return '\n'.join(borderText)


# TODO: Setup Column View
def displayNotes():
    """Displays the notes from your Google Keep account in a grid view with borders."""
    googleNotes = keep.all()
    rawNoteText = []

    for index in range(len(googleNotes)):
        notelist = googleNotes[index].text.split('\n')
        notelist[:] = [x for x in notelist if "☑" not in x]
        rawNoteText.append(notelist)

    # print(rawNoteText)
    # print(tabulate(rawNoteText, tablefmt="plain"))

    noteText = []

    for index in range(len(rawNoteText)):
        note = rawNoteText[index]
        note = '\n'.join(note)
        noteText.append(note)

    # print(noteText)

    table = BeautifulTable()
    table2 = PrettyTable()

    fullNotes = []

    for index in range(len(noteText)):
        fullNote = googleNotes[index].title + '\n' + noteText[index]
        # fullNote = bordered(fullNote)
        fullNotes.append(fullNote)

    for index in range(len(fullNotes)):
        print(bordered(fullNotes[index]))


def login():
    """Prompts the user to login and logs them in."""
    
    sys.stdout.write('\033[21;93m')
    sys.stdout.write('Please Login: \n \n')
    login = [
    {
        'type': 'input',
        'name': 'username',
        'message': 'Please enter your username:',
    },
    {
        'type': 'password',
        'name': 'password',
        'message': 'Please enter your password:',
    }]

    loginCredentials = prompt(login)

    username = loginCredentials['username']
    password = loginCredentials['password']

    try:
        keep.login(username, password)
    except:
        print("Your login credentials were incorrect!\n")


    displayNotes()

def animateWelcomeText():
    """Animates the welcome keepd text in ASCII font."""

    fig = Figlet(font='larry3d', justify='center', width=width)
    welcomeText = 'keepd...'

    text = ''

    for x in welcomeText:
        os.system('clear')
        text += x
        sys.stdout.write('\033[1;33m')
        sys.stdout.write(fig.renderText(text))
        sleep(0.1)

    sys.stdout.write('\n')
    paragraphText = 'Hello! This is a terminal based Google Keep Program. It is still in development so feel free to leave comments or suggestions on the github page:. In addition, not all features from the true Google Keep are included. However, if there is something you want to see feel free to make a request on github or email: zachary.h.a@gmail.com. Thanks! \n'
    # newtext = '\n'.join(sampletext[i:i+80] for i in range(0, len(sampletext), 80))

    paragraphStrings = []

    for index in range(0, len(paragraphText), 91):
        paragraphStrings.append(paragraphText[index : index + 91])

    for index in range(0, len(paragraphStrings)):
        print(paragraphStrings[index].center(width))

    line = ''
    for index in range(width):
        line += '-'
    print(line)

if __name__ == '__main__':
    animateWelcomeText()
    if username=='example@gmail.com' and password=='password':
        login()
    else:
        sys.stdout.write('\033[1;32m')
        print('Using credentials you entered in keeperd.py to login...'.center(width))

        keep.login(username, password)

        sys.stdout.write('\033[21;93m')

        displayNotes()
