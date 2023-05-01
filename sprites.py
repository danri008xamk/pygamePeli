import pygame
import random

#Parent class that has sprites' common properties and methods.
class Sprite:
    #Every sprite will have x and y values that define loaction of that sprite.
    #Speed determines how many pixels sprite moves.
    #Picture value is a string, that defines which picture file is rendered in that sprite's location.
    def __init__(self, x: int, y: int, speed: int, picture: str):
        self.__x = x
        self.__y = y
        self.__speed = speed
        self.__picture = pygame.image.load(picture)
        #Sprite will have width and height that are defined automatically using the sprite's pictures size.
        self.__width = self.__picture.get_width()
        self.__height = self.__picture.get_height()
    
    #Method for moving sprite towards given point (x,y) on screen.
    #Sprite's speed property defines, how many pixels sprite will move.
    def moveTowards(self, x, y):
        #If given x is bigger than sprites x, sprite is moved to the right.
        if x > self.__x:
            self.__x += self.__speed
        #If given x is smaller than sprites x, sprite is moved to the left.
        if x < self.__x:
            self.__x -= self.__speed
        #If given y is bigger than sprites y, sprite is moved down.
        if y > self.__y:
            self.__y += self.__speed
        #If given y is bigger than sprites y, sprite is moved up.
        if y < self.__y:
            self.__y -= self.__speed

    #Method when sprite is moved directly to the given point.
    def moveTo(self, x, y):
        #Sprites x and y values are changed to given x and y.
        #Half of sprite's pictures width and height are extracted so that sprites middle point will be at given x and y.
        self.__x = x - self.__picture.get_width() / 2
        self.__y = y - self.__picture.get_height() / 2

    #Draws sprites image to it's location on screen.
    def draw(self, screen):
        screen.blit(self.__picture, (self.__x, self.__y))

    #Checks if sprite touches other sprite object.
    #Sprites are toching if their x and y values overlap.
    def is_touching(self, other_sprite: "Sprite"):
        if ((other_sprite.x >= self.__x and other_sprite.x <= self.__x + self.__width) or (self.__x >= other_sprite.x and self.__x <= other_sprite.x + other_sprite.width)) and ((other_sprite.y >= self.__y and other_sprite.y <= self.__y + self.__height) or (self.__y >= other_sprite.y and self.__y <= other_sprite.y + other_sprite.height)):
            return True
        else:
            return False

    #Sprite's properties are capsuled. 
    #These are methods are for easily getting values from sprite's properties.
    @property
    def x(self):
        return self.__x
    @property
    def y(self):
        return self.__y

    @property
    def width(self):
        return self.__width
    @property
    def height(self):
        return self.__height
    

#Class for enemy sprites. Class inherits Sprite class.
#At creation sprite is given a list of tuples, which hold coordinates of possible spawn points.
class Enemy(Sprite):
    def __init__(self, spawn_points: list):
        #Enemy's starting location is randomly selected from the given list.
        spawn_point = random.choice(spawn_points)
        #Calls parent's init method to create new Enemy sprite.
        super().__init__(spawn_point[0], spawn_point[1], random.randint(1, 3), "assets/enemy.png")

#Class that holds a list of enemy sprites
class EnemyList():
    def __init__(self, spawn_points: list):
        #Empty list of enemies 
        self.enemies = []
        #Because EnemyList class has a method that creates new enemy to the list, list of spawn points is given as an attribute.
        self.__spawn_points = spawn_points
    
    #Creates a new enemy sprite that is added to the list.
    def add_enemy(self):
        self.enemies.append(Enemy(self.__spawn_points))
    
    #Deletes an enemy from the list at given index.
    def destroy_enemy(self, index: int):
        self.enemies.pop(index)

    #Loops through the enemy list and calls the draw method of each enemy
    def draw_all(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)
    
    #Loops through the enemy list and moves all enemy sprites one step toward given destination.
    def move_all(self, destination_x, destination_y):
        for enemy in self.enemies:
            enemy.moveTowards(destination_x, destination_y)
    
    #Returns how many enemies exist.
    @property
    def enemy_count(self):
        return len(self.enemies)

#Class for creating King sprite. Class inherits Sprite class.
class King(Sprite):
    def __init__(self, game_width: int, game_height: int):
        #King moves automatically towards random points. Destination property holds x and y values of the current destination.
        self.__destination = (200, 200)
        self.__life = 5
        self.__alive = True
        #Calls parent's init method to create new sprite.
        super().__init__(game_width / 2, game_height / 2, 1, "assets/king.png")
        #King moves randomly on the screen. Max values are used to keep king inside game borders.
        #To avoid enemies hitting king directly at the border, max values are a bit less than border points.
        self.__max_x = game_width - self.width / 2 - 10
        self.__max_y = game_height - self.height / 2 - 10
    
    #Method for moving king sprite towards random point
    def move(self):
        #If king has reached destination, new destination point is selected using random. 
        if self.__destination == (self.x, self.y):
           self.__destination = (random.randint(10, self.__max_x), random.randint(10, self.__max_y))
        #Uses method from the parent class to move king one step towards destination.
        super().moveTowards(self.__destination[0], self.__destination[1])
    
    #Removes one life. If king has no lives left, alive status will be changed to False.
    def take_hit(self):
        self.__life -= 1
        if self.__life <= 0:
            self.__alive = False
   
    @property
    def alive(self):
        return self.__alive
    
    #Method draws king's heart icons on top of the screen. Amount of hearts is defined by kings life amount.
    def draw_hearts(self, screen, start_x, start_y):
        heart = pygame.image.load("assets/heart.png")
        hearts_drawn = 0
        #Drawing method blit is called in the while loop. 
        #Loop will stay on until there is as many hearts on screen as king has lives.
        while (hearts_drawn < self.__life):
            screen.blit(heart, (start_x, start_y))
            start_x += heart.get_width() + 4
            hearts_drawn += 1

#Queen sprite doesn't hold any special properties or methods. Class inherits Sprite class.
#Queen's moving happens in Game class, which uses Sprite classe's methods for moving the queen.
class Queen(Sprite):
    def __init__(self):
        super().__init__(200, 200, 2, "assets/queen.png")
    


#Coin class inherits sprite class.
class Coin(Sprite):
    def __init__(self, game_width, game_height):
        #Property keeps a count of how many times a coin has been collected.
        self.__coin_count = 0
        super().__init__(random.randint(0, game_width), random.randint(0, game_height), 0, "assets/coin.png")
        #Max values are used to keep coin on screen when new location is picked at random.
        self.__max_x = game_width - self.width / 2
        self.__max_y = game_height - self.height / 2
    
    def add_coin(self):
        #Increases coin count.
        self.__coin_count += 1
        #Coin is moved to a new random location.
        self.moveTo(random.randint(0, self.__max_x), random.randint(0, self.__max_y))

    #Writes coin count on given screen to the given location.
    def show_count(self, x: int, y: int, screen):
        font = pygame.font.SysFont("Arial", 20)
        count_text = font.render(f"Coins: {self.__coin_count}", True, (255,255,255))
        screen.blit(count_text, (x, y))