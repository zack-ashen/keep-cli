#!/usr/bin/env python3

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
from .__init__ import __version__

columns, rows = os.get_terminal_size()
width = columns

columnEndPos = 0
continuePrintingRow = True


fig = Figlet(font='larry3d', justify='center', width=width)

keep = gkeepapi.Keep()


#TODO Build method
def refresh(noteList, googleNotes, noteToEdit, indexOfNote):
    pass


def noteView():
    """Displays the notes from your Google Keep account in a grid view with borders."""
    googleNotes = keep.all()

    os.system('clear')
    print('\033[1;33m')
    print(fig.renderText('Keep...'))

    if len(googleNotes) == 0:
        print('\u001b[1;31m', end='')
        print('You don\'t have any notes!'.center(width))
        choices = [
            '✎ Make a New Note ✎',
            '✎ Make a New List ✎',
            '⛔ Exit ⛔'
        ]
        noteList = []
    else:
        global continuePrintingRow

        noteList = NoteGrid.listifyGoogleNotes(googleNotes)
        noteList = NoteGrid.wrapText(noteList)
        noteList = NoteGrid.addListBorder(noteList)
        NoteGrid.printGrid(noteList)
        print('\n')
        continuePrintingRow = True
        choices =  [
            '✎ Make a New Note ✎',
            '✎ Make a New List ✎',
            'Edit a Note',
            '⛔ Exit ⛔']

    initialPrompt = [
    {
        'type': 'list',
        'name': 'options',
        'message': 'Please select an option:',
        'choices': choices
    }]
    initialSelection = prompt(initialPrompt)

    if initialSelection.get('options') == '✎ Make a New Note ✎':
        makeANote(noteList)
    elif initialSelection.get('options') == '✎ Make a New List ✎':
        makeAList(noteList)
    elif initialSelection.get('options') == 'Edit a Note':
        editNoteSelectorView(noteList, googleNotes)
    elif initialSelection.get('options') == '⛔ Exit ⛔':
        return


def makeAList(noteList, displayNoteView=True):
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
    if displayNoteView:
        noteView()
    else:
        return


def makeANote(noteList, displayNoteView=True):
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
    if displayNoteView:
        noteView()
    else:
        return


def editNoteSelectorView(noteList, googleNotes):
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
                if len(noteList) == 1:
                    noteToEdit.append(noteList[0])
                    indexOfNote  = 0
                else:
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
    print('\033[1;33m')
    print(fig.renderText('keep...'))

    NoteGrid.printGrid(noteToEdit)

    global continuePrintingRow
    continuePrintingRow = True

    gnote = googleNotes[indexOfNote]

    if type(googleNotes[indexOfNote]) == gkeepapi.node.List:
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

        noteToEdit = NoteGrid.removeListBorder(noteToEdit)

        if type(googleNotes[indexOfNote]) == gkeepapi.node.List:
            for index in range(len(noteToEdit[0])):
                if index > 0:
                    noteToEdit[0][index] = '□ ' + noteToEdit[0][index]

        noteToEdit = NoteGrid.addListBorder(noteToEdit)

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
            #if index > 1 and index < (len(noteList[indexOfNote])-1):
            if '□' in noteList[indexOfNote][index]:
                itemList.append(re.sub("[│]", '', str(noteList[indexOfNote][index])).rstrip(' ').lstrip(' '))

        itemList.append('...+ Add Item/s +')
        itemList.append('...⏎ Go Back ⏎')

        itemToEdit = [
        {
            'type': 'list',
            'name': 'item',
            'message': 'Please select a list item to edit:',
            'choices': itemList
        }]

        itemToEditAnswer = prompt(itemToEdit)

        if itemToEditAnswer.get('item') == '...+ Add Item/s +':
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

            for index in range(len(listItems)):
                gnote.add(listItems[index][0], listItems[index][1])

            keep.sync()

            noteList = NoteGrid.listifyGoogleNotes(googleNotes)
            noteList = NoteGrid.addListBorder(noteList)
            noteToEdit[0] = noteList[indexOfNote]
            noteEditView(noteToEdit, googleNotes, noteList, indexOfNote)

        elif itemToEditAnswer.get('item') == '...⏎ Go Back ⏎':
            noteEditView(noteToEdit, googleNotes, noteList, indexOfNote)
        else:
            glistitem = gnote.unchecked[itemList.index(itemToEditAnswer.get('item'))]

            editItemPrompt = [{
                'type':'input',
                'name':'itemEdited',
                'message': 'Edit the item (Delete all text to delete item):',
                'default': glistitem.text
            }]

            editItemAnswer = prompt(editItemPrompt)

            if editItemAnswer.get('itemEdited') != '':
                glistitem.text = editItemAnswer.get('itemEdited')
                keep.sync()

                noteToEdit = NoteGrid.removeListBorder(noteToEdit)
                for index in range(len(noteToEdit[0])):
                    if index > 0:
                        noteToEdit[0][index] = '□ ' + noteToEdit[0][index]
                noteToEdit[0][(itemList.index(itemToEditAnswer.get('item')))+1] = '□ ' + editItemAnswer.get('itemEdited')
                noteToEdit = NoteGrid.addListBorder(noteToEdit)
                noteList[indexOfNote] = noteToEdit[0]
            else:
                # Add delete item
                pass

        noteEditView(noteToEdit, googleNotes, noteList, indexOfNote)
    elif listSelection.get('options') == 'Check the items of this list ✎':
        # Select list item to edit ==> options: check or uncheck, edit item
        itemList = []
        itemChoices = []
        for index in range(len(noteList[indexOfNote])):
            if '□' in noteList[indexOfNote][index]:
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

        checkedItems = listItemsSelection.get('options')

        for index in range(len(checkedItems)):
            checkedItems[index] = re.sub("[□]", '', str(checkedItems[index])).rstrip(' ').lstrip(' ')
        noteToEdit = NoteGrid.removeListBorder(noteToEdit)
        for index in range(len(checkedItems)):
            try:
                noteToEdit[0].index(checkedItems[index])
                googleList = gnote.unchecked
                googleList[index].checked = True
                keep.sync()
            except:
                pass
        googleNotes = keep.all()
        noteList = NoteGrid.listifyGoogleNotes(googleNotes)
        noteList = NoteGrid.addListBorder(noteList)
        noteToEdit[0] = noteList[indexOfNote]
        noteEditView(noteToEdit, googleNotes, noteList, indexOfNote)
    elif listSelection.get('options') == '⏎ Go Back ⏎':
        editNoteSelectorView(noteList, googleNotes)


def login():
    """Prompts the user to login and logs them in."""
    print('\033[21;93m')
    print('Please Login: \n \n')
    usernamePrompt = [
    {
        'type': 'input',
        'name': 'username',
        'message': 'Please enter your username:',
    }]
    usernameCredentials = prompt(usernamePrompt)

    username = usernameCredentials['username']
    password = keyring.get_password('google-keep', username)

    if isinstance(password, type(None)):
        passwordCredentials = [
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

        passwordCredentials = prompt(passwordCredentials)
        password = passwordCredentials['password']

        try:
            keep.login(username, password)
        except:
            print('\u001b[31m', end='')
            print("Your login credentials were incorrect!\n")
            return

        if passwordCredentials['confirm-save'] == True:
            keyring.set_password('google-keep', username, password)
    else:
        keep.login(username, password)


def animateWelcomeText():
    """Animates the welcome keepd text in ASCII font and welcome paragraph."""

    welcomeText = 'keepd...'

    text = ''

    for character in welcomeText:
        os.system('clear')
        text += character
        print('\033[1;33m')
        print(fig.renderText(text))
        sleep(0.1)

    print('\n')

    paragraphText = 'Hello! This is a terminal based Google Keep Program. It is still in development so feel free to leave comments or suggestions on the github page: https://github.com/zack-ashen/keep-cli. In addition, not all features from the true Google Keep are included. However, if there is something you want to see feel free to make a request on github or email: zachary.h.a@gmail.com. Thanks! \n'

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


def parseArguments():
    parser = argparse.ArgumentParser(description='keep-cli is a command line version of Google Keep. You can add, view, edit and delete notes.')

    parser.add_argument('--quick', help='Skips the intro animation and gets directly to login.', action='store_true')
    parser.add_argument('--note', help='Make a note...', action='store_true')
    parser.add_argument('--list', help='Make a list...', action='store_true')
    args = parser.parse_args()

    if args.quick:
        login()
        noteView()
    elif not args.quick and not args.note and not args.list:
        animateWelcomeText()
        login()
        noteView()
    if args.note:
        login()
        googleNotes = keep.all()
        noteList = [[]]
        makeANote(noteList, False)

    elif args.list:
        googleNotes = keep.all()
        noteList = [[]]
        makeAList(noteList, False)


def main():
    parseArguments()


if __name__ == '__main__':
    main()
