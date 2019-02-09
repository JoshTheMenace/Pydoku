from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import random
savePath = []
entries = []
rBoard = []
'''
BUGS
1. doesnt have to be the right stringBoard to display congrats                      FIXED
2. delete file in save diolog does not open a new save as when clicking save
3. Make default size bigger and change placement of buttons and lines
'''

def initialize(top, arr):
    E = entries[0]
    m = 1
    for i in range(9):
        for j in range(9):
            if (not E.get()):
                arr[i][j] = 0
            else:
                arr[i][j] = int(E.get())
            if (m <= 80):
                E = entries[m]
                m += 1

def print_maze(arr):

    E = entries[0]
    m = 1
    completedString = ""
    for i in range(9):
        for j in range(9):

            completedString += str(arr[i][j])
            if (m <= 80):
                E = entries[m]
                m += 1

    return completedString


def find_empty_location(arr, l):
    for row in range(9):
        for col in range(9):
            if (arr[row][col] == 0):
                l[0] = row
                l[1] = col
                return True
    return False


def used_in_row(arr, row, num):
    for i in range(9):
        if (arr[row][i] == num):
            return True
    return False


def used_in_col(arr, col, num):
    for i in range(9):
        if (arr[i][col] == num):
            return True
    return False


def used_in_box(arr, row, col, num):
    for i in range(3):
        for j in range(3):
            if (arr[i + row][j + col] == num):
                return True
    return False


def check_location_is_safe(arr, row, col, num):
    return not used_in_row(arr, row, num) and not used_in_col(arr, col, num) and not used_in_box(arr, row - row % 3,
                                                                                                 col - col % 3, num)

def solve_sudoku(arr):
    l=[0,0]
    if(not find_empty_location(arr,l)):
        return True
    row=l[0]
    col=l[1]
    for num in range(1,10):
        if(check_location_is_safe(arr,row,col,num)):
            arr[row][col]=num
            if(solve_sudoku(arr)):
                return True
            arr[row][col] = 0
    return False


def convertEntriesToString():
    savedFormattedString = ""
    for count, elem in enumerate(entries):
        if elem.get() == "" or elem.get() == " ":
            savedFormattedString += "0"
        else:
            savedFormattedString += elem.get()
    return savedFormattedString


def putStringToBoard(arr):
    for count, elem in enumerate(entries):

        valueToPass = arr[count]
        if valueToPass == "0":
            elem.delete(0, END)
            continue
        else:
            elem.delete(0, END)
            elem.insert(0, valueToPass)
        realBoardString = print_maze(maze)
        rBoard.append(realBoardString)


def createGUI(maze):
    top = Tk()
    top.resizable(False, False)
    top.title("Sudoku: By, Josh Gimenes")
    top.iconbitmap(r'C:\Users\harry\Desktop\favicon.ico')
    canvas = Canvas(top, height=320, width=350)
    createRow(canvas)
    createCol(canvas)
    createEntry(top)
    createButtons(top)
    createMenuBar(top)
    canvas.pack(side='top')
    top.mainloop()



def createButtons(top):
    button_new = Button(top, text="Submit", justify='right', command=lambda: checkForCompletion(top,maze))
    button_hint = Button(top, text="Hint", justify='left', command=lambda: give_hint(top))
    button_hint.place(x=70, y=275, height=30, width=60)
    button_new.place(x=230, y=275, height=30, width=60)

def clean_Mess():
    for e in entries:
        e.delete(0, END)

def createMenuBar(top):
    menubar = Menu(top)
    newGameMenu = Menu(top,tearoff = 0)
    filemenu = Menu(top, tearoff=0)
    filemenu.add_command(label="Save", command=lambda: save_game(top))
    filemenu.add_separator()
    filemenu.add_command(label="Save As", command=lambda: save_as(top))
    filemenu.add_separator()
    filemenu.add_command(label="Load", command=lambda: load_file(top))
    filemenu.add_separator()
    filemenu.add_cascade(label="New",menu=newGameMenu)
    menubar.add_cascade(label="File", menu=filemenu)

    newGameMenu.add_command(label="Easy",command=lambda: arrangeEasy(top))
    newGameMenu.add_command(label="Intermediate",command=lambda: arrangeIntermediate(top))
    newGameMenu.add_command(label="Hard",command=lambda: arrangeHard(top))

    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_separator()
    top.config(menu=menubar)


def save_game(top):


    if len(savePath) == 0:
        save_as(top)
    else:
        pathToSave = savePath[len(savePath)-1]
        file = open(top.filename + ".sku", "w")

        file.write(convertEntriesToString())



def give_hint(top):
    listOfZeroIndexes = []
    initialize(top, maze)
    if (solve_sudoku(maze)):
        realBoardString = print_maze(maze)
        currentBoardString = convertEntriesToString()
        if currentBoardString != realBoardString:
            for count, elem in enumerate(currentBoardString):
                if elem == "0":
                    listOfZeroIndexes.append(count)
            randomIndex = random.choice(listOfZeroIndexes)
            hintValue = realBoardString[randomIndex]

            entries[randomIndex].insert(0, hintValue)
            if (solve_sudoku(maze)):
                realBoardString = print_maze(maze)
                rBoard.append(realBoardString)



def checkForCompletion(top,maze):
    initialize(top, maze)
    if (solve_sudoku(maze)):
        if(rBoard[len(rBoard)-1] == convertEntriesToString()):
            messagebox.showinfo("Sudoku", "Congratulations! You have successfully\n completed the puzzle!")
        else:
            messagebox.showwarning("Sudoku", "Sorry but the puzzle is not correct.")
    else:
        print("No solution found!")



def save_as(top):

    top.filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                   filetypes=(("sku file", "*.txt"), ("all files", "*.*")))
    file = open(top.filename+".sku", "w+")

    file.write(convertEntriesToString())
    if(top.filename != ""):
        savePath.append(top.filename)



def arrangeEasy(top):
    for count, elem in enumerate(entries):
        elem.delete(0,END)
    difficulty = 1
    start_new_game(top,difficulty)


def arrangeIntermediate(top):
    for count, elem in enumerate(entries):
        elem.delete(0,END)
    difficulty = 20
    start_new_game(top,difficulty)

def arrangeHard(top):
    for count, elem in enumerate(entries):
        elem.delete(0,END)
    difficulty = 30
    start_new_game(top,difficulty)


def start_new_game(top,difficulty):

    import sudokuGenerateVB
    sudokuString = sudokuGenerateVB.start()
    import sudokuRemoveSpaces
    newBoardString = sudokuRemoveSpaces.main(sudokuString,difficulty)
    for count, elem in enumerate(entries):

        valueToPass = newBoardString[count]
        if valueToPass == "0":
            continue
        else:
            elem.delete(0,END)
            elem.insert(0, valueToPass)
    initialize(top, maze)
    if (solve_sudoku(maze)):
        realBoardString = print_maze(maze)
        rBoard.append(realBoardString)




def load_file(top):

    top.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                filetypes=(("sku files", "*.sku"), ("all files", "*.*")))
    try:
        file = open(top.filename, "r")
        sudokuString = file.read()

        if(len(sudokuString) == 81 and sudokuString.isdigit() == True):
            putStringToBoard(sudokuString)
            savePath.append(top.filename)
            if (solve_sudoku(maze)):
                realBoardString = print_maze(maze)
                rBoard.append(realBoardString)

        else:
            messagebox.showerror("Error", "Cannot Load File. File is not correctly formatted.")

    except FileNotFoundError:
        pass


def createEntry(top):
    p, q = 41.4, 41.4
    for i in range(9):
        for j in range(9):
            E = Entry(top, width=3, font='BOLD')
            E.grid(row=i, column=j)
            E.place(x=p, y=q, height=20, width=25)
            entries.append(E)
            p += 30.0
        q += 24.5
        p = 41.2


def createRow(canvas):
    i, j = 40, 40
    p = 40
    q = 260
    for m in range(10):
        if (m % 3 == 0):
            canvas.create_line(i, j, p, q, width=6)
        else:
            canvas.create_line(i, j, p, q, width=1.5)
        i += 30
        p += 30


def createCol(canvas):
    t = 1.5
    i, j = 40, 40
    p, q = 310, 40
    for m in range(10):
        if m == 3 or m == 6 or m == 0 or m == 9:
            t = 6
        else:
            t = 1.5
        canvas.create_line(i, j, p, q, width=t)
        j += 24.5
        q += 24.5


if __name__ == "__main__":
    maze = [[0 for x in range(9)] for y in range(9)]
    createGUI(maze)