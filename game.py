import time, pygame, sys
from constants import *
from board import Board
from player import Player
from donkey import Donkey
from fireball import Fireball
from pygame.locals import *

class Game:
    """Main Game Class. Handles all the functionalities of the game"""

    def __init__(self):
        """Calls the function for Starting the game"""

        self.PyGameBasicSetup()
        self.LoadMainImages()
        self.IntroVideo()
        self.CreateHelperVariables()
        self.MenuOptions()

    def PyGameBasicSetup(self):
        """Basic Screen, clock, caption set up"""

        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption('Donkey Kong')
        self.__affect = pygame.mixer.Sound("Videos/output.ogg")
        self.__affect.play(-1)
        self.__fire_affect = pygame.mixer.Sound("Videos/fire.wav")
        self.__loselife_affect = pygame.mixer.Sound("Videos/loselife.wav")
        self.__jump_affect = pygame.mixer.Sound("Videos/jump.wav")
        self.__levelup_affect = pygame.mixer.Sound("Videos/levelup.wav")
        self.__gameover_affect = pygame.mixer.Sound("Videos/gameover.wav")
        self.__clock = pygame.time.Clock()
        self.__screen = pygame.display.set_mode((1280, 715))

    def GetFont(self, size, font="comicsansms"):
        """Returns font object given the font and size"""

        return pygame.font.SysFont(font, size)

    def WriteText(self, font, string, xcoord, ycoord, color=PINK):
        """Blits the text"""

        text = font.render(string, True, color)
        self.__screen.blit(text, (xcoord, ycoord))

    def LoadImagesHelper(self, name, width, height):
        """Returns image object given file name and dimensions"""

        return pygame.transform.scale(pygame.image.load(name), (width, height))

    def LoadMainImages(self):
        """Loads all the images for use in the game"""

        self.__coin = self.LoadImagesHelper("Pictures/coin.jpg", WIDTH, HEIGHT)
        self.__brick = self.LoadImagesHelper("Pictures/brick.jpeg", WIDTH, HEIGHT)
        self.__ladder = self.LoadImagesHelper("Pictures/ladder.jpeg", WIDTH, HEIGHT)
        self.__fireball_image = self.LoadImagesHelper("Pictures/fireball.jpeg", WIDTH, HEIGHT)
        self.__donkey_image = self.LoadImagesHelper("Pictures/donkey.jpg", WIDTH, HEIGHT)
        self.__player_image = self.LoadImagesHelper("Pictures/player.jpg", WIDTH, HEIGHT)
        self.__princess = self.LoadImagesHelper("Pictures/princess.png", WIDTH, HEIGHT)
        self.__heart = self.LoadImagesHelper("Pictures/heart.jpeg", INTACT_WIDTH, INTACT_HEIGHT)
        self.__broken = self.LoadImagesHelper("Pictures/broken.jpeg", LOST_WIDTH, LOST_HEIGHT)
        self.__banner = self.LoadImagesHelper("Pictures/banner.jpg", 1280, 715)
        self.__menu = self.LoadImagesHelper("Pictures/menu.jpeg", 565, 715)

    def IntroVideo(self):
        """Displays an Introductory Video"""

        i = 433 
        while i <= 697:
            video = self.LoadImagesHelper("Pictures/start/Pictures" + str(i) + ".jpg", 1280, 715)
            i += 1
            self.__screen.blit(video, (0,0))
            self.__clock.tick(30)
            pygame.display.flip()
        self.__screen.fill(BLACK)

    def CreateHelperVariables(self):
        """Creates and initializes helper variables, flags, containers, counters etc"""
        
        self.__fireballs = []
        self.__pressed_a = False
        self.__pressed_d = False
        self.__pause = False
        self.__cnt_fireballs = 150
        self.__mov_fireballs = 0
        self.__display = False
        self.__mov_donkey = 4
        self.__how_to = False
        self.__high_scores = False
        self.__play_game = False

    def HowTo(self):
        """Displays the How to play menu screen, controls and settings"""
        
        self.__screen.fill(BLACK)
        font = self.GetFont(F_SIZE)
        self.WriteText(font, "Here's how you play it!", X_DIST, HEADER_DEPTH)
        self.WriteText(font, "a -> Move Left", X_DIST, INIT_DEPTH)
        self.WriteText(font, "d -> Move Right", X_DIST, INIT_DEPTH + 50)
        self.WriteText(font, "w -> Move Up", X_DIST, INIT_DEPTH + 100)
        self.WriteText(font, "s -> Move Down", X_DIST, INIT_DEPTH + 150)
        self.WriteText(font, "Space -> Jump", X_DIST, INIT_DEPTH + 200)
        self.WriteText(font, "p -> Pause", X_DIST, INIT_DEPTH + 250)
        self.WriteText(font, "q -> Quit", X_DIST, INIT_DEPTH + 300)
        self.WriteText(font, "b -> Back", X_DIST, INIT_DEPTH + 350)
        pygame.display.flip()

    def HighScore(self):
        """Displays the top five high scores ever made in the game"""
        
        self.__screen.fill(BLACK)
        font = self.GetFont(F_SIZE)
        self.WriteText(font, "Here are the High Scores!", X_DIST, HEADER_DEPTH)
        f = open("highscores.txt","r")
        i = 200
        j = 0
        for line in f.readlines():
            j += 1
            self.WriteText(font, line.strip(), X_DIST, i)
            i += 50
            if j == 5:
                break
        self.WriteText(font, "b -> Back", X_DIST, INIT_DEPTH + 350)
        pygame.display.flip()
        f.close()
        
    def MenuOptions(self):
        """Displays all the Menu Options"""
        
        font = self.GetFont(80)
        while True:
            self.__screen.blit(self.__banner, (0,0))
            if self.__how_to == False and self.__high_scores == False:
                self.__screen.blit(self.__menu, (0,0))          
                self.WriteText(font, "Donkey Kong", 35, 150, color=PURPLE)
                self.WriteText(font, "1->Play Game", 1, 280, color=PURPLE)
                self.WriteText(font, "2->How To Play", 1, 360, color=PURPLE)
                self.WriteText(font, "3->High Scores", 1, 440, color=PURPLE)
                self.__clock.tick(30)
                pygame.display.flip()
            for event in pygame.event.get():
                if event.type == KEYUP:
                    if event.key == K_1:
                        self.__play_game = True
                    elif event.key == K_2:
                        self.HowTo()
                        self.__how_to = True
                    elif event.key == K_3:
                        self.HighScore()
                        self.__high_scores = True
                    elif event.key == K_b and (self.__how_to == True or self.__high_scores == True):
                        self.__screen.fill(BLACK)
                        self.__how_to = False
                        self.__high_scores = False
                    elif event.key == K_q:
                        self.Quit()
                elif event.type == QUIT:
                    self.Quit()
            if self.__play_game == True:
                break
        if self.__play_game == True:
            self.CreateObjectsForPlay()
            self.PlayGame()

    def CreateObjectsForPlay(self):
        """Creates instances of various objects in the game"""
        
        self.__board = Board()
        self.__player = Player(self.__board)
        self.__donkeys = []
        self.__donkeys.append(Donkey(self.__board, self.__player, (4,2)))

    def DisplayBoard(self):
        """Displays the current state of the game"""

        for i in range(30):
            for j in range(80):
                pygame.draw.rect(self.__screen, BLACK, [ WIDTH*j, HEIGHT*i, WIDTH, HEIGHT])

                char = self.__board.getCharAt((i,j))

                if char == "Q":
                    self.__screen.blit(self.__princess, (WIDTH*j + WIDTH/100, HEIGHT*i + HEIGHT/100))
                elif char == "H":
                    self.__screen.blit(self.__ladder, (WIDTH*j + WIDTH/100, HEIGHT*i + HEIGHT/100))
                elif char == "C":
                    self.__screen.blit(self.__coin, (WIDTH*j + WIDTH/100, HEIGHT*i + HEIGHT/100))
                elif char == "X":
                    self.__screen.blit(self.__brick, (WIDTH*j + WIDTH/100, HEIGHT*i + HEIGHT/100))
                elif char == "O":
                    self.__screen.blit(self.__fireball_image, (WIDTH*j + WIDTH/100, HEIGHT*i + HEIGHT/100))
                elif char == "D":
                    self.__screen.blit(self.__donkey_image, (WIDTH*j + WIDTH/100, HEIGHT*i + HEIGHT/100))
                elif char == "P":
                    self.__screen.blit(self.__player_image, (WIDTH*j + WIDTH/100, HEIGHT*i + HEIGHT/100))

    def Quit(self):
        """Action when user clicks on cross on top left of the window"""

        pygame.quit()
        sys.exit()

    def FireballMotion(self):
        """Controls the occurrence and speed of fireballs"""

        if self.__cnt_fireballs == 150:
            for donkey in self.__donkeys:
                pos = donkey.getPosRight()
                if self.__board.getCharAt(pos) != "H":
                    self.__fireballs.append(Fireball(self.__board, pos, self.__player))
                    self.__fire_affect.play()
            self.__cnt_fireballs = 0
        else:   
            self.__cnt_fireballs += 1

        if self.__mov_fireballs == 1 or self.__cnt_fireballs == 0:
            for ball in self.__fireballs:
                if ball.getDeadFlag() == False:
                    ball.Motion(self.__board, self.__player)
                else:
                    self.__fireballs.remove(ball)
            self.__mov_fireballs = 0
        else:
            self.__mov_fireballs += 1

    def DonkeyMotion(self):
        """Controls the motion and speed of donkey"""
        
        if self.__mov_donkey == 5:
            for donky in self.__donkeys:
                donky.Motion(self.__board, self.__player)
                pygame.display.flip()
            self.__mov_donkey = 0
        else:
            self.__mov_donkey += 1

    def SideBar(self):
        """Displays the side bar containing score, lives and level"""
        
        font = self.GetFont(30)
        self.WriteText(font, "SCORE: " + str(self.__player.getScore()), 1050, 30)
        self.WriteText(font, "LIVES: " + str(self.__player.getLives()), 1060, 65)
        self.WriteText(font, "LEVEL: " + str(self.__player.getLevel()), 1060, 100)

    def GameOver(self):
        """Displays the game over screen"""
        
        i = 36
        self.__gameover_affect.play()
        while i <= 240:
            img = self.LoadImagesHelper("Pictures/over/Pictures" + str(i) + ".jpg", 1280, 715)
            i += 1
            self.__screen.blit(img, (0,0))
            self.__clock.tick(30)
            pygame.display.flip()
        self.__screen.fill(BLACK)

    def NewHighScore(self, new):
        """Displays the score after game is over"""
        
        f = open("highscores.txt", "r+")
        i = 0
        while i < 5:
            line = f.readline()
            if int(line.strip()) < new:
                f.seek(f.tell()-len(line))
                f.write(str(new)+"\n"+line)
                break
            i += 1
        f.read()
        f.write(str(new) + "\n")
        f.close()
        self.__screen.fill(BLACK)
        font = self.GetFont(50)
        self.WriteText(font, "Congratulations! You made a new high score!", 200, 300)
        self.WriteText(font, str(new), 500, 400)
        pygame.display.flip()
        time.sleep(4)
        self.__screen.fill(BLACK)  

    def LoseLife(self):
        """Displays the lives intact and lost every time the player loses a life"""
        
        self.__screen.fill(BLACK)
        hearts = self.__player.getLives()
        if hearts == 2:
            self.__screen.blit(self.__heart, (100, 200))
            self.__screen.blit(self.__heart, (400, 200))
            self.__screen.blit(self.__broken, (800, 200))
        elif hearts == 1:
            self.__screen.blit(self.__heart, (100, 200))
            self.__screen.blit(self.__broken, (400, 200))
            self.__screen.blit(self.__broken, (800, 200))
        self.__loselife_affect.play()
        pygame.display.flip()
        time.sleep(3)
        self.__pause = False
        self.__board.setChar(self.__player.getPosition(), "P")

    def ReSpawnPlayer(self):
        """For Respawning the player when he loses a life"""

        self.__player.setSpawnFlag(False)
        self.LoseLife()

    def ReInitializeForLevelUp(self):
        """To Reinitialise variables, objects etc for Level up and increase the number of donkeys"""

        self.CreateHelperVariables()
        self.__board.Initialize()
        self.__donkeys.append(Donkey(self.__board, self.__player, (4, 30)))        
        self.__player.UpdatePosition((28, 2))
        self.__board.setChar((28, 2), "P")
        pygame.display.flip()

    def LevelUp(self):
        """Displays the level Up screen"""
        
        self.__levelup_affect.play()
        self.__screen.fill(BLACK)    
        font = self.GetFont(50)
        self.WriteText(font, "Congratulations! You passed the level!", 200, 300)
        pygame.display.update()
        time.sleep(3) 
        self.__screen.fill(BLACK)
        self.ReInitializeForLevelUp()
        
    def HandleJumpUpdate(self):
        """To Update parts of a jump"""

        self.DisplayBoard()
        pygame.display.flip()

    def HandleJump(self):
        """To display player's jump"""

        self.__jump_affect.play()
        if self.__player.getFacing() == "right":
            self.__player.JumpNorthEast(self.__board)
            self.HandleJumpUpdate()
            self.__player.JumpNorthEast(self.__board)
            self.HandleJumpUpdate()
            self.__player.JumpSouthEast(self.__board)
            self.HandleJumpUpdate()
            self.__player.JumpSouthEast(self.__board)
            self.__player.CheckForFall(self.__board)
        else:
            self.__player.JumpNorthWest(self.__board)
            self.HandleJumpUpdate()
            self.__player.JumpNorthWest(self.__board)
            self.HandleJumpUpdate()
            self.__player.JumpSouthWest(self.__board)
            self.HandleJumpUpdate()
            self.__player.JumpSouthWest(self.__board)
            self.__player.CheckForFall(self.__board)

    def ManageEvents(self):
        """Manages all the keyboard presses, ups and downs, for movement of the player, quitting etc"""

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_q):
                self.Quit()
            if self.__pause == False:
                if event.type == KEYDOWN:
                    if event.key == K_a:
                        self.__pressed_a = True
                    elif event.key == K_d:
                        self.__pressed_d = True    
                    elif event.key == K_w:
                        self.__player.MoveUp(self.__board)
                    elif event.key == K_s:
                        self.__player.MoveDown(self.__board)
                elif event.type == KEYUP:
                    if event.key == K_a:
                        self.__pressed_a = False
                    elif event.key == K_d:
                        self.__pressed_d = False
                    elif event.key == K_SPACE:
                        self.HandleJump()
            if event.type == KEYUP and event.key == K_p:
                if self.__pause == False:
                    self.__pause = True
                elif self.__player.getSpawnFlag() != True:
                    self.__pause = False

    def HandlePlayerMovement(self):
        """To display left and right movement of player"""

        if self.__pressed_a == True:
            self.__player.MoveLeft(self.__board)
        elif self.__pressed_d == True:
            self.__player.MoveRight(self.__board)

    def PlayGame(self):
        """Main Game Loop"""
        
        while True:
            if self.__pause == False:
                self.FireballMotion()
                self.DonkeyMotion()
                self.HandlePlayerMovement()
                self.__clock.tick(20)
                self.DisplayBoard()
                self.SideBar()
                if self.__player.getLoseFlag() == True:                    
                    self.GameOver()                    
                    self.NewHighScore(self.__player.getScore())
                    self.CreateHelperVariables()
                    self.MenuOptions()
                    break
                elif self.__player.getWinFlag() == True:
                    self.__player.setWinFlag(False)
                    self.LevelUp()
                elif self.__player.getSpawnFlag() == True:
                    self.__pause = True
                    self.ReSpawnPlayer()

            self.ManageEvents()
            pygame.display.flip()
