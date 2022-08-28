from time import sleep
import pyautogui

#CURRENTLY ONLY WORKS FOR 200% ZOOM ON 1080x1920 MONITOR

# UNCHECKED = (255, 255, 255)
# ONE = (0, 0, 255)
# TWO = (0, 123, 0)
# THREE = (255, 0, 0)
# FOUR = (0, 0, 123)
# FIVE = (123, 0, 0)
# SIX = (0, 123, 123)
# SEVEN = (0, 0, 0)
# EIGHT = (123, 123, 123)

# The numbers 1-8 represent the number of mines around a square, while the number -1 is an unchecked square and the number
# 9 is a checked square that has no more mines around it. The number 10 will represent a flag

class Program:
    def __init__(self) -> None:
        # RGB Values for every number
        self.colors = [(255, 255, 255), (0, 0, 255), (0, 123, 0), (255, 0, 0), (0, 0, 123), (123, 0, 0), (0, 123, 123), (0, 0, 0), (123, 123, 123), (300, 300, 300)]
        self.boxes = []
        self.visited = set()
        self.box_width = 0
        self.box_height = 0
        self.mines = 0
        self.model = [[]]
        #adds 1 to the model value after the first pass, because each unchecked square is set to -1 rather than 0
        self.first_pass_flag = 0
        #if some action advanced the board, self.changes will equal 1
        self.changes = 0

    def initializeBoard(self) -> None:
        """Gets the position of each of the boxes on the minesweeper board, as well as initializes the model and the number of mines"""
        for i in pyautogui.locateAllOnScreen("square.png", confidence=0.98):
            _, _, self.box_width, self.box_height = i
            z = pyautogui.center(i)
            x, y = z
            # self.boxes.append([x+3, int(y-0.27*self.box_height)]) 
            self.boxes.append([x+3, y]) 
            #IMPORTANT: FINE TUNE PARAMETERS TO GET PROPER MODEL

        #determining the difficulty
        if len(self.boxes) == 81:
            self.model = [[0 for _ in range(9)] for _ in range(9)]
            self.mines = 10
        elif len(self.boxes) == 256:
            self.model = [[0 for _ in range(16)] for _ in range(16)]
            self.mines = 40
        else:
            self.model = [[0 for _ in range(30)] for _ in range(16)]
            self.mines = 99

    def startGame(self) -> None:
        """The game will start with a click on the top left box"""
        pyautogui.click(x=self.boxes[0][0], y=self.boxes[0][1])


    def getModel(self) -> None:
        """Updates the model for the board"""
        row, col = 0, 0
        m, n = len(self.model), len(self.model[0])
        tolerance = 5
        for box in self.boxes:
            if (box[0], box[1]) in self.visited:
                col += 1
                if col == n:
                    row += 1
                    col = 0
                continue
            pix = pyautogui.pixel(int(box[0]), int(box[1]))
            for i in range(10):
                if i == 0:
                    if pyautogui.pixel(int(box[0]-3-self.box_width/2), int(box[1])) == self.colors[i]:
                        if self.first_pass_flag:
                            break
                        self.model[row][col] = -1
                        break
                elif i == 9:
                    self.model[row][col] += i+self.first_pass_flag
                    self.visited.add((box[0], box[1]))
                    break
                elif (abs(pix[0]-self.colors[i][0]) <= tolerance) and (abs(pix[1]-self.colors[i][1]) <= tolerance) and (abs(pix[2]-self.colors[i][2]) <= tolerance):
                    self.model[row][col] += i+self.first_pass_flag
                    self.visited.add((box[0], box[1]))
                    break
            col += 1
            if col == n:
                row += 1
                col = 0

    def placeObviousFlags(self) -> None:
        """Places a flag where there is only one possible location that a mine could be in"""
        for i in range(len(self.model)):
            for j in range(len(self.model[i])):
                # Only continue if the square is numbered
                if self.model[i][j] > 0 and self.model[i][j] != 9 and self.model[i][j] != 10:
                    sqaures_around = 0
                    squares = []
                    
                    # Gets the number of unknown squares around a numbered square
                    for x in range(-1, 2):
                        for y in range(-1, 2):
                            if i+x >= 0 and j+y >= 0 and i+x < len(self.model) and j+y < len(self.model[0]) and self.model[i+x][j+y] < 0:
                                sqaures_around += 1
                                squares.append([i+x, j+y])
                                
                    # If the number of unknown squares is equal to the number on the square, then they all must be mines, so flags are placed at each square
                    if sqaures_around == self.model[i][j]:
                        for square in squares:
                            self.model[square[0]][square[1]] = 10
                            pyautogui.rightClick(self.boxes[square[0]*len(self.model[0])+square[1]][0], self.boxes[square[0]*len(self.model[0])+square[1]][1])
                            self.mines -= 1
                            self.visited.add((self.boxes[square[0]*len(self.model[0])+square[1]][0], self.boxes[square[0]*len(self.model[0])+square[1]][1]))
                            for x in range(-1, 2):
                                for y in range(-1, 2):
                                    if square[0]+x >= 0 and square[1]+y >= 0 and square[0]+x < len(self.model) and square[1]+y < len(self.model[0]) and self.model[square[0]+x][square[1]+y] != 9 and self.model[square[0]+x][square[1]+y] != 10:
                                        self.model[square[0]+x][square[1]+y] -= 1
                                        self.changes = 1
    
    def clickEmptySquares(self) -> None:           
        """Click squares where there are no more mines"""
        for row in range(len(self.model)):
            for col in range(len(self.model[row])):
                if self.model[row][col] == 0:
                    for x in range(-1, 2):
                        for y in range(-1, 2):
                            if row+x >= 0 and col+y >= 0 and row+x < len(self.model) and col+y < len(self.model[0]) and (self.boxes[(row+x)*len(self.model[0])+col+y][0], self.boxes[(row+x)*len(self.model[0])+col+y][1]) not in self.visited:
                                pyautogui.click(self.boxes[(row+x)*len(self.model[0])+col+y][0], self.boxes[(row+x)*len(self.model[0])+col+y][1])
                                self.changes = 1

    def dfs(self, model) -> None:
        """CURRENTLY A WORK IN PROGRESS. Tries to determine the location of mines through backtracking"""
        for row in range(len(model)):
            for col in range(len(model[row])):
                if self._isValid(model, row, col):
                    
                    # If the square is valid, then we need to pretend it's a mine and update the surrounding squares
                    model[row][col] = 10
                    for x in range(-1, 2):
                        for y in range(-1, 2):
                            if row+x >= 0 and col+y >= 0 and row+x < len(model) and col+y < len(model[0]) and model[row+x][col+y] != 9 and model[row+x][col+y] != 10 and model[row+x][col+y] != -1:
                                model[row+x][col+y] -= 1
                    
                    # If this leads to an inconsistency, then the square must actually not be a mine. An inconsistency is when a square still has a mine surrounding it, but there are no more squares that could be mines around it
                    #DELETE AFTER DONE
                    for i in range(len(model)):
                        print(model[i])
                    sleep(50000)
                                
                    # self.dfs(model)
                    
                    # # Resets the board to the previous state
                    # for x in range(-1, 2):
                    #     for y in range(-1, 2):
                    #         if row+x >= 0 and col+y >= 0 and row+x < len(model) and col+y < len(model[0]) and model[row+x][col+y] != 9 and model[row+x][col+y] != 10 and model[row+x][col+y] != -1:
                    #             model[row+x][col+y] += 1
                
    def _isValid(self, model, row, col) -> bool:
        """Returns true or false, depending on whether the position has any surrounding squares that aren't unknown"""
        if model[row][col] == -1:
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if row+x >= 0 and col+y >= 0 and row+x < len(model) and col+y < len(model[0]) and model[row+x][col+y] > 0 and model[row+x][col+y] < 9:
                        return True
        return False

    def clickAllSquares(self) -> None:
        """Once there are no mines left, run this function. This will click the remaining squares"""
        for box in self.boxes:
            if (box[0], box[1]) in self.visited:
                continue
            else:
                pyautogui.click(x=box[0], y=box[1])

    def run(self) -> None:
        """Runs the main program"""
        self.initializeBoard()
        self.startGame()
        while self.mines > 0:
            self.changes = 0
            self.getModel()
            self.placeObviousFlags()
            self.clickEmptySquares()
            self.first_pass_flag = 1
            
            #if we couldn't advance the board then we need to break the loop and use dfs
            if not self.changes:
                self.dfs(self.model)
            
        self.clickAllSquares()
        
if __name__ == "__main__":
    ai = Program()
    ai.run()
                            