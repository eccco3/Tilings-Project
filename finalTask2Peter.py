import sys
import copy
import tkinter as tkr
import random

tilingList = [] #holds successful tilings
stack = [] #holds the tiles of our current attempt at tiling

def tilings(matrix,tileCount): #compute tilings, append the stack to tilinglist if the matrix is filled
    global stack
    global tilingList

    if matrix == None: #this happens when placeTile() cannot place a tile in some orientation at some location
        return
    for i in range(0,m):
        for j in range(0,n):
            if matrix[i][j] == 0:
                tilings(placeTile(1, copy.deepcopy(matrix),i,j,False,tileCount),tileCount+1)
                if tileDims[0] != 1 and tileDims[1] != 1: #prevent double-counting if tile is one-dimensional
                    tilings(placeTile(2, copy.deepcopy(matrix),i,j,False,tileCount),tileCount+1)
                    tilings(placeTile(3, copy.deepcopy(matrix),i,j,False,tileCount),tileCount+1)
                    tilings(placeTile(4, copy.deepcopy(matrix),i,j,False,tileCount),tileCount+1)
                if tileDims[0]!=tileDims[1]: #prevent double-counting if tile has equal dimensions
                    tilings(placeTile(1, copy.deepcopy(matrix),i,j,True,tileCount),tileCount+1)
                    if tileDims[0] != 1 and tileDims[1]!=1: #prevent double-counting if tile is one-dimensional
                        tilings(placeTile(2, copy.deepcopy(matrix),i,j,True,tileCount),tileCount+1)
                        tilings(placeTile(3, copy.deepcopy(matrix),i,j,True,tileCount),tileCount+1)
                        tilings(placeTile(4, copy.deepcopy(matrix),i,j,True,tileCount),tileCount+1)
                return
    tilingList.append(copy.deepcopy(stack))
    return

def placeTile(orientation,matrix,row,col,inverted,tileCount):
    """If a tile can be placed at matrix[row][col]  then this function returns the new matrix with that tile placed. 
    
    The orientations are ordered by the quadrant the L opens towards:
    orientation 1 is L, 
    orientation 2 is backwards L,     
    orientation 3 is upside-down backwards L, 
    orientation 4 is upside-down L.
    
    If inverted == True, then the tileDimensions are inverted to give another orientation. If it's False, they aren't.
    
    Returns None if it is not possible to place the tile as specified. If tilings() receives None, it will itself return."""
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
        
    #check if the entries are 0 and fill them if they are
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
    stack.append((row,col,orientation,inverted))
    return matrix


#GUI and Input
    
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


def inputParameters():
    #when the button is pressed
    
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
    #draws the matrix
    for i in range(0,m+1):
        canv.create_line(0,50*i+4,50*len(userMatrix[0])+3,50*i+4,width=4)
    for j in range(0,n+1):
        canv.create_line(50*j+4,0,50*j+4,50*len(userMatrix)+6,width=4)
    for i in range(0,m):
        for j in range(0,n):
            if userMatrix[i][j] == 1:
                canv.create_rectangle(50*j+4,50*i+4,50*(j+1)+4,50*(i+1)+4,fill="black")


def drawTiling(canv): 
    #draws the tiling onto the matrix, removes the tiling from tilingList
    global tilingList
    tilingNumber = random.randrange(0,len(tilingList))
    tiling = copy.deepcopy(tilingList[tilingNumber])
    tilingList.pop(tilingNumber)
    tiledCanv = canv
    for tile in tiling:
        if tile[2] == 1: #orientation 1
            tiledCanv.create_rectangle(tile[1]*50 + 10, (tile[0]+tileDims[tile[3]]-1)*50 + 10, (tile[1] + tileDims[1-tile[3]])*50 - 2 ,(tile[0]+tileDims[tile[3]])*50 - 2, fill="blue", outline="")
            tiledCanv.create_rectangle(tile[1]*50 + 10, tile[0]*50 + 10, (tile[1]+1)*50 -2, (tile[0] + tileDims[tile[3]])*50 - 2, fill="blue", outline="")
        if tile[2] == 2: #orientation 2
            tiledCanv.create_rectangle((tile[1] - tileDims[1-tile[3]] + 1)*50 + 10, (tile[0]+tileDims[tile[3]]-1)*50 + 10, (tile[1]+1)*50 - 2 ,(tile[0]+tileDims[tile[3]])*50 - 2, fill="blue", outline="")
            tiledCanv.create_rectangle(tile[1]*50 + 10, tile[0]*50 + 10, (tile[1]+1)*50 -2, (tile[0] + tileDims[tile[3]])*50 - 2, fill="blue", outline="")
        if tile[2] == 3: #orientation 3
            tiledCanv.create_rectangle(tile[1]*50 + 10, tile[0]*50 + 10, (tile[1] + tileDims[1-tile[3]]) *50 - 2,(tile[0]+1)*50 - 2, fill="blue", outline="")
            tiledCanv.create_rectangle((tile[1]+tileDims[1-tile[3]]-1)*50 + 10, tile[0]*50 + 10, (tile[1]+tileDims[1-tile[3]])*50 - 2, (tile[0]+tileDims[tile[3]])*50 - 2, fill="blue", outline="")
        if tile[2] == 4: #orientation 4
            tiledCanv.create_rectangle(tile[1]*50 + 10, tile[0]*50 + 10, (tile[1] + tileDims[1-tile[3]]) *50 - 2,(tile[0]+1)*50 - 2, fill="blue", outline="")
            tiledCanv.create_rectangle(tile[1]*50 + 10, tile[0]*50 + 10, (tile[1]+1)*50 -2, (tile[0] + tileDims[tile[3]])*50 - 2, fill="blue", outline="")


tileButton = tkr.Button(window, text="Tile", command = inputParameters)
tileButton.pack()

window.mainloop()
   
   
   
   
