import pygame

#This file has classes for creating games start and end screens.

class Endscreen:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height

    def draw_screen(self, screen):
        #fill method isn't called, so game screen will be shown under ending texts.
        font = pygame.font.SysFont("Arial", 30)
        end_text = font.render("The king is dead!", True, (247,156,156))
        screen.blit(end_text, (self.__width / 2 - end_text.get_width() / 2, self.__height / 2 - end_text.get_height()))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

class Startscreen:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height

    #Recursive function that draws a line of circles from starting point to the end point.
    def __draw_circleline(self, screen, start_x, y, endpoint, radius):
        pygame.draw.circle(screen, (255, 255, 255), (start_x, y), radius)
        #If end point hasn't been reached, function draws a new circle to the next point.
        if start_x < endpoint:
            self.__draw_circleline(screen, start_x + radius * 2, y, endpoint, radius)

    #Draws game's starting view to the given screen.
    def draw_screen(self, screen):
        queen = pygame.image.load("assets/queen.png")
        king = pygame.image.load("assets/king.png")

        #Draw game's name.
        font = pygame.font.SysFont("Arial", 30)
        game_name = font.render("Defend the King", True, (255,255,255))

        #Draw game instructions.
        smaller_font = pygame.font.SysFont("Arial", 15)
        start_instruction = smaller_font.render("Press Space to start", True, (255,255,255))
        game_insturction = smaller_font.render("Move queen with mouse cursor. Defend the king by hitting enemies and collect coins.", True, (255,255,255))

        screen.fill((0, 0, 0))

        #Write game's name in the middle of the screen.
        screen.blit(game_name, (self.__width / 2 - game_name.get_width() / 2, self.__height / 2 - game_name.get_height() / 2))

        #Draw queen sprite on top of the name and king sprite under it.
        screen.blit(queen, (self.__width / 2 - queen.get_width() / 2, self.__height / 2 - game_name.get_height() - queen.get_height() - 5))
        screen.blit(king, (self.__width / 2 - king.get_width() / 2, self.__height / 2 + game_name.get_height() + 5))

        #Write start and game instructions to the screen.
        screen.blit(start_instruction, (self.__width / 2 - start_instruction.get_width() / 2, self.__height - 100))
        screen.blit(game_insturction, (self.__width / 2 - game_insturction.get_width() / 2, self.__height - 70))

        #Use recursive function to draw two decorative lines on screen.
        self.__draw_circleline(screen, 10, 15, self.__width, 10)
        self.__draw_circleline(screen, 10, self.__height - 15, self.__width, 10)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            
            #If user presses space button, this method will return false and game will start.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return False
        #If player doesn't press space button, this methos returns value true and start screen will stay on screen.
        return True

