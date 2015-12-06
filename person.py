class Person(object):    

    def __init__(self):
        pass
    
    def getPosDown(self, pos):
        """Gets position down of pos"""

        return (pos[0] + 1, pos[1])
    
    def getPosUp(self, pos):
        """Gets position up of pos"""

        return (pos[0] - 1, pos[1])
    
    def getPosLeft(self, pos):
        """Gets position left of pos"""

        return (pos[0], pos[1] - 1)
    
    def getPosRight(self, pos):
        """Gets position right of pos"""

        return (pos[0], pos[1] + 1)

