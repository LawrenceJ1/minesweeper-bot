from time import sleep
import pyautogui

#CURRENTLY ONLY WORKS FOR 200% ZOOM ON 1080x1920 MONITOR

# RGB Values for every number
colors = [(255, 255, 255), (0, 0, 255), (0, 123, 0), (255, 0, 0), (0, 0, 123), (0, 123, 123), (0, 0, 0), (123, 123, 123), (300, 300, 300)]
# UNCHECKED = (255, 255, 255), top left will be checked for this
# ONE = (0, 0, 255)
# TWO = (0, 123, 0)
# THREE = (255, 0, 0)
# FOUR = (0, 0, 123)
# FIVE = (123, 0, 0)
# SIX = (0, 123, 123)
# SEVEN = (0, 0, 0)
# EIGHT = (123, 123, 123)

boxes = []
visited = set()

for i in pyautogui.locateAllOnScreen("square.png", confidence=0.98):
    _, _, box_width, box_height = i
    z = pyautogui.center(i)
    x, y = z
    boxes.append([x+3, int(y-0.25*box_height)])

#determining the difficulty
if len(boxes) == 81:
    model = [[0 for _ in range(9)] for _ in range(9)]
    mines = 10
elif len(boxes) == 256:
    model = [[0 for _ in range(16)] for _ in range(16)]
    mines = 40
else:
    model = [[0 for _ in range(30)] for _ in range(16)]
    mines = 99

#the game will start with a click on the top left box
pyautogui.click(x=boxes[0][0], y=boxes[0][1])

# The numbers 1-8 represent the number of mines around a square, while the number -1 is an unchecked square and the number
# 9 is a checked square that has no more mines around it. The number 10 will represent a flag

#gets a model for the board
row, col = 0, 0
m, n = len(model), len(model[0])
tolerance = 5
for box in boxes:
    if (box[0], box[1]) in visited:
        continue
    pix = pyautogui.pixel(int(box[0]), int(box[1]))
    for i in range(10):
        if i == 0:
            if pyautogui.pixel(int(box[0]-3-box_width/2), int(box[1])) == colors[i]:
                model[row][col] = -1
                break
        elif i == 9:
            model[row][col] = i
            visited.add((box[0], box[1]))
            break
        elif (abs(pix[0]-colors[i][0]) <= tolerance) and (abs(pix[1]-colors[i][1]) <= tolerance) and (abs(pix[2]-colors[i][2]) <= tolerance):
            model[row][col] = i
            visited.add((box[0], box[1]))
            break
    col += 1
    if col == n:
        row += 1
        col = 0

#check for obvious flags
for i in range(len(model)):
    for j in range(len(model[i])):
        if model[i][j] != -1 and model[i][j] != 9 and model[i][j] != 10:
            sqaures_around = 0
            squares = []
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if i+x >= 0 and j+y >= 0 and i+x < len(model) and j+y < len(model[0]) and model[i+x][j+y] == -1:
                        sqaures_around += 1
                        squares.append([i+x, j+y])
            if sqaures_around == model[i][j]:
                for square in squares:
                    model[square[0]][square[1]] = 10
                    pyautogui.rightClick(boxes[square[0]*len(model[0])+square[1]][0], boxes[square[0]*len(model[0])+square[1]][1])
                    mines -= 1
                    visited.add((boxes[square[0]*len(model[0])+square[1]][0], boxes[square[0]*len(model[0])+square[1]][1]))
                    for x in range(-1, 2):
                        for y in range(-1, 2):
                            if square[0]+x >= 0 and square[1]+y >= 0 and square[0]+x < len(model) and square[1]+y < len(model[0]) and model[square[0]+x][square[1]+y] != -1 and model[square[0]+x][square[1]+y] != 9 and model[square[0]+x][square[1]+y] != 10:
                                model[square[0]+x][square[1]+y] -= 1
                                
#click squares where there are no more mines
for row in range(len(model)):
    for col in range(len(model[col])):
        if model[row][col] == 0:
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if row+x >= 0 and col+y >= 0 and row+x < len(model) and col+y < len(model[0]) and (boxes[(row+x)*len(model[0])+col+y][0], boxes[(row+x)*len(model[0])+col+y][1]) not in visited:
                        pyautogui.click(boxes[(row+x)*len(model[0])+col+y][0], boxes[(row+x)*len(model[0])+col+y][1])
                        visited.add((boxes[(row+x)*len(model[0])+col+y][0], boxes[(row+x)*len(model[0])+col+y][1]))
                        