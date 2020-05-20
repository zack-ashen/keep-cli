#!/usr/bin/env python3

from __future__ import print_function, unicode_literals
import gkeepapi
import argparse
from pyfiglet import Figlet
import sys
from os import system, name
from time import sleep
import os
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
    lines = text.splitlines()
    borderWidth = max(len(s) for s in lines)
    borderText = ['┌' + '─' * borderWidth + '┐']
    for s in lines:
        borderText.append('│' + (s + ' ' * borderWidth)[:borderWidth] + '│')
    borderText.append('└' + '─' * borderWidth + '┘')
    return '\n'.join(borderText)


# TODO: Setup Column View
def displayNotes():
    googleNotes = keep.all()
    rawNoteText = []

    for index in range(len(googleNotes)):
        notelist = googleNotes[index].text.split('\n')
        notelist[:] = [x for x in notelist if "☑" not in x]
        rawNoteText.append(notelist)

    table3 = [["spam",42],["eggs",451],["bacon",0]]
    print(tabulate(table3, tablefmt="plain"))
    #print(rawNoteText)
    #print(tabulate(rawNoteText, tablefmt="plain"))
    noteText = []

    for index in range(len(rawNoteText)):
        note = rawNoteText[index]
        note = '\n'.join(note)
        noteText.append(note)

    #print(noteText)

    table = BeautifulTable()
    table2 = PrettyTable()

    fullNotes = []

    for index in range(len(noteText)):
        fullNote = googleNotes[index].title + '\n' + noteText[index]
        #fullNote = bordered(fullNote)
        fullNotes.append(fullNote)

    #print(fullNotes)
    #print(tabulate(fullNotes, tablefmt="plain"))

    #for fullNote in fullNotes:
    #    print(' '.join(fullNotes))
    for index in range(int(len(fullNotes)/3)):
        table.append_row([fullNotes[index], fullNotes[index+1], fullNotes[index+2]])
        table2.add_row([fullNotes[index], fullNotes[index+1], fullNotes[index+2]])

    table.set_style(BeautifulTable.STYLE_GRID)
    table.set_padding_widths(3)

    #print(table2)


def login():
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

    keep.login(username, password)
    displayNotes()

def animateWelcomeText():
    fig = Figlet(font='larry3d', justify='center', width=width)
    welcomeText = 'keepd...'

    text = ''

    for x in welcomeText:
        system('clear')
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

def main():
    animateWelcomeText()
    if username=='example@gmail.com' and password=='password':
        login()
    else:
        sys.stdout.write('\033[1;32m')
        print('Using credentials you entered in keeperd.py to login...'.center(width))

        keep.login(username, password)

        sys.stdout.write('\033[21;93m')

        #sleep(0.2)

        displayNotes()

    #createNoteView()

main()
