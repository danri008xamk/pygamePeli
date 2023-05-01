import pygame
import sprites

class Game:
    def __init__(self, game_width, game_height):
        #Count game screens corners. Will be used as spawn points for enemy sprites.
        corners = [(-10, -10), (game_width+10, -10), (-10, game_height+10), (game_width+10, game_height+10)]
        #Create sprites
        self.king = sprites.King(game_width, game_height)
        self.queen = sprites.Queen()
        self.enemies = sprites.EnemyList(corners)
        self.coin = sprites.Coin(game_width, game_height)
        #Variable to keep a count of how many times game has looped. This is used to track game time.
        self.loops = 0
    
    def draw_game(self, screen):
        self.loops += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            #Queen is drawn to the cursor point
            if event.type == pygame.MOUSEMOTION:
                self.queen.moveTo(event.pos[0], event.pos[1])
        self.king.move()
        #Loops through all enemy sprites and moves them towards king)
        self.enemies.move_all(self.king.x, self.king.y)
        
        #Game's tick is 60 frames per second.
        #Two enemies are created every second.
        if self.loops == 60:
            if self.enemies.enemy_count < 7: #Max amount of enemies on screen.
                self.enemies.add_enemy()
                self.enemies.add_enemy()
            self.loops = 0 #Reset loop count
        
        #Loops through list of enemies to check sprite collision
        for index, enemy in enumerate(self.enemies.enemies):
            if enemy.is_touching(self.king):
                #Enemy sprite is destroyed on hit.
                self.enemies.destroy_enemy(index)
                #King looses one heart when enemy touches it.
                self.king.take_hit()

            if enemy.is_touching(self.queen):
                #Enemy sprite is destroyed on hit.
                self.enemies.destroy_enemy(index)
        #If queen sprite touches coin sprite, coin count is increased and coin is moved to a new position.
        if self.coin.is_touching(self.queen):
            self.coin.add_coin()
        
        #Clears previous game loop by filling screen with base color.
        screen.fill((0, 0, 0))
        #Draw sprites, points and hearts on screen.
        self.enemies.draw_all(screen)
        self.king.draw(screen)
        self.king.draw_hearts(screen, 300, 5)
        self.queen.draw(screen)
        self.coin.draw(screen)
        self.coin.show_count(200, 5, screen)

        #Every game loop checks if king is still alive.
        #Main file uses this information to determine if game is still on.
        return self.king.alive