import random
from person import Person

class Donkey(Person):

    def __init__(self, board, player, pos):
        """Initialises the donkey object"""

        self.__pos = pos 
        self.__oncoin = False
        self.__sClass = super(Donkey, self)
        self.__onladder = False
        self.__onfireball = False
        self.__ondonkey = False
        board.setChar(self.__pos, "D")

    def UpdatePosition(self, new):
        """update position of the person to new"""    
        
        self.__pos = new 
    
    def getPosRight(self):
        """Gets right position to initialize fireball"""

        return self.__sClass.getPosRight(self.__pos)

    def getPosition(self):
        """Returns current position of person"""
        
        return self.__pos        

    def MoveLeft(self, board, player):
        """A move left function for the Donkey"""

        left = self.__sClass.getPosLeft(self.__pos)
        left_chr = board.getCharAt(left)

        if left_chr != "X":

            if self.__ondonkey == True:
                board.setChar(self.__pos, "D")
                self.__ondonkey = False
            elif self.__onladder == True:
                board.setChar(self.__pos, "H")
                self.__onladder = False
            elif self.__oncoin == True:
                board.setChar(self.__pos, "C")
                self.__oncoin = False
            elif self.__onfireball == True:
                board.setChar(self.__pos, "O")
                self.__onfireball = False
            else:
                board.setChar(self.__pos, " ")
                
            if left_chr == "H":
                self.__onladder = True         
            elif left_chr == "O":
                self.__onfireball = True
            elif left_chr == "C":
                self.__oncoin = True    
            elif left_chr == "D":
                self.__ondonkey = True
            elif left_chr == "P":
                player.decreaseLife(board)
            board.setChar(left, "D")
            self.UpdatePosition(left)

    def MoveRight(self, board, player):
        """A move right function for the donkey"""

        right = self.__sClass.getPosRight(self.__pos)
        right_chr = board.getCharAt(right)
        right_down = self.__sClass.getPosDown(right)
        if board.getCharAt(right_down) != " ":
            if self.__ondonkey == True:
                board.setChar(self.__pos, "D")
                self.__ondonkey = False
            if self.__onladder == True:
                board.setChar(self.__pos, "H")
                self.__onladder = False
            elif self.__oncoin == True:
                board.setChar(self.__pos, "C")
                self.__oncoin = False
            elif self.__onfireball == True:
                board.setChar(self.__pos, "O")
                self.__onfireball = False
            else:
                board.setChar(self.__pos, " ")

            if right_chr == "H":
                self.__onladder = True
            elif right_chr == "O":
                self.__onfireball = True
            elif right_chr == "C":
                self.__oncoin = True
            elif right_chr == "D":
                self.__ondonkey = True
            elif right_chr == "P":
                player.decreaseLife(board)
            board.setChar(right, "D")
            self.UpdatePosition(right)

    def Motion(self, board, player):
        """To randomize the motion of the donkey"""
        
        if self.__pos[1] > 160/3:
            direction = ["left", "left", "right"]
        elif self.__pos[1]  < 80/12:
            direction = ["left", "right", "right"]
        else:
            direction = ["left", "right" ]
            
        direction = direction[random.randrange(len(direction))]
        
        if direction == "left":
            self.MoveLeft(board, player)
        else:
            self.MoveRight(board, player)
