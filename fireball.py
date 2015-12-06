import random

class Fireball:

    def __init__(self, board, new, player):
        """Initializes a fireball object"""

        self.__pos = new
        self.__onladder = False
        if board.getCharAt(self.__pos) == "H":
            self.__onladder = True
        board.setChar(self.__pos, "O")
        self.__oncoin = False
        self.__direction = "right"
        self.__dead = False
        #self.__ondonkey = False

    def getPosDown(self):
        """Gets position down of fireball's position"""
        
        return (self.__pos[0] + 1, self.__pos[1])

    def getPosUp(self):
        """Gets position up of fireball's position"""

        return (self.__pos[0] - 1, self.__pos[1])

    def getPosLeft(self):
        """Gets position left of fireball's position"""

        return (self.__pos[0], self.__pos[1] - 1)

    def getDeadFlag(self):
        """Gets fireball.__dead flag"""

        return self.__dead

    def getPosRight(self):
        """Gets position right of fireball's position"""

        return (self.__pos[0], self.__pos[1] + 1)    

    def UpdatePosition(self, pos):
        """updates position of fireball"""

        self.__pos = pos

    def MoveHelperPrev(self, board):
        """A move helper function to update previous position"""

        if self.__onladder == True or board.getCharAt(self.getPosUp()) == "H":
            board.setChar(self.__pos, "H")
            self.__onladder = False
        elif self.__oncoin == True:
            board.setChar(self.__pos, "C")
            self.__oncoin = False
        #elif self.__ondonkey == True:
        #    board.setChar(self.__pos, "D")
        #    self.__ondonkey = False
        else:
            board.setChar(self.__pos, " ")

    def MoveHelperNew(self, pos, char, board, player):
        """A move helper function to update new position and set new flags"""

        if char == "P":
            player.decreaseLife(board)
        elif char == "H":
            self.__onladder = True
        elif char == "C":
            self.__oncoin = True
        #elif char == "D":
        #    self.__ondonkey = True
        board.setChar(pos, "O")
        self.UpdatePosition(pos)

    def MoveRight(self, board, player):
        """A move right function for the fireball"""
        
        self.__direction = "right"
        right_pos = self.getPosRight()
        right_chr = board.getCharAt(right_pos)
        self.MoveHelperPrev(board)
        self.MoveHelperNew(right_pos, right_chr, board, player)            

    def MoveLeft(self, board, player):
        """A moveleft function for the fireball"""

        self.__direction == "left"
        left_pos = self.getPosLeft()
        left_chr = board.getCharAt(left_pos)
        self.MoveHelperPrev(board)
        self.MoveHelperNew(left_pos, left_chr, board, player)

    def getLadderBreak(self, board):
        """To check if ladder is broken"""

        return board.getCharAt((self.__pos[0] + 3, self.__pos[1])) == " "

    def MoveDown(self, board, down):
        """A move down function for the fireball"""

        if self.__onladder == True:
            board.setChar(self.__pos, "H")
            self.__onladder = False
        else:
            board.setChar(self.__pos, " ")
        board.setChar(down, "O")
        self.UpdatePosition(down)

    def CheckForFall(self, board, player):
        """A function for fireball to fall down the edges or down the ladder"""

        down = self.getPosDown()
        down_chr = board.getCharAt(down)
        direction = ["left", "right"]

        if down_chr == " ":            
            while down_chr != "X":                
                self.MoveDown(board, down)
                down = self.getPosDown()
                down_chr = board.getCharAt(down)
                if down_chr == "P":
                    player.decreaseLife(board) 
                elif down_chr == "C":
                    self.__oncoin = True
            self.__direction = direction[random.randrange(len(direction))]
            
        elif down_chr == "H" and self.getLadderBreak(board) == False and random.randint(1,2) == 2:    
            while down_chr != "X":
                self.MoveDown(board, down)
                down = self.getPosDown()
                down_chr = board.getCharAt(down)
                if down_chr == "P":
                    player.decreaseLife(board)
                self.__onladder = True
            self.__direction = direction[random.randrange(len(direction))]
            
            
    def CheckForFinish(self, board):
        """To check if a fireballs needs to vanish"""

        if self.__pos == (28, 1):
            board.setChar(self.__pos, " ")
            self.__dead = True
            del self
    
    def Motion(self, board, player):
        """To check left and right movements to fireball"""

        self.__direction == "right"
        pos_r = self.getPosRight()
        r_chr = board.getCharAt(pos_r)
        pos_l = self.getPosLeft()
        l_chr = board.getCharAt(pos_l)
        if r_chr == "X":
            self.__direction = "left"
        if l_chr == "X":
            self.__direction = "right"
        if self.__direction == "left":
            self.MoveLeft(board, player)
        else:
            self.MoveRight(board, player)
        self.CheckForFall(board, player)
        self.CheckForFinish(board)
