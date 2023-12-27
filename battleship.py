"""
Author: Jorly Metzger
Date: 11/18/2023

Description:
    Simmulates the Battleship game using the following ship and sizes:
        Mothership: 5 (x shape)
        Battleship: 4 (square shape)
        Destroyer: 3 (E shape)
        Stealth Ship: 3 (line)
        Patrol Ship: 2 (line)

    Game will maintain a list of top 10 highest accuracy players and
    display in a hall-of-fame (HOF).

    User will have the option to (1) view instructions, (2) view an
    example layout of ships in a grid to inspect their shaps, (3) play
    the game, (4) view the HOF, and (5) exit the game
"""

""" Imported Modules """
import random

""" Constants """
TOTAL_HITS = 17
M_MAX = 5
B_MAX = 4
D_MAX = 3
S_MAX = 3
P_MAX = 2
MAX_ROW = 10
MAX_COL = 12

""" Classes and Functions """
class Game:
    def __init__(self):
        self.game_grid = initiate_grid()    
        self.ships = make_grid()            
        self.hof = readHOF()                
        self.attempts = 0                   
        self.m_hits = 0                     
        self.b_hits = 0                     
        self.d_hits = 0                     
        self.s_hits = 0                     
        self.p_hits = 0                     
        
    def mapCol(self,col):
        col = col.upper()

        if (col == "A"): return 0
        elif (col == "B"): return 1
        elif (col == "C"): return 2
        elif (col == "D"): return 3
        elif (col == "E"): return 4
        elif (col == "F"): return 5
        elif (col == "G"): return 6
        elif (col == "H"): return 7
        elif (col == "I"): return 8
        elif (col == "J"): return 9
        elif (col == "K"): return 10
        elif (col == "L"): return 11
        else: return -1

    def shot(self, shot):
        row = int(shot[0])
        col = self.mapCol(shot[1])
        self.attempts += 1

        if self.game_grid[row][col] != "~":
            print ("You've already targeted that location")
        else:
            result = self.ships[row][col]
            if (result == "~"):
                print ("")                                      # align formatting
                print ("miss")
                self.game_grid[row][col] = "o"
            else:
                print ("")                                      # align formatting
                print ("IT'S A HIT!")
                self.game_grid[row][col] = "x"

                if (result == "M"):                             
                    self.m_hits += 1
                    if (self.m_hits >= M_MAX):
                        print ("The enemy's Mothership has been destroyed.")
                elif (result == "B"):                           
                    self.b_hits += 1
                    if (self.b_hits >= B_MAX):
                        print ("The enemy's Battleship has been destroyed.")
                elif (result == "D"):                           
                    self.d_hits += 1
                    if (self.d_hits >= D_MAX):
                        print ("The enemy's Destroyer has been destroyed.")
                elif (result == "S"):                           
                    self.s_hits += 1
                    if (self.s_hits >= S_MAX):
                        print ("The enemy's Stealth Ship has been destroyed.")
                elif (result == "P"):                           
                    self.p_hits += 1
                    if (self.p_hits >= P_MAX):
                        print ("The enemy's Patrol Ship has been destroyed.")

        if (self.m_hits >= M_MAX and                   
            self.b_hits >= B_MAX and                   
            self.d_hits >= D_MAX and                    
            self.s_hits >= S_MAX and                    
            self.p_hits >= P_MAX):                      
            return True                                 
        else:
            return False                                
    
    ####
    # Returns True if added to HOF and False if not added to HOF
    # ##
    def hofEntry(self):
        if (self.attempts < TOTAL_HITS):
            return                                      # invalid; there should be at least equal attempts to hits needed

        misses = self.attempts - TOTAL_HITS             # misses are total attempts minus the hits
        highScore = False

        if (len(self.hof) >= 10):
            bottom = self.hof[-1]
            if (bottom[0] > misses):                    
                highScore = True                        
                del self.hof[-1]                        # delete the lowest HOF entry
        else:                                           # if there are less than 10 entries, then automatically HOFer
            highScore = True

        if (highScore == True):
            print ("Congratulations, you have achieved a targeting accuracy of")
            print (f"{(TOTAL_HITS/self.attempts)*100:.2f}% and earned a spot in the Hall of Fame.")
            name = input("Enter your name: ")           

            entry = [misses, name]                      
            self.hof = addHOFEntry(self.hof, entry)     
            writeHOFtoFile(self.hof)                    
            printHOF(self.hof)                          
            return True                
        return False


def menu():
    print ("Menu:")
    print ("  1 : Instructions")
    print ("  2 : View Example Map")
    print ("  3 : New Game")
    print ("  4 : Hall of Fame")
    print ("  5 : Quit")

def instructions():
    str = "Instructions\n\n"
    str += "Ships are positioned at fixed locatoins in a 10-by-12 grid.  "
    str += "The rows of the gird are labeled 0 through 9, and the colums are labeled A through L.  "
    str += "Use menu option \"2\" to see an example.  "
    str += "Target the ships by entering the row and column of the location you wish to shoot.  "
    str += "A ship is destryoed when all of the spaces it fills have been hit.  "
    str += "Try to destroy the fleet with as few shots as possible.  "
    str += "The fleet consists of the following 5 ships:\n\n"

    str += "Size : Type\n"
    str += "   5 : Mothership\n"
    str += "   4 : Battleship\n"
    str += "   3 : Destroyer\n"
    str += "   3 : Stealth Ship\n"
    str += "   2 : Patrol Ship\n"
    print(str)
    return

def print_grid(grid):
    print ("")
    print ("   A  B  C  D  E  F  G  H  I  J  K  L")
    rows, cols = 10, 12
    cnt = 0

    for r in range(rows):
            column = f"{cnt}  "
            cnt += 1

            for c in range(cols):
                column += grid[r][c]
                if (c < cols-1):
                    column += "  "
            print (column)

    print("")

def mothership(grid):
    searching = True
    
    while (searching == True):
        col = random.randint(0, MAX_COL-1)
        row = random.randint(0,MAX_ROW-1)
        coordinates = []

        if (col + 2 < MAX_COL) and (row + 2 < MAX_ROW):
            if grid[row][col] == "~":
                coordinate = [row, col]
                coordinates.append(coordinate)                      # top left coordinate of ship
                col += 2
                if grid[row][col] == "~":
                    coordinate = [row, col]
                    coordinates.append(coordinate)                  # top right coordinate of ship
                    row += 1
                    col -= 1
                    if grid[row][col] == "~":               
                        coordinate = [row, col]
                        coordinates.append(coordinate)              # middle coordinate of ship
                        row += 1
                        col -= 1
                        if grid[row][col] == "~":               
                            coordinate = [row, col]
                            coordinates.append(coordinate)          # bottom left coordinate of ship
                            col += 2
                            if grid[row][col] == "~":               
                                coordinate = [row, col]
                                coordinates.append(coordinate)      # bottom right coordinate of ship
                                searching = False
    #end while

    for iter in coordinates:                                        # upon succes, mark the grid
        grid[iter[0]][iter[1]] = "M"

    return grid

def battleship(grid):
    searching = True
    
    while (searching == True):
        col = random.randint(0, MAX_COL-1)
        row = random.randint(0,MAX_ROW-1)
        coordinates = []

        if (col + 1 < MAX_COL) and (row + 1 < MAX_ROW):             # ensure entire ship will fit in grid
            if grid[row][col] == "~":
                coordinate = [row, col]
                coordinates.append(coordinate)                      # top left coordinate of ship
                col += 1
                if grid[row][col] == "~":
                    coordinate = [row, col]
                    coordinates.append(coordinate)                  # top right coordinate of ship
                    row += 1
                    if grid[row][col] == "~":               
                        coordinate = [row, col]
                        coordinates.append(coordinate)              # bottom right coordinate of ship
                        col -= 1
                        if grid[row][col] == "~":               
                            coordinate = [row, col]
                            coordinates.append(coordinate)          # bottom left coordinate of ship
                            searching = False
    #end while

    for iter in coordinates:                                        # upon succes, mark the grid
        grid[iter[0]][iter[1]] = "B"

    return grid

def destroyer_right(grid):
    col = random.randint(0, MAX_COL-1)
    row = random.randint(0,MAX_ROW-1)
    coordinates = []
    search = True

    if (col + 1 < MAX_COL) and (row + 2 < MAX_ROW):             # ensure entire ship will fit in grid
        if grid[row][col] == "~":
            coordinate = [row, col]
            coordinates.append(coordinate)                      # top left coordinate of ship
            row += 1
            col += 1
            if grid[row][col] == "~":
                coordinate = [row, col]
                coordinates.append(coordinate)                  # middle coordinate of ship
                row += 1
                col -= 1
                if grid[row][col] == "~":               
                    coordinate = [row, col]
                    coordinates.append(coordinate)              # bottom left coordinate of ship
                    search = False                              # destroyer complete; stop search
    
    return coordinates, search

def destroyer_down(grid):
    col = random.randint(0, MAX_COL-1)
    row = random.randint(0,MAX_ROW-1)
    coordinates = []
    search = True

    if (col + 2 < MAX_COL) and (row + 1 < MAX_ROW):             # ensure entire ship will fit in grid
        if grid[row][col] == "~":
            coordinate = [row, col]
            coordinates.append(coordinate)                      # top left coordinate of ship
            col += 2
            if grid[row][col] == "~":
                coordinate = [row, col]
                coordinates.append(coordinate)                  # top right coordinate of ship
                row += 1
                col -= 1
                if grid[row][col] == "~":               
                    coordinate = [row, col]
                    coordinates.append(coordinate)              # middle coordinate of ship
                    search = False                              # destroyer complete; stop search
    
    return coordinates, search

def destroyer_left(grid):
    col = random.randint(0, MAX_COL-1)
    row = random.randint(0,MAX_ROW-1)
    coordinates = []
    search = True

    if (col - 1 >= 0) and (row + 2 < MAX_ROW):                  # ensure entire ship will fit in grid
        if grid[row][col] == "~":
            coordinate = [row, col]
            coordinates.append(coordinate)                      # top right coordinate of ship
            row += 1
            col -= 1
            if grid[row][col] == "~":
                coordinate = [row, col]
                coordinates.append(coordinate)                  # middle coordinate of ship
                row += 1
                col += 1
                if grid[row][col] == "~":               
                    coordinate = [row, col]
                    coordinates.append(coordinate)              # bottom right coordinate of ship
                    search = False                              # destroyer complete; stop search
    
    return coordinates, search

def destroyer_up(grid):
    col = random.randint(0, MAX_COL-1)
    row = random.randint(0,MAX_ROW-1)
    coordinates = []
    search = True

    if (col + 2 < MAX_COL) and (row - 1 >= 0):                  # ensure entire ship will fit in grid
        if grid[row][col] == "~":
            coordinate = [row, col]
            coordinates.append(coordinate)                      # bottom left coordinate of ship
            row -= 1
            col += 1
            if grid[row][col] == "~":
                coordinate = [row, col]
                coordinates.append(coordinate)                  # middle coordinate of ship
                row += 1
                col += 1
                if grid[row][col] == "~":               
                    coordinate = [row, col]
                    coordinates.append(coordinate)              # bottom right coordinate of ship
                    search = False                              # destroyer complete; stop search
    
    return coordinates, search

def destroyer(grid):
    coordinates = []
    searching = True
    
    while (searching == True):
        orientation = random.randint(0,3)

        if (orientation == 0):
            coordinates, searching = destroyer_right(grid)
        elif (orientation == 1):
            coordinates, searching = destroyer_down(grid)
        elif (orientation == 2):
            coordinates, searching = destroyer_left(grid)
        else:
            coordinates, searching = destroyer_up(grid)

    for iter in coordinates:                                    # upon succes, mark the grid
        grid[iter[0]][iter[1]] = "D"

    return grid

def stealth_horiz(grid):
    col = random.randint(0, MAX_COL-1)
    row = random.randint(0,MAX_ROW-1)
    coordinates = []
    search = True

    if (col + 2 < MAX_COL):                                     # ensure entire ship will fit in grid
        if grid[row][col] == "~":
            coordinate = [row, col]
            coordinates.append(coordinate)                      # left coordinate of ship
            col += 1
            if grid[row][col] == "~":
                coordinate = [row, col]
                coordinates.append(coordinate)                  # middle coordinate of ship
                col += 1
                if grid[row][col] == "~":               
                    coordinate = [row, col]
                    coordinates.append(coordinate)              # right coordinate of ship
                    search = False                              # stealth complete; stop search
    
    return coordinates, search

def stealth_vert(grid):
    col = random.randint(0, MAX_COL-1)
    row = random.randint(0,MAX_ROW-1)
    coordinates = []
    search = True

    if (row + 2 < MAX_ROW):                                     # ensure entire ship will fit in grid
        if grid[row][col] == "~":
            coordinate = [row, col]
            coordinates.append(coordinate)                      # top coordinate of ship
            row += 1
            if grid[row][col] == "~":
                coordinate = [row, col]
                coordinates.append(coordinate)                  # middle coordinate of ship
                row += 1
                if grid[row][col] == "~":               
                    coordinate = [row, col]
                    coordinates.append(coordinate)              # bottom coordinate of ship
                    search = False                              # stealth complete; stop search
    
    return coordinates, search

def stealth(grid):
    coordinates = []
    searching = True
    
    while (searching == True):
        orientation = random.randint(0,1)

        if (orientation == 0):
            coordinates, searching = stealth_horiz(grid)
        else:
            coordinates, searching = stealth_vert(grid)

    for iter in coordinates:                                    # upon succes, mark the grid
        grid[iter[0]][iter[1]] = "S"

    return grid

def patrol_horiz(grid):
    col = random.randint(0, MAX_COL-1)
    row = random.randint(0,MAX_ROW-1)
    coordinates = []
    search = True

    if (col + 1 < MAX_COL):                                     # ensure entire ship will fit in grid
        if grid[row][col] == "~":
            coordinate = [row, col]
            coordinates.append(coordinate)                      # left coordinate of ship
            col += 1
            if grid[row][col] == "~":
                coordinate = [row, col]
                coordinates.append(coordinate)                  # right coordinate of ship
                search = False                                  # patrol complete; stop search
    
    return coordinates, search

def patrol_vert(grid):
    col = random.randint(0, MAX_COL-1)
    row = random.randint(0,MAX_ROW-1)
    coordinates = []
    search = True

    if (row + 1 < MAX_ROW):                                     # ensure entire ship will fit in grid
        if grid[row][col] == "~":
            coordinate = [row, col]
            coordinates.append(coordinate)                      # top coordinate of ship
            row += 1
            if grid[row][col] == "~":
                coordinate = [row, col]
                coordinates.append(coordinate)                  # bottom coordinate of ship
                search = False                                  # patrol complete; stop search
    
    return coordinates, search

def patrol(grid):
    coordinates = []
    searching = True
    
    while (searching == True):
        orientation = random.randint(0,1)

        if (orientation == 0):
            coordinates, searching = patrol_horiz(grid)
        else:
            coordinates, searching = patrol_vert(grid)

    for iter in coordinates:                                    # upon succes, mark the grid
        grid[iter[0]][iter[1]] = "P"

    return grid

def initiate_grid():
    return [["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"]]

def make_grid():
    grid = initiate_grid()

    mothership(grid)
    battleship(grid)
    destroyer(grid)
    stealth(grid)
    patrol(grid)

    return grid

def playGame():
    game = Game()

    while (True):
        print_grid (game.game_grid)

        valid = False
        while (valid == False):
            shot = input("Where should we target next (q to quit)? ")

            if shot.upper() == "Q":                                             
                print("")                                                       # align formatting
                return                                                          # EXIT GAME

            if (len(shot) != 2):                                                # process only 2 character inputs
                print ("Please enter exactly two characters.\n")
            elif (shot.isalnum == False):                                       # process only alphanumeric strings
                print ("Please enter a location in the form \"6G\".\n")
            else:
                if (shot[0].isnumeric() == False) or (game.mapCol(shot[1]) == -1):  # needs to be in format [0-9][A-L]
                    print ("Please enter a location in the form \"6G\".\n")
                else:
                    valid = True
        #end while input is invalid

        if (game.shot(shot)  == True):                                      # Play Game
            print ("")                                                      # align formatting
            print ("You've destroyed the enemy fleet!")
            print ("Humanity has been saved from the threat of AI.\n")
            print ("For now ...\n")

            if (game.hofEntry() == False):                                  # check hall of fame (HOF)
                print (f"Your targeting accuracy was {(TOTAL_HITS / game.attempts)*100:.2f}%.")
                print ("")                                                  # align formatting
            return                                                          # GAME COMPLETE
    #end of while loop
    return

# Assumes list is ranked.
def writeHOFtoFile(hof):
    document = open ("battleship_hof.txt", "w")                 
    document.write("misses,name\n")                             
    for iter in hof:                                            
        document.write(f"{iter[0]},{iter[1]}\n")                

    return

# Assumes the list is ordered by rank
def readHOF():
    document = open ("battleship_hof.txt", "r")                 
    hof = []                                                    
    init = True

    for line in document:
        if init == True:
            init = False                                        
        else:
            line = line.strip()                                 
            line = line.split(',')                              
            entry = [int(line[0]), line[1]]                     

            hof.append(entry)
 
    document.close()
    return hof


# Assumes list is already ordered by rank.  Returns a HOF list order by rank.
def addHOFEntry(hof, entry):
    length = len(hof)
    if length == 0:                                             
        hof.append(entry)                                       
        return hof                                             

    if length == 10 and hof[length-1][0] <= entry[0]:           
        return hof                                              

    if length > 10:                                             
        return hof

    for index in range(length):                                 
        if (hof[length-index-1][0] <= entry[0]):                
            hof.insert(length-index, entry)                     
            return hof                                          

    return hof                                                  

# Assumes the HOF list received is already sorted
def printHOF(hof):
    print ("")
    print ("Hall of Fame:")
    print ("+------+-------------+----------+")
    print ("| Rank | Player Name | Accuracy |")
    print ("+------+-------------+----------+")

    rank = 1                                    
    for iter in hof:                           
        if (rank <= 10):                        
            name = iter[1]                      
            misses = iter[0]                    

            accuracy = TOTAL_HITS / (TOTAL_HITS + int(misses))   # accuracy is (hits / attempts), where attempts is the misses + the hits
            print ("|" + f"{rank:>4}" + "  |" + f"{name:^13}" + "|" + f"{accuracy*100:.2f}".rjust(8) + "% |")
            rank += 1

    print ("+------+-------------+----------+\n")
    return


def main():
    print ("")
    print ("~ Welcome to Battleship! ~".center(64))
    print ("")
    print ("ChatGPT has gone rogue and commandeered a space strike fleet.")
    print ("It's on a mission to take over the world.  We've located the")
    print ("stolen ships, but we need your superior intelligence to help")
    print ("destroy them before it's too late.")
    print ("")

    selection = 0
    while selection != "5":
        menu()
        selection = input("What would you like to do? ")

        if (selection == "1"):
            instructions()
        elif (selection == "2"):
            grid = make_grid()
            print_grid(grid)
        elif (selection == "3"):
            playGame()
        elif (selection == "4"):
            hof = readHOF()
            printHOF(hof)
        elif (selection == "5"):
            print ("\nGoodbye")
        else:
            print ("\nInvalid selection.  Please choose a number from the menu.\n")


"""Main - Do not change anything below this line."""
if __name__ == "__main__":
    main()
