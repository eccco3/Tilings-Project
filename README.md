    This is a school project from my scientific computing class.
    It takes a binary matrix (list of lists) and an integer tuple as inputs:
- The binary matrix represents a grid where 0's are empty cells and 1's are blocked off cells. 
- The tuple represents a pair of dimensions of an L-shaped tile, so that for example (2,3) or (3,2) would be an L shaped like the movement of a Chess knight, and (2,1) or (1,2) would be a degenerate L shaped like a domino. 
    The program must find all possible tilings of the grid with the tile, and display up to 2 of them picked randomly. 
    I used DFS to solve this problem and displayed the results in a simple GUI.
