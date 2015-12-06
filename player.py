from person import Person
import pygame

class Player(Person):
    """The player of the game"""

    def __init__(self, board):
        """Constructor function to set up the first instance of the player in the game"""
        
        self.__pos = (28, 2)
        self.__lives = 3
        self.__score = 0        
        self.__onladder = False   
        self.__facing = "right"
        self.__sClass = super(Player, self)
        self.__lose = False
        self.__win = False
        self.__respawn = False
        self.__onlevel = 1
        board.setChar(self.__pos, "P") 
        self.__coinaffect = pygame.mixer.Sound("Videos/coin.wav")

    def collectCoin(self):
        """Collects coin"""     

        self.__coinaffect.play()
        self.__score += 5

    def getScore(self):
        """Returns player's score"""

        return self.__score

    def getLives(self):
        """Returns player's lives"""

        return self.__lives

    def getLevel(self):
        """Returns player's level"""

        return self.__onlevel

    def setSpawnFlag(self, flag):
        """sets player.__respawn flag"""

        self.__respawn = flag

    def getSpawnFlag(self):
        """Returns player.__respawn flag"""

        return self.__respawn

    def getFacing(self):
        """Returns player's facing direction"""

        return self.__facing

    def setWinFlag(self, flag):
        """Sets __win flag"""

        self.__win = flag

    def getWinFlag(self):
        """Returns __win flag"""

        return self.__win

    def getLoseFlag(self):
        """Returns __lose flag"""

        return self.__lose

    def CheckWin(self, board):
        """checks if player has won a level"""

        if self.__pos[0] == 1:
            self.__score += 50
            self.__win = True
            self.__onlevel += 1
            board.setChar(self.__pos, " ")
            self.UpdatePosition((28,2))
            board.setChar(self.__pos, "P")

    def ReSpawn(self, board):
        """respawns the player"""

        if self.__onladder == True:
            board.setChar(self.__pos, "H")
            self.__onladder = False      
        else:
            board.setChar(self.__pos, " ")
        self.UpdatePosition((28, 2))
        board.setChar(self.__pos, "P")
        self.__respawn = True

    def UpdatePosition(self, new):
        """update position of the person to new"""    
        
        self.__pos = new 
        
    def getPosition(self):
        """Returns current position of person"""
        
        return self.__pos

    def decreaseLife(self, board):
        """decrease life"""

        self.__lives -= 1
        self.__score -= 25
        if self.__lives == 0:
            self.__lose = True
        else:
            self.ReSpawn(board)

    def CheckForFall(self, board):
        """Check for fall"""

        down = self.__sClass.getPosDown(self.__pos)
        down = board.getCharAt(down)
        if down == "O":
            self.decreaseLife(board)
        elif down == " ":
            self.fallDown(board)

    def MoveLeftHelper(self, board):
        """ move left helper function"""

        if self.__onladder == True:
            board.setChar(self.__pos, "H")
            self.__onladder = False
        else:
            board.setChar(self.__pos, " ")
        new = self.__sClass.getPosLeft(self.__pos)
        board.setChar(new, "P")
        self.UpdatePosition(new)

    def MoveLeft(self, board):
        """A move left function for the player"""
        
        self.__facing = "left"
        left = self.__sClass.getPosLeft(self.__pos)
        if board.getCharAt(left) != "X":
            left = board.getCharAt(left)
            if left == "O" or left == "D":
                self.decreaseLife(board)
            else:
                self.MoveLeftHelper(board)
            if left == "C":
                self.collectCoin()
            elif left == "H":
                self.__onladder = True
            self.CheckForFall(board)

    def MoveRightHelper(self, board):
        """a move right helper function for the player"""

        if self.__onladder == True:
            board.setChar(self.__pos, "H")
            self.__onladder = False
        else:
            board.setChar(self.__pos, " ")
        new = self.__sClass.getPosRight(self.__pos)
        board.setChar(new, "P")
        self.UpdatePosition(new)                                

    def MoveRight(self, board):
        """a move right function for the player"""

        self.__facing = "right"
        right = self.__sClass.getPosRight(self.__pos)
        if board.getCharAt(right) != "X":
            right = board.getCharAt(right)
            if right == "O" or right == "D":
                self.decreaseLife(board)
            else:
                self.MoveRightHelper(board)
            if right == "C":
                self.collectCoin()
            elif right == "H":
                self.__onladder = True
            self.CheckForFall(board)

    def MoveUpHelper(self, board):
        """move up helper function"""

        new = self.__sClass.getPosUp(self.__pos)
        board.setChar(self.__pos, "H")
        board.setChar(new, "P")
        self.UpdatePosition(new)                                

    def MoveUp(self, board):
        """a move up function for the player"""

        up = self.__sClass.getPosUp(self.__pos)
        up = board.getCharAt(up)
        down = self.__sClass.getPosDown(self.__pos)
        down = board.getCharAt(down)
        if self.__onladder == True and up == "H":
            self.MoveUpHelper(board)
        elif up == "O":
            self.decreaseLife(board)
        elif self.__onladder == True and (up == " " or up == "C") and down == "H":
            self.MoveUpHelper(board)
            self.__onladder = False
        self.CheckWin(board)
    
    def CheckLadderBreakDown(self, board, pos):
        """Checks if the ladder is broken"""

        down = self.__sClass.getPosDown(pos)
        down = self.__sClass.getPosDown(down)
        return board.getCharAt(down) == " "

    def MoveDownHelper(self, board):
        """move down helper function"""

        new = self.__sClass.getPosDown(self.__pos)
        if self.__onladder == True:
            board.setChar(self.__pos, "H")
            self.__onladder = False
        else:
            board.setChar(self.__pos, " ")
        board.setChar(new, "P")
        self.UpdatePosition(new)

    def MoveDown(self, board):
        """A move down function for the player"""

        down = self.__sClass.getPosDown(self.__pos)
        down_chr = board.getCharAt(down)    
        if down_chr != "X":
            if self.__onladder == True or not self.CheckLadderBreakDown(board, down):
                if down_chr == "H":
                    self.MoveDownHelper(board)
                    self.__onladder = True
            elif down_chr == "O":
                self.decreaseLife(board)
        
    def CheckCollision(self, board, pos):
        """checks collision with fireball during jump"""

        return board.getCharAt(pos) == "O"
    
    def getPosNorthEast(self):
        """gets position north east of current position"""

        return (self.__pos[0] - 1, self.__pos[1] + 1)            

    def getPosSouthEast(self):
        """gets position south east of current position"""

        return (self.__pos[0] + 1, self.__pos[1] + 1)

    def getPosNorthWest(self):
        """gets position north west of current position"""

        return (self.__pos[0] - 1, self.__pos[1] - 1)
    
    def getPosSouthWest(self):                
        """gets position soth west of current position"""

        return (self.__pos[0] + 1, self.__pos[1] - 1)
    
    def SubJumpHelper(self, pos, board):
        """Helper function for jump helper function"""

        ne_char = board.getCharAt(pos)
        if self.__onladder == True:
            board.setChar(self.__pos, "H")
            self.__onladder = False
        else:
            board.setChar(self.__pos, " ")
        if ne_char == "H":
            self.__onladder = True
        board.setChar(pos, "P") 
        self.UpdatePosition(pos)

    def JumpHelper(self, board, pos):
        """Jump helper function"""

        pos_char = board.getCharAt(pos) 
        if self.CheckCollision(board, pos):
            self.decreaseLife(board)
        else:         
            self.SubJumpHelper(pos, board)
    
    def JumpNorthEast(self, board):
        """A function for jump in north east direction"""
        
        ne = self.getPosNorthEast()
        ne_chr = board.getCharAt(ne)
        if ne_chr == "X":
            self.fallDown(board)
            return 
        elif ne_chr == "O":
            self.decreaseLife(board)
        self.JumpHelper(board, ne)

    def JumpSouthEast(self, board):
        """A function for jump in south east direction"""

        se = self.getPosSouthEast()
        se_chr = board.getCharAt(se)
        if se_chr == "X":
            self.fallDown(board)
            return
        if se_chr == "C":
            self.collectCoin()
        self.JumpHelper(board, se)

    def JumpNorthWest(self, board):
        """A function for jump in north west direction"""

        nw = self.getPosNorthWest()
        nw_chr = board.getCharAt(nw) 
        if nw_chr == "X":
            self.fallDown(board)
            return 
        elif nw_chr == "O":
            self.decreaseLife(board)
        self.JumpHelper(board, nw)

    def JumpSouthWest(self, board):
        """A function for jump in south west direction"""

        sw = self.getPosSouthWest()
        sw_chr = board.getCharAt(sw)
        if sw_chr == "X":
            self.fallDown(board)
            return
        if sw_chr == "C":
            self.collectCoin()
        self.JumpHelper(board, sw)     

    def fallDownHelper(self, board):
        """A fall down helper function"""

        board.setChar(self.__pos, " ")
        new = self.__sClass.getPosDown(self.__pos)
        board.setChar(new, "P")
        self.UpdatePosition(new)
        
    def fallDown(self, board):
        """Function for the player falling down the edges of the floors"""

        down = self.__sClass.getPosDown(self.__pos)
        down = board.getCharAt(down)
        while down != "X":            
            if down == "O":
                self.decreasLife(board)
            elif down == " ":
                self.fallDownHelper(board)
            elif down == "C":
                self.collectCoin()
                self.fallDownHelper(board)
            down = self.__sClass.getPosDown(self.__pos)
            down = board.getCharAt(down)   

