import sys
import copy
import tkinter as tkr
import random

"""
    This is a school project from my scientific computing class.
    It takes a binary matrix (list of lists) and an integer tuple as inputs, and outputs as follows: 
    The binary matrix represents a grid where 0's are empty cells and 1's are blocked off cells. 
    The tuple represents a pair of dimensions of an L-shaped tile, 
        so that for example (2,3) or (3,2) would be an L shaped like the movement of a Chess knight,
        and (2,1) or (1,2) would be a degenerate L shaped like a domino. 
    The program must find all possible tilings of the grid with the tile,
        and display up to 2 of them picked randomly. 
    I used DFS to solve this problem and displayed the results in a simple GUI.
"""


stack = [] #holds the tiles of our current attempt to tile the grid
tilingList = [] #holds successful tilings (copies of the stack)


def tilings(matrix,tileCount): 
    """
    Recursively computes all possible tilings of the matrix using DFS starting at the
    topmost,leftmost empty cell.
    
    matrix: list of lists of binary numbers representing a grid of possibly blocked off cells.
    tileCount: int indicating how full the global stack should be. placeTile() will shed excess tiles.
    returns: None
    """
    global stack
    global tilingList

    if matrix == None: #this happens when placeTile() cannot place a tile in some orientation at some location
        return
    
    for i in range(0,m):
        for j in range(0,n):
            if matrix[i][j] == 0:
                tilings(placeTile(orientation = 1, matrix = copy.deepcopy(matrix),row = i,col = j,
                                  inverted = False, tileCount = tileCount), tileCount+1)
                #prevent double-counting if tile is one-dimensional
                if tileDims[0] != 1 and tileDims[1] != 1:
                    tilings(placeTile(orientation = 2, matrix = copy.deepcopy(matrix),row = i,col = j,
                                      inverted = False, tileCount = tileCount), tileCount+1)
                    tilings(placeTile(orientation = 3, matrix = copy.deepcopy(matrix),row = i,col = j,
                                      inverted = False, tileCount = tileCount), tileCount+1)
                    tilings(placeTile(orientation = 4, matrix = copy.deepcopy(matrix),row = i,col = j,
                                      inverted = False, tileCount = tileCount), tileCount+1)
                #prevent double-counting if tile has equal dimensions
                if tileDims[0]!=tileDims[1]: 
                    tilings(placeTile(orientation = 1, matrix = copy.deepcopy(matrix),row = i,col = j,
                                      inverted = True, tileCount = tileCount), tileCount+1)
                    #prevent double-counting if tile is one-dimensional
                    if tileDims[0] != 1 and tileDims[1]!=1: 
                        tilings(placeTile(orientation = 2, matrix = copy.deepcopy(matrix),row = i,col = j,
                                          inverted = True, tileCount = tileCount), tileCount+1)
                        tilings(placeTile(orientation = 3, matrix = copy.deepcopy(matrix),row = i,col = j,
                                          inverted = True, tileCount = tileCount), tileCount+1)
                        tilings(placeTile(orientation = 4, matrix = copy.deepcopy(matrix),row = i,col = j,
                                          inverted = True, tileCount = tileCount), tileCount+1)
                return
    #matrix is full so we have a successful tiling
    tilingList.append(copy.deepcopy(stack))

def placeTile(orientation,matrix,row,col,inverted,tileCount):
    """
    If a tile can be placed at matrix[row][col] then this function adds that tile to the stack and
    returns the new matrix with that tile placed. 
    
    orientation: int indicating the quadrant the L opens towards:
        orientation 1 is L, 
        orientation 2 is backwards L,
        orientation 3 is upside-down backwards L,
        orientation 4 is upside-down L.
    matrix: list of lists of bits representing the grid to be tiled
    row: int indicating the row of the topmost point of the tile
    col: int indicating the column of the leftmost point of the tile
    inverted: boolean indicating whether the tile dimensions should be inverted to get another orientation.
    tileCount: int indicating how full the global stack should be. placeTile() will shed excess tiles.
    returns: None if it is not possible to place the tile as specified. Returns the tiled matrix otherwise.
    """
    global stack
    dims = tileDims
    
    if inverted:
        dims = (tileDims[1],tileDims[0])
    
    while len(stack)>tileCount: #While we have leftover tiles from earlier tiling attempts
        stack.pop()

    #check if it's even possible to tile based on our position and the dimensions of the matrix
    if dims[0]+row>m: 
        return None
    if orientation == 1 or orientation == 3 or orientation == 4:
        if dims[1]+col>n: 
            return None
    if orientation == 2:
        if col-(dims[1]-1)<0: 
            return None
    
    #check if the entries are 0 and fill them if they are. Return None if any are blocked.
    if orientation == 1: #L (down-then-right)
        for i in range(row, row+dims[0]): #check and fill the column
            if matrix[i][col] == 0:
                matrix[i][col] = 1
            else:
                return None
        for j in range(col+1, col+dims[1]): #from there check and fill the row
            if matrix[row+dims[0]-1][j] == 0:
                matrix[row+dims[0]-1][j] = 1
            else:
                return None
    if orientation == 2: #backwards L (down-then-left)
        for i in range(row, row+dims[0]): #check and fill the column
            if matrix[i][col] == 0:
                matrix[i][col] = 1
            else:
                return None
        for j in range(col-dims[1]+1, col): #from there check and fill the row
            if matrix[row+dims[0]-1][j] == 0:
                matrix[row+dims[0]-1][j] = 1
            else:
                return None
    if orientation == 3: #upside-down backwards L (right-then-down)
        for j in range(col, col+dims[1]): #check and fill the row
            if matrix[row][j] == 0:
                matrix[row][j] = 1
            else:
                return None
        for i in range(row+1, row+dims[0]): #from there check and fill the column
            if matrix[i][col+dims[1]-1] == 0:
                matrix[i][col+dims[1]-1] = 1
            else:
                return None
    if orientation == 4: #upside-down L (down-then-back-then-right)
        for i in range(row, row+dims[0]): #check and fill the column
            if matrix[i][col] == 0:
                matrix[i][col] = 1
            else:
                return None
        for j in range(col+1, col+dims[1]): #go back and then check and fill the row
            if matrix[row][j] == 0:
                matrix[row][j] = 1
            else:
                return None
    stack.append((row,col,orientation,inverted)) #add the tile to the stack
    return matrix


def buttonPressed():
    """
    Called when the data is entered and the button within the GUI is clicked.
    Processes the inputs and calls tilings(). Up to 2 tilings are chosen randomly and displayed.
    
    returns: None
    """
    
    try:
        userMatrix = [[int(j.replace('[','').replace(']','')) for j in row.split(',')] for row in matrixTxt.get()[1:-1].split('],[')]
    except: 
        print("Error: Binary matrix entered in incorrect format.")
        window.destroy()
    
    try: 
        global tileDims
        tileDims = (int(tileTxt.get()[1]),int(tileTxt.get()[3]))
    except: 
        print("Error: Please input a positive integer ordered pair in the format (a,b).")
        window.destroy()

    if (tileDims[0] < 1 or tileDims[1]<1):
        window.destroy()
        sys.exit("Error: Tile dimensions must be positive.")
    global m
    global n
    m = len(userMatrix)
    n = len(userMatrix[0])
    tilings(userMatrix,0)
    print(len(tilingList))
    
    #draw the bare matrix and label it
    canv1 = tkr.Canvas(window, width=50*len(userMatrix[0])+4, height=50*len(userMatrix)+4)      
    drawMatrix(canv1,userMatrix)
    canv1.pack()
    
    infoLbl = tkr.Label(window,text="There are " + str(len(tilingList)) + " tiling(s) of this matrix with the tile you specified.", font=("Comic Sans MS",14))
    infoLbl.pack()
    
    #if there exist tilings, pick up to 2 of them and draw them (drawTiling() pops a tiling from tilingList)
    if len(tilingList)>0:
        canv2 = tkr.Canvas(window, width=50*len(userMatrix[0])+4, height=50*len(userMatrix)+4)
        drawMatrix(canv2,userMatrix)
        drawTiling(canv2)
        canv2.pack()
    if len(tilingList)>0:
        canv3 = tkr.Canvas(window, width=50*len(userMatrix[0])+4, height=50*len(userMatrix)+4)
        drawMatrix(canv3,userMatrix)
        drawTiling(canv3)
        canv3.pack()
      
        
def drawMatrix(canv,userMatrix):
    for i in range(0,m+1):
        canv.create_line(0,50*i+4,50*len(userMatrix[0])+3,50*i+4,width=4)
    for j in range(0,n+1):
        canv.create_line(50*j+4,0,50*j+4,50*len(userMatrix)+6,width=4)
    for i in range(0,m):
        for j in range(0,n):
            if userMatrix[i][j] == 1:
                canv.create_rectangle(50*j+4,50*i+4,50*(j+1)+4,50*(i+1)+4,fill="black")


def drawTiling(canv): 
    global tilingList
    
    #pick a random tiling and pop it from tilingList so that we don't use it twice
    tilingNumber = random.randrange(0,len(tilingList))
    tiling = copy.deepcopy(tilingList[tilingNumber])
    tilingList.pop(tilingNumber)
    
    for tile in tiling:
        if tile[2] == 1: #orientation 1
            canv.create_rectangle(tile[1]*50 + 10, (tile[0] + tileDims[tile[3]] - 1)*50 + 10, 
                                  (tile[1] + tileDims[1-tile[3]])*50 - 2, (tile[0] + tileDims[tile[3]])*50 - 2, 
                                  fill="blue", outline="")
            canv.create_rectangle(tile[1]*50 + 10, tile[0]*50 + 10, 
                                  (tile[1]+1)*50 -2, (tile[0] + tileDims[tile[3]])*50 - 2, 
                                  fill="blue", outline="")
        if tile[2] == 2: #orientation 2
            canv.create_rectangle((tile[1] - tileDims[1-tile[3]] + 1)*50 + 10, (tile[0]+tileDims[tile[3]]-1)*50 + 10,
                                  (tile[1]+1)*50 - 2 ,(tile[0]+tileDims[tile[3]])*50 - 2,
                                  fill="blue", outline="")
            canv.create_rectangle(tile[1]*50 + 10, tile[0]*50 + 10, 
                                  (tile[1]+1)*50 -2, (tile[0] + tileDims[tile[3]])*50 - 2, 
                                  fill="blue", outline="")
        if tile[2] == 3: #orientation 3
            canv.create_rectangle(tile[1]*50 + 10, tile[0]*50 + 10, 
                                  (tile[1] + tileDims[1-tile[3]]) *50 - 2, (tile[0]+1)*50 - 2, 
                                  fill="blue", outline="")
            canv.create_rectangle((tile[1]+tileDims[1-tile[3]]-1)*50 + 10, tile[0]*50 + 10, 
                                  (tile[1]+tileDims[1-tile[3]])*50 - 2, (tile[0]+tileDims[tile[3]])*50 - 2, 
                                  fill="blue", outline="")
        if tile[2] == 4: #orientation 4
            canv.create_rectangle(tile[1]*50 + 10, tile[0]*50 + 10, 
                                  (tile[1] + tileDims[1-tile[3]]) *50 - 2, (tile[0]+1)*50 - 2, 
                                  fill="blue", outline="")
            canv.create_rectangle(tile[1]*50 + 10, tile[0]*50 + 10, 
                                  (tile[1]+1)*50 -2, (tile[0] + tileDims[tile[3]])*50 - 2, 
                                  fill="blue", outline="")

# Build GUI window
window = tkr.Tk()
window.title("Matrix Tilizationator")
window.geometry("1000x800")
matrixLbl = tkr.Label(window,text="Type a binary matrix below as a python list of lists, e.g. [[0 0], [0,0], [0,0]]", font=("Comic Sans MS",14))
matrixLbl.pack()
matrixTxt = tkr.Entry(window,width=10)
matrixTxt.pack()

tileLbl = tkr.Label(window,text="Type a pair of tile dimensions below as a python tuple of integers, e.g. (2,2)", font=("Comic Sans MS",14))
tileLbl.pack()
tileTxt = tkr.Entry(window,width=10)
tileTxt.pack()

tileButton = tkr.Button(window, text="Tile", command = buttonPressed)
tileButton.pack()

window.mainloop()
   
   
   
   
