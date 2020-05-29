#!/usr/bin/env python3

"""
Keep-CLI
Author: Zachary Ashen
Date: May 15th 2020
Description: A CLI version of Google Keep which is a
note taking/list making website developed by Google.
Contact: zachary.h.a@gmail.com
"""

#from __future__ import print_function, unicode_literals
import gkeepapi
from pyfiglet import Figlet
import sys # can get rid of this -- replace sys.stdout with print
from time import sleep
import os
from textwrap import fill
import re
from PyInquirer import prompt, print_json
from KeepGrid import KeepGrid
import argparse

# Enter your credentials here to save them
username = 'zachary.h.a@gmail.com'
password = 'orghhdaqedhypamu'

#username = 'example@gmail.com'
#password = 'password'

columns, rows = os.get_terminal_size(0)
width = columns

columnEndPos = 0
continuePrintingRow = True

keep = gkeepapi.Keep()

fig = Figlet(font='larry3d', justify='center', width=width)


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

        noteView()


def listToDict(lst): 
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)} 
    return res_dct 

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


    # This is the list accumulator that recieves the parsed Google Notes
    noteList = []

    for index in range(len(googleNotes)):
        # execute if note is a list
        if type(googleNotes[index]) == gkeepapi.node.List:
            # Only retrieve unchecked list items
            uncheckedList = googleNotes[index].unchecked
            noteTitle = googleNotes[index].title
            # get the string text of the list and change the list item to the string
            for i in range(len(uncheckedList)):
                uncheckedList[i] = '□  ' + uncheckedList[i].text
            noteList.append(uncheckedList)
            uncheckedList.insert(0, noteTitle)
        # execute of note is a note
        else:
            note = googleNotes[index]
            noteTitle = note.title
            note = note.text.split('\n')
            noteList.append(note)
            note.insert(0, noteTitle)
    return noteList


def wrapText(nestedList):
    for index in range(len(nestedList)):
        for i in range(len(nestedList[index])):
            if len(nestedList[index][i]) > (width-25):

                nestedList[index][i] = fill(nestedList[index][i], width=(width-22))

                unwrappedText = nestedList[index][i]

                #nestedList[index][i][width-30:width-20].split(' ')
                wrappedTextList = nestedList[index][i].split('\n')
                #print(wrappedTextList)
                for a in range(len(wrappedTextList)):
                    nestedList[index].insert(i+(a), wrappedTextList[a])
                nestedList[index].remove(str(unwrappedText))

    return nestedList


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
            if i == 1:
                listItem[i] = '│' + (' ' * ((borderWidth-len(listItem[i]))//2)) + (listItem[i] + ' ' * ((1+borderWidth-len(listItem[i]))//2))[:borderWidth] + '│'
            elif i >= 2:
                listItem[i] = '│' + (listItem[i] + ' ' * borderWidth)[:borderWidth] + '│'

        # add bottom border
        bottomBorder = ['└' + '─' * borderWidth + '┘']
        bottomBorder = re.sub("['',]", '', str(bottomBorder)).strip('[]')
        nestedList[index].append(bottomBorder)
    return nestedList


def removeListBorder(nestedList):
    for index in range(len(nestedList)):
        nestedList[index].pop(0)
        nestedList[index].pop(len(nestedList[index])-1)

    for index in range(len(nestedList)):
        for i in range(len(nestedList[index])):
            nestedList[index][i] = re.sub("[│]", '', str(nestedList[index][i])).rstrip(' ').lstrip(' ')
    return nestedList


def printGrid(nestedList, startPos=0):
    maxNestedListLength = max(len(i) for i in nestedList)
    nestedListItemWidthAccumulator = 0
    foundColumnCount = False

    global columnEndPos
    global continuePrintingRow

    rowPosition = range(len(nestedList))

    # ------ Find columnEndPos ------
    for index in rowPosition[startPos:]:
        nestedListItem = nestedList[index]

        noteWidth = max(len(s) for s in nestedListItem)
        nestedListItemWidthAccumulator += noteWidth
        if nestedListItemWidthAccumulator > (width-20) and not foundColumnCount:
            columnEndPos = (nestedList.index(nestedList[index-1]))
            foundColumnCount = True
        elif index == max(rowPosition[startPos:]) and not foundColumnCount and nestedListItemWidthAccumulator < width:
            columnEndPos = len(nestedList)
            continuePrintingRow = False
            foundColumnCount = True
    # ------ End Find columnEndPos ------

    # ------ Add spaces below note to make rectangular row of characters ------
    if columnEndPos == startPos:
        maxNestedListLength = len(nestedList[columnEndPos])
    elif columnEndPos == len(nestedList):
        maxNestedListLength = max(len(i) for i in nestedList[startPos:columnEndPos])
    else:
        maxNestedListLength = max(len(i) for i in nestedList[startPos:columnEndPos+1])

    for index in rowPosition[startPos:columnEndPos+1]:
        nestedListItem = nestedList[index]
        noteWidth = max(len(s) for s in nestedListItem)
        for i in range(len(nestedListItem)):
            if len(nestedListItem) < maxNestedListLength:
                for x in range(maxNestedListLength-len(nestedListItem)):
                    nestedListItem.append(' ' * noteWidth)
    # ------ End add spaces below note to make rectangular row of characters ------


    if (columnEndPos+1) == startPos:
        nestedListFormatted = nestedList[columnEndPos+1]
    else:
        nestedListRow = nestedList[startPos:columnEndPos+1]

        nestedListFormatted = zip(*nestedListRow)

        nestedListFormatted = list(nestedListFormatted)

    # ------ Center Notes ------
    centerSpaceCount = round(abs((width - len(''.join(nestedListFormatted[0])))/2))

    for i in range(len(nestedListFormatted)):
        sys.stdout.write('\u001b[0;33m')
        if i == 1:
            sys.stdout.write('\u001b[1;33m')
        stringLine = ''.join(nestedListFormatted[i])
        print((centerSpaceCount * ' '), stringLine)

    while continuePrintingRow:
        printGrid(nestedList, columnEndPos+1)


def noteView():
    """Displays the notes from your Google Keep account in a grid view with borders."""
    googleNotes = keep.all()

    noteGrid = KeepGrid(googleNotes, width)

    os.system('clear')
    sys.stdout.write('\033[1;33m')
    sys.stdout.write(fig.renderText('Keep...'))

    # ------ Using Methods ------

    global continuePrintingRow

    noteList = listifyGoogleNotes(googleNotes)
    noteList = wrapText(noteList)
    noteList = addListBorder(noteList)

    printGrid(noteList)
    continuePrintingRow = True

    initialPrompt = [
    {
        'type': 'list',
        'name': 'options',
        'message': 'Please a Note Title to Edit:',
        'choices': ['Make a New Note', 'Make a New List', 'Edit a Note']
    }]
    initialSelection = prompt(initialPrompt)

    if initialSelection.get('options') == 'Make a New Note':
        makeANote(noteList)
    elif initialSelection.get('options') == 'Make a New List':
        makeAList(noteList)
    elif initialSelection.get('options') == 'Edit a Note':
        editNoteSelector(noteList, googleNotes)


def makeAList(noteList):
    listTitlePrompt = [
    {
        'type': 'input',
        'name': 'noteTitle',
        'message': 'What should the title of the list be?',
    }]

    listTitleAnswer = prompt(listTitlePrompt)

    listTitle = listTitleAnswer.get('noteTitle')

    listFinished = False
    listItems = []
    while listFinished == False:
        addListItem = [
        {
            'type': 'input',
            'name': 'listItem',
            'message': 'Add a list item (Enter \'-\' to finish):',
        }]

        listItemAnswer = prompt(addListItem)

        listItem = (listItemAnswer.get('listItem'), False)

        listItems.append(listItem)

        if listItemAnswer.get('listItem') == '-':
            listItems.pop(len(listItems)-1)
            listFinished = True

    gnote = keep.createList(listTitle, listItems)
    keep.sync()
    noteView()


def makeANote(noteList):
    noteTitlePrompt = [
    {
        'type': 'input',
        'name': 'noteTitle',
        'message': 'What should the title of the note be?',
    }]

    noteTitleAnswer = prompt(noteTitlePrompt)

    noteTitle = noteTitleAnswer.get('noteTitle')

    os.system('$EDITOR note')

    with open('note', 'r') as file:
        noteText = file.read()

    os.system('rm note')

    gnote = keep.createNote(noteTitle, noteText)
    keep.sync()
    noteView()


def editNoteSelector(noteList, googleNotes):
    global continuePrintingRow

    titleList = []
    for i in range(len(noteList)):
        titleList.append(re.sub("[│]", '', str(noteList[i][1])).rstrip(' ').lstrip(' '))

    titleList.append('⏎ Go Back ⏎')

    listPrompt = [
    {
        'type': 'list',
        'name': 'options',
        'message': 'Please pick an note to edit:',
        'choices': titleList
    }]

    listSelection = prompt(listPrompt)

    if listSelection.get('options') == '⏎ Go Back ⏎':
        noteView()

    notes = []
    for i in range(len(noteList)):
        for index in range(len(noteList[i])):
            title = list(filter(lambda x: listSelection.get('options') in noteList[i][index], noteList[i][index]))
            titleString = ''
            for y in range(len(title)):
                titleString += title[y]

            if titleString != '':
                notes.append(titleString)

    noteToEdit = []

    for index in range(len(noteList)):
        for i in range(len(noteList[index])):
            try:
                testNoteExistence = noteList[i][index].index(notes[0])
                noteToEdit.append(noteList[i])
                indexOfNote = i
            except:
                pass

    deleteWhiteSpace = False

    noteToEditAccumulator = []

    for note in range(len(noteToEdit)):
        for item in range(len(noteToEdit[note])):
            if deleteWhiteSpace == False:
                noteToEditAccumulator.append(noteToEdit[note][item])
                if '┘' in noteToEdit[note][item]:
                    deleteWhiteSpace = True
            else:
                pass

    noteToEdit = []
    noteToEdit.append(noteToEditAccumulator)
    noteEditView(noteToEdit, googleNotes, noteList, indexOfNote)


def noteEditView(noteToEdit, googleNotes, noteList, indexOfNote):
    os.system('clear')
    sys.stdout.write('\033[1;33m')
    sys.stdout.write(fig.renderText('keep...'))

    printGrid(noteToEdit)
    global continuePrintingRow
    continuePrintingRow = True



    gnote = googleNotes[indexOfNote]

    if type(googleNotes[indexOfNote]) == gkeepapi.node.List:
        choices = ['Check the items of this list ✎', 'Edit the items of this list ✎', 'Edit the title of this note ✎', 'Delete this note ⌫', '⏎ Go Back ⏎']
    else:
        choices = ['Edit the title of this note ✎', 'Edit the body of this note ✎', 'Delete this note ⌫', '⏎ Go Back ⏎']

    editOptions = [
        {
            'type': 'list',
            'name': 'options',
            'message': 'What would you like to do to this note?',
            'choices': choices
        }]

    listSelection = prompt(editOptions)


    # LOOK AT THESE FOR REPEATED CODE (CONVERT TO METHODS)
    if listSelection.get('options') == 'Delete this note ⌫':
        noteToDelete = googleNotes[indexOfNote]
        noteToDelete.delete()
        keep.sync()
        noteView()
    elif listSelection.get('options') == 'Edit the title of this note ✎':
        newTitlePrompt = [
        {
            'type': 'input',
            'name': 'noteTitle',
            'message': 'What should the title of the note be?',
        }]

        newTitleAnswer = prompt(newTitlePrompt)

        newTitle = newTitleAnswer.get('noteTitle')

        gnote.title = newTitle

        keep.sync()

        borderWidth = len(noteToEdit[0][1])
        noteToEdit[0][1] = newTitle

        noteToEdit = removeListBorder(noteToEdit)
        noteToEdit = addListBorder(noteToEdit)

        noteEditView(noteToEdit, googleNotes, noteList, indexOfNote)
    elif listSelection.get('options') == 'Edit the body of this note ✎':
        os.system('touch note')

        noteBodyFile = open('note', "w")
        textBody = noteBodyFile.write(gnote.text)
        noteBodyFile.close()

        os.system('$EDITOR note')

        with open('note', 'r') as file:
            noteText = file.read()

        os.system('rm ' + 'note')

        gnote.text = noteText
        keep.sync()
        noteView()
    elif listSelection.get('options') == 'Edit the items of this list ✎':
        itemList = []
        for index in range(len(noteList[indexOfNote])):
            if index > 1 and index < (len(noteList[indexOfNote])-1):
                itemList.append(re.sub("[│]", '', str(noteList[indexOfNote][index])).rstrip(' ').lstrip(' '))
        itemToEdit = [
        {
            'type': 'list',
            'name': 'item',
            'message': 'Please select a list item to edit:',
            'choices': itemList
        }]

        itemToEditAnswer = prompt(itemToEdit)

        glistitem = gnote.unchecked[itemList.index(itemToEditAnswer.get('item'))]

        editItemPrompt = [{
            'type':'input',
            'name':'itemEdited',
            'message': 'Edit the item:',
            'default': glistitem.text
        }]

        editItemAnswer = prompt(editItemPrompt)

        glistitem.text = editItemAnswer.get('itemEdited')
        keep.sync()
        googleNotes = keep.all()
        noteList = listifyGoogleNotes(googleNotes)
        noteList = addListBorder(noteList)
        noteEditView(noteToEdit, googleNotes, noteList, indexOfNote)

    elif listSelection.get('options') == 'Check the items of this list ✎':
        # Select list item to edit ==> options: check or uncheck, edit item
        itemList = []
        itemChoices = []
        for index in range(len(noteList[indexOfNote])):
            if index > 1 and index < (len(noteList[indexOfNote])-1):
                itemString = re.sub("[│]", '', str(noteList[indexOfNote][index])).rstrip(' ').lstrip(' ')
                itemDict = dict.fromkeys([itemString], 'name')
                itemDictInverted = dict(map(reversed, itemDict.items()))
                itemChoices.append(itemDictInverted)

        listItemsPrompt = [
        {
            'type': 'checkbox',
            'name': 'options',
            'message': 'Please pick a item to edit:',
            'choices': itemChoices
        }]

        listItemsSelection = prompt(listItemsPrompt)


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

    noteView()


def animateWelcomeText():
    """Animates the welcome keepd text in ASCII font and welcome paragraph."""

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
            line += '─'
        print(line)

def addArguments():
    pass

if __name__ == '__main__':
    main()
