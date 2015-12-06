import random

class Board:
    """A class for the Board containing various function for the initial setup of the board"""

    def __init__(self):
        """Sets up the initial look of the board"""

        self.Initialize()

    def Initialize(self):
        self.__array = []
        for i in range(30):
            line = [' '] * 80
            self.__array.append(line)    
        self.BuildWalls()
        self.BuildFloors()
        self.PositionPrincess()
        self.GenerateCoins()
        self.BuildLadders()

    def BuildWalls(self):
        """Builds the walls or the boundaries for the playing area"""

        __walls = [ (0,0,80,1),
                (0,0,1,30),
                (0,29,80,1),
                (79,0,1,30),
                (24,1,1,1),
                (34,1,1,1),
                (24,2,11,1)
                ]

        for wall in __walls:
            for i in range(wall[1], wall[1] + wall[3]):
                for j in range(wall[0], wall[0] + wall[2]):
                    self.__array[i][j] = "X"

    def BuildFloors(self):
        """Builds the floors in the playing area"""

        __floors = [
                (0,5,50,1),
                (20,9,60,1),
                (0,13,60,1),
                (15,17,65,1),
                (0,21,65,1),
                (10,25,70,1)
                ]

        for floor in __floors:
            for i in range(floor[1], floor[1] + floor[3]):
                for j in range(floor[0], floor[0] + floor[2]):
                    self.__array[i][j] = "X"

    def PositionPrincess(self):
        """Sets the position of the princess"""
       
        self.__array[1][28] = "Q"

    def BuildLadders(self):
        """Builds the intact as well as broken ladders"""

        __ladders = [ (32,2,1,3),
                (47,5,1,4),
                (23,5,1,4),
                (34,9,1,4),
                (49,13,1,4),
                (39,17,1,4),
                (59,17,1,4),
                (63,21,1,4),
                (22,21,1,4),
                (22,21,1,4),
                (35,25,1,4)
                ]

        __ladder_breaks = [ (23,7,1,1),
                (59,19,1,1),
                (22,23,1,1)
                ]

        for ladder in __ladders:
            for i in range(ladder[1], ladder[1] + ladder[3]):
                for j in range(ladder[0], ladder[0] + ladder[2]):
                    self.__array[i][j] = "H"


        for ladder_break in __ladder_breaks:
            for i in range(ladder_break[1], ladder_break[1] + ladder_break[3]):
                for j in range(ladder_break[0], ladder_break[0] + ladder_break[2]):
                    self.__array[i][j] = " "

    def GenerateCoinsHelper(self, num, limit, floor_row):
        """A helper funtion for generating coins per floor"""

        for i in range(num):
            pos = random.randint(limit[0], limit[1])
            self.__array[floor_row][pos] = "C"

    def GenerateCoins(self):
        """Randomly generate coins on all floors"""

        NUM_FLOORS = 7
        NUM_COINS_LIMITS = (3, 5)

        __limits = [ (4, 49), 
                (21, 78),
                (4, 59),
                (16, 78),
                (4, 64),
                (11, 78),
                (4, 78)
                ]

        __floor_rows = [ 4, 8, 12, 16, 20, 24, 28 ]

        for i in range(NUM_FLOORS):
            num = random.randint(NUM_COINS_LIMITS[0], NUM_COINS_LIMITS[1])
            self.GenerateCoinsHelper(num, __limits[i], __floor_rows[i])

    def getCharAt(self, pos):
        """Gets character at pos"""

        return self.__array[pos[0]][pos[1]]

    def setChar(self, pos, char):
        """Sets char at pos"""

        self.__array[pos[0]][pos[1]] = char
