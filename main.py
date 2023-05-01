import pygame
import screens
import gameplay

#Creating game window.
pygame.init()
game_width = 600
game_height = 600
screen = pygame.display.set_mode((game_width, game_height))

#Boolean variables to keep a track of which screen should be shown.
startscreen_on = True
game_on = False

#Screen's are objects defined in separate files.
start_screen = screens.Startscreen(game_width, game_height)
game_screen = gameplay.Game(game_width, game_height)
end_screen = screens.Endscreen(game_width, game_height)

#Pygame clock that is used to control game loops.
clock = pygame.time.Clock()

#Game loop
while True:
    if startscreen_on:
        #Startscreen's draw method will return false, if player starts the game
        startscreen_on = start_screen.draw_screen(screen)
        #If player has started game, game_on is turned to True.
        if not startscreen_on:
            game_on = True
    #If both startscreen_on and game_on are false, ending screen is drawn.
    elif not game_on:
        end_screen.draw_screen(screen)
        
    else:
        #Game screens draw method will return true if king sprite is alive.
        game_on = game_screen.draw_game(screen)

    clock.tick(60)
    #Update drawn screen to the display.
    pygame.display.flip()