
class KeepGrid:
    """
    """

    def __init__(self, googleNotes, termWidth):
        self.googleNotes = googleNotes
        self.termWidth = termWidth

    def listifyGoogleNotes(self, googleNotes):
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

    def addListBorder(self, nestedList):
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

    def printRow(self, nestedList, startPos):
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
        centerSpaceIterator = abs((width - len(str(nestedListFormatted[0])))//2)+1
        centerSpace = ''

        for i in range(centerSpaceIterator):
            centerSpace += ' '

        if (columnCount+1) == startPos:
            nestedListFormatted = nestedList[columnCount+1]
            for index in range(len(nestedListFormatted)):
                nestedListFormatted[index] = centerSpace + nestedListFormatted[index]

            for i in range(len(nestedListFormatted)):
                sys.stdout.write('\u001b[0;33m')
                if i == 1:
                    sys.stdout.write('\u001b[1;33m')
                print(nestedListFormatted[i])

        else:
            for index in range(len(nestedListFormatted)):
                nestedListFormatted[index] = list(nestedListFormatted[index])
                nestedListFormatted[index][0] = centerSpace + nestedListFormatted[index][0]

            for i in range(len(nestedListFormatted)):
                sys.stdout.write('\u001b[0;33m')
                if i == 1:
                    sys.stdout.write('\u001b[1;33m')
                print(re.sub("['',()]", '', str(nestedListFormatted[i])).strip('[]'))
