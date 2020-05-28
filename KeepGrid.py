import re
import sys

class KeepGrid:
    """A Google Keep Grid
    Attribute: googleNotes is a """

    columnCount = 0

    def __init__(self, googleNotes, termWidth):
        """"""
        assert str(type(googleNotes)) == "<class 'list'>", repr(googleNotes) + ' is not a list.'
        self.googleNotes = googleNotes
        self.termWidth = termWidth

    def _listifyGoogleNotes(self, googleNotes):
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
            if str(type(googleNotes[index])) == "<class 'gkeepapi.node.List'>":
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

    def _addListBorder(self, nestedList):
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

            # add bottom borders
            bottomBorder = ['└' + '─' * borderWidth + '┘']
            bottomBorder = re.sub("['',]", '', str(bottomBorder)).strip('[]')
            nestedList[index].append(bottomBorder)
        return nestedList

    def printRow(self, startPos):
        """Prints a single row of googleNotes. All notes are centered and the amount
        varies depending on the terminal width. It is not responsive to adjusting width
        during use. Uses helper methods: listifyGoogleNotes() and addListBorder()"""

        noteList = self._listifyGoogleNotes(self.googleNotes)

        noteList = self._addListBorder(noteList)
        
        maxNoteListLength = max(len(i) for i in noteList)
        noteListItemWidthAccumulator = 0
        foundColumnCount = False

        rowPosition = range(len(noteList))

        for index in rowPosition[startPos:]:
            # add empty spaces below
            noteListItem = noteList[index]
            noteWidth = max(len(s) for s in noteListItem)
            noteListItemWidthAccumulator += noteWidth
            if noteListItemWidthAccumulator > (self.termWidth-20) and not foundColumnCount:
                columnCount = (noteList.index(noteList[index-1]))
                foundColumnCount = True

            elif index == max(rowPosition[startPos:]) and not foundColumnCount and noteListItemWidthAccumulator < self.termWidth:
                columnCount = (noteList.index(noteList[index-1]))
                foundColumnCount = True


        if (columnCount+1) == startPos:
            maxNoteListLength = len(noteList[columnCount+1])
        else:
            maxNoteListLength = max(len(i) for i in noteList[startPos:columnCount+1])

        for index in rowPosition[startPos:]:
            noteListItem = noteList[index]
            noteWidth = max(len(s) for s in noteListItem)
            for i in range(len(noteListItem)):
                if len(noteListItem) < maxNoteListLength:
                    for x in range(maxNoteListLength-len(noteListItem)):
                        noteListItem.append(' ' * noteWidth)

        if (columnCount+1) == startPos:
            noteListFormatted = noteList[columnCount+1]
        else:
            noteListRow = noteList[startPos:columnCount+1]

            noteListFormatted = zip(*noteListRow)

            noteListFormatted = list(noteListFormatted)

        # Center Notes
        centerSpaceIterator = round(abs((self.termWidth - len(re.sub("['',()]", '', str(noteListFormatted[0])).strip('[]')))/2))
        centerSpace = ''

        for i in range(centerSpaceIterator):
            centerSpace += ' '

        if (columnCount+1) == startPos:
            noteListFormatted = noteList[columnCount+1]
            for index in range(len(noteListFormatted)):
                noteListFormatted[index] = centerSpace + noteListFormatted[index]

            for i in range(len(noteListFormatted)):
                sys.stdout.write('\u001b[0;33m')
                if i == 1:
                    sys.stdout.write('\u001b[1;33m')
                print(noteListFormatted[i])

        else:
            for index in range(len(noteListFormatted)):
                noteListFormatted[index] = list(noteListFormatted[index])
                noteListFormatted[index][0] = centerSpace + noteListFormatted[index][0]

            for i in range(len(noteListFormatted)):
                sys.stdout.write('\u001b[0;33m')
                if i == 1:
                    sys.stdout.write('\u001b[1;33m')
                print(re.sub("['',()]", '', str(noteListFormatted[i])).strip('[]'))

    def getColumnCount(self):
        return columnCount

    def printKeepGrid():
        pass
