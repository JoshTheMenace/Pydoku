import random
l = "532986714174253986698471253853697421246815379719324865967138542425769138381542697"
difficulty = 1


def main(boardString,difficulty):
    return locateSpaces(boardString,difficulty)




def locateSpaces(boardString,difficulty):

    boardList = []
    for i in boardString:#Convert the board into a list
        boardList.append(i)

    count = 0
    boardListWithSpaces = boardList
    while count < difficulty:#loop and get random space
        randInBoard = random.randint(1,(len(boardListWithSpaces)-1))#get index of space and mirrored space
        mirrorSpace = len(boardListWithSpaces)-randInBoard

        if randInBoard and mirrorSpace != 0:#set value to 0 if space is not 0
            boardListWithSpaces[randInBoard] = 0
            boardListWithSpaces[mirrorSpace] = 0
            count = count + 1
        else:

            continue

    newBoardString = ''.join(str(boardList))
    formattedBoardString = newBoardString.replace('[', r'').replace('\'', r'').replace(',', r'').replace(']', r'').replace(' ', r'')
    return formattedBoardString


