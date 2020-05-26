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
from PyInquirer import prompt, print_json

# Enter your credentials here to save them
username = 'zachary.h.a@gmail.com'
password = 'kmaclzvenpdofpqw'

#username = 'example@gmail.com'
#password = 'password'

columns, rows = os.get_terminal_size(0)
width = columns

keep = gkeepapi.Keep()

def main():
    animateWelcomeText()
    if username=='example@gmail.com' and password=='password':
        login()
    else:
        # If user has already entered login info then display notes.
        sys.stdout.write('\033[1;32m')
        print('Using credentials you entered in keepd.py to login...\n'.center(width))


        try:
            keep.login(username, password)
        except:
            sys.stdout.write('\u001b[31m')
            print("Your login credentials were incorrect!\n")
            return

        sys.stdout.write('\033[21;93m')

        displayNotes()

# TODO: Setup Rows
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
    noteWidthAccumulator = 0

    foundColumnCount = False

    for index in range(len(rawNoteText)):
        # add empty spaces below
        note = rawNoteText[index]
        borderWidth = max(len(s) for s in note)

        noteWidthAccumulator += borderWidth
        if noteWidthAccumulator > width and not foundColumnCount:
            #print(noteWidthAccumulator, width)
            columnCount = rawNoteText.index(rawNoteText[index-1])
            foundColumnCount = True

        for i in range(len(note)):
            if len(note) < maxNoteLength:
                for x in range(maxNoteLength-len(note)):
                    note.append(' ' * borderWidth)

    #print(columnCount)
    rawNoteTextRow = rawNoteText[:columnCount+1]
    #print(list(noteTextFormatted))
    noteTextFormatted = zip(*rawNoteTextRow)
        #print(index)

    noteTextFormatted = list(noteTextFormatted)
    testList = list(zip(rawNoteText[0], rawNoteText[1], rawNoteText[2]))

    centerSpaceIterator = abs((width - len(str(noteTextFormatted[0])))//2)-1
    centerSpace = ''
    for i in range(centerSpaceIterator):
        centerSpace += ' '

    for index in range(len(noteTextFormatted)):
        noteTextFormatted[index] = list(noteTextFormatted[index])
        noteTextFormatted[index][0] = centerSpace + noteTextFormatted[index][0]

    # Center text
    #print(len(str(testList[0])))
    #print(re.sub("['',()]", '', str(testList[0])))

    for i in range(len(noteTextFormatted)):
        print(re.sub("['',()]", '', str(noteTextFormatted[i])).strip('[]'))

    # -------------------------------------------------------------------------------------






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
        sys.stdout.write('\u001b[31m')
        print("Your login credentials were incorrect!\n")
        return


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

    paragraphText = 'Hello! This is a terminal based Google Keep Program. It is still in development so feel free to leave comments or suggestions on the github page: https://github.com/zack-ashen/keepd. In addition, not all features from the true Google Keep are included. However, if there is something you want to see feel free to make a request on github or email: zachary.h.a@gmail.com. Thanks! \n'

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
    main()
