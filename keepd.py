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
from textwrap import fill
import re

# Testing column view packages
from PyInquirer import prompt, print_json
from beautifultable import BeautifulTable
from prettytable import PrettyTable
from tabulate import tabulate

# Enter your credentials here to save them
username = 'zachary.h.a@gmail.com'
password = 'fkxcrvjpepkvwtqd'

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

def filterTop(x):
    if '┌' in x:
        return True
    return False

def filterMiddle(x):
    if '│' in x:
        return True
    return False

# TODO: Setup Column View
def displayNotes():
    """Displays the notes from your Google Keep account in a grid view with borders."""
    googleNotes = keep.all()

    rawNoteText = []

    for index in range(len(googleNotes)):
        notelist = googleNotes[index].text.split('\n')
        notelist[:] = [x for x in notelist if "☑" not in x]
        rawNoteText.append(notelist)

    #print(rawNoteText)

    for index in range(len(rawNoteText)):

        note = rawNoteText[index]
        borderWidth = max(len(s) for s in note)

        # add top border
        topBorder = ['┌' + '─' * borderWidth + '┐']
        topBorder = re.sub("['',]", '', str(topBorder)).strip('[]')
        rawNoteText[index].insert(0, topBorder)

        # iterate over middle lines and add border there
        for i in range(len(note)):
            if i > 0:
                note[i] = '│' + (note[i] + ' ' * borderWidth)[:borderWidth] + '│'

        # add bottom borders
        bottomBorder = ['└' + '─' * borderWidth + '┘']
        bottomBorder = re.sub("['',]", '', str(bottomBorder)).strip('[]')
        rawNoteText[index].append(bottomBorder)

    maxNoteLength = max(len(i) for i in rawNoteText)
    for index in range(len(rawNoteText)):
        # add empty spaces below
        note = rawNoteText[index]
        for i in range(len(note)):
            if len(note) < maxNoteLength:
                for x in range(maxNoteLength-len(note)):
                    note.append('')


    #print(rawNoteText)

    for rawNoteText[0], rawNoteText[1], rawNoteText[2], rawNoteText[3] in zip(rawNoteText[0], rawNoteText[1], rawNoteText[2], rawNoteText[3]):
        print(rawNoteText[0], rawNoteText[1], rawNoteText[2], rawNoteText[3])


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
        fullNote = bordered(fullNote)
        fullNotes.append(fullNote)

    #print(fullNotes)

    #for index in range(len(fullNotes)):
    #    print(fmt.format(fullNotes[index], fullNotes[index+1]))

    list_a = ['┌─────────────────────────┐', '│Hello this is  a test│', '│Hello this is a test│']
    list_b = ['┌─────────────────────────┐', '│Hello this is  a test│', '│Hello this is a test│']

    for item_a, item_b in zip(list_a, list_b):
        #print(item_a, item_b)
        pass

    fullNoteBorderedListSplit = list(map(lambda x: x.split('\n'), fullNotes))
    fullNoteBorderedListLines = []

    for index in range(len(fullNoteBorderedListSplit)):
        for i in range(len(fullNoteBorderedListSplit[index])):
            fullNoteBorderedListLines.append(fullNoteBorderedListSplit[index][i])

    topLineFiltered = list(filter(filterTop, fullNoteBorderedListLines))
    middleLinesFiltered = list(filter(filterMiddle, fullNoteBorderedListLines))
    topLine = fill(str(topLineFiltered), width=width)
    middleLines = fill(str(middleLinesFiltered), width=width)

    #print(re.sub("['',]", '', topLine).strip('[]'))
    #print(re.sub("['',]", '', middleLines).strip('[]'))

    #for index in range(len(fullNoteBorderedListFiltered)):
        #print(fullNoteBorderedListFiltered[index], end = ' ')
        #pass


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
    """Animates the welcome keepd text in ASCII font and welcome paragraph."""

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

    paragraphStrings = []

    if width < 100:
        print(paragraphText)
    else:
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
        # If user has already entered login info then display notes.
        sys.stdout.write('\033[1;32m')
        print('Using credentials you entered in keepd.py to login...'.center(width))

        keep.login(username, password)

        sys.stdout.write('\033[21;93m')

        displayNotes()
