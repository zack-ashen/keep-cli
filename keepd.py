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
password = 'nldhilyhirqxrofl'

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

def listifyGoogleNotes(googleNotes):
    """Returns: a nested list from a Google Note object. Checked items are removed
    from the list.

    Example: Google Note object with list titled 'Foo List' and items:
    'get apples', "pick up groceries" and a note titled 'Foo Note' with text:
    'Garbage in garbage out the end of this note', becomes:
    [[["Foo List"], ["get apples"], ["pick up gorceries"]],
    [["Foo Note"], ["Garbage in garbage out"], ["the end of this note"]]

     Precondition: googleNote is a list containing either items of type
     'gkeepapi.node.List' or 'gkeepapi.node.Note'"""


    noteList = []

    for index in range(len(googleNotes)):
        if type(googleNotes[index]) == gkeepapi.node.List:
            uncheckedList = googleNotes[index].unchecked
            noteTitle = googleNotes[index].title
            for i in range(len(uncheckedList)):
                uncheckedList[i] = uncheckedList[i].text
                uncheckedList[i] = '□  ' + uncheckedList[i]
            noteList.append(uncheckedList)
            uncheckedList.insert(0, noteTitle)
        else:
            note = googleNotes[index]
            noteTitle = note.title
            note = note.text.split('\n')
            noteList.append(note)
            note.insert(0, noteTitle)

    return noteList

def addListBorder(nestedList):
    """Returns: a ragged list with ASCII borders. The nested lists will have borders.
    Precondition: list is a nested list and all items in the nested list are strings"""

    for index in range(len(nestedList)):
        listItem = nestedList[index]
        borderWidth = max(len(s) for s in listItem)

        # add top border
        topBorder = ['┌' + '─' * borderWidth + '┐']
        topBorder = re.sub("['',]", '', str(topBorder)).strip('[]')
        nestedList[index].insert(0, topBorder)

        # iterate over middle lines and add border there
        for i in range(len(listItem)):
            if i > 0:
                listItem[i] = '│' + (listItem[i] + ' ' * borderWidth)[:borderWidth] + '│'

        # add bottom borders
        bottomBorder = ['└' + '─' * borderWidth + '┘']
        bottomBorder = re.sub("['',]", '', str(bottomBorder)).strip('[]')
        nestedList[index].append(bottomBorder)
    return nestedList

def printRow(nestedList, startPos):
    maxNestedListLength = max(len(i) for i in nestedList)
    nestedListItemWidthAccumulator = 0
    foundColumnCount = False
    global columnCount
    rowPosition = range(len(nestedList))

    for index in rowPosition[startPos:]:
        # add empty spaces below
        nestedListItem = nestedList[index]
        noteWidth = max(len(s) for s in nestedListItem)
        nestedListItemWidthAccumulator += noteWidth
        if nestedListItemWidthAccumulator > width-5 and not foundColumnCount:
            columnCount = (nestedList.index(nestedList[index-1]))
            foundColumnCount = True

        elif index == max(rowPosition[startPos:]) and not foundColumnCount and nestedListItemWidthAccumulator < width:
            columnCount = (nestedList.index(nestedList[index-1]))
            foundColumnCount = True


    if (columnCount+1) == startPos:
        maxNestedListLength = len(nestedList[columnCount+1])
    else:
        maxNestedListLength = max(len(i) for i in nestedList[startPos:columnCount+1])

    for index in rowPosition[startPos:]:
        nestedListItem = nestedList[index]
        noteWidth = max(len(s) for s in nestedListItem)
        for i in range(len(nestedListItem)):
            if len(nestedListItem) < maxNestedListLength:
                for x in range(maxNestedListLength-len(nestedListItem)):
                    nestedListItem.append(' ' * noteWidth)

    if (columnCount+1) == startPos:
        nestedListFormatted = nestedList[columnCount+1]
    else:
        nestedListRow = nestedList[startPos:columnCount+1]

        nestedListFormatted = zip(*nestedListRow)

        nestedListFormatted = list(nestedListFormatted)

    # Center Notes
    centerSpaceIterator = abs((width - len(str(nestedListFormatted[0])))//2)+5
    centerSpace = ''

    for i in range(centerSpaceIterator):
        centerSpace += ' '

    if (columnCount+1) == startPos:
        nestedListFormatted = nestedList[columnCount+1]
        for index in range(len(nestedListFormatted)):
            nestedListFormatted[index] = centerSpace + nestedListFormatted[index]

        for i in range(len(nestedListFormatted)):
            print(nestedListFormatted[i])

    else:
        for index in range(len(nestedListFormatted)):
            nestedListFormatted[index] = list(nestedListFormatted[index])
            nestedListFormatted[index][0] = centerSpace + nestedListFormatted[index][0]

        for i in range(len(nestedListFormatted)):
            print(re.sub("['',()]", '', str(nestedListFormatted[i])).strip('[]'))

def displayNotes():
    """Displays the notes from your Google Keep account in a grid view with borders."""
    googleNotes = keep.all()

    noteList = listifyGoogleNotes(googleNotes)

    noteList = addListBorder(noteList)

    #for i in range(len(noteList[5])):
    #    print(noteList[5][i])

    #print(noteList[5])

    # Find Amount of Notes in a Column (Column Count) and

    printRow(noteList, 0)

    #print(columnCount)

    #printRow(noteList, 5)

    i = columnCount + 1

    while len(noteList) >= columnCount + 2:
        printRow(noteList, columnCount+1)
        print(columnCount)
        sleep(1)




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
        paragraphText = str(fill(paragraphText, width/2))
        paragraphTextList = paragraphText.split('\n')
        for index in range(len(paragraphTextList)):
            print(paragraphTextList[index].center(width))
        print('\n')

        line = ''
        for index in range(width):
            line += '-'
        print(line)

if __name__ == '__main__':
    main()
