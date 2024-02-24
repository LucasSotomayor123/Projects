import pygame
import random
import os   



pygame.init()

#Dimensions of the game window
screenWidth = 400
screenLength = 600

#Create game window
screen = pygame.display.set_mode((screenWidth, screenLength))
pygame.display.set_caption('Back Home')

#create frame rate
clock = pygame.time.Clock()
FPS = 60

#variables
scrollThresh = 200
gravity = 1
maxPlatform = 10
upperLimit = 200
scroll = 0
bgScroll = 0
gameOver = False
score = 0
fadeCounter = 0
newHighscore = 0


if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        highScore = int(file.read())
else:
    highScore = 0

#colors
white =(255,255,255)
black = (0, 0, 0)

#define font

fontSmall = pygame.font.SysFont('Lucida Sans', 20)
fontLarge = pygame.font.SysFont('Lucida Sans', 24)

#load images
AlienImage = pygame.image.load("assets/Alien__.png").convert_alpha()
bgImage = pygame.image.load('assets/Bg.jpg').convert_alpha()
platformImage = pygame.image.load('assets/Pad_02_1.png').convert_alpha()



#Function to put font to screen
def drawText(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


#drawing info panel
def drawPanel():
    pygame.draw.line(screen, white, (0,30), (screenWidth, 30), 2)
    drawText('SCORE: ' + str(score), fontSmall, white,0,0)

#drawing the bg
def drawBg(bgscroll): 
    screen.blit(bgImage, (0, 0 + bgscroll))
    screen.blit(bgImage, (0, -600 + bgscroll))

#player class

class player():

    def __init__(self, x, y):
        self.image = pygame.transform.scale(AlienImage, (55,55)) 
        self.width = 22
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height) #creating the collision rectangle (hitbox for the sprite)
        self.rect.center = (x,y)
        self.velocityY = 0
  
    def move(self):
        scroll = 0
        # change in Y and X
        dx =0
        dy =0

        #key pressing
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx-= 8
        if key[pygame.K_d]:
            dx+= 8

        #Gravity
        self.velocityY += gravity
        dy = self.velocityY

        #double check if its going to move off the screen
        if self.rect.left + dx < 0:
            dx = 0 -self.rect.left
        if  self.rect.right + dx > 400:
           dx = screenWidth -self.rect.right


        #collsion with platform
        for platform in platformGroup:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.rect.bottom < platform.rect.centery:
                    if self.velocityY > 0:
                        self.velocityY = -20
                        dy = 0

        #check if player moves above upper limit
        if self.rect.top <= upperLimit:
            #if player only jumping
            if self.velocityY < 0:
                scroll = -dy
    
        #update rect postiion
        self.rect.x += dx
        self.rect.y += dy + scroll
       
        return scroll

    def draw(self):  #image     #where rect is the player is drawn there
        screen.blit(self.image, (self.rect.x -14, self.rect.y- 12)) #creating the image adjusting it into the hitbox
       # pygame.draw.rect(screen, white, self.rect, 2) 


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving):  
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platformImage, (width, 10)) 
        self.moving = moving
        self.moveCounter = random.randint(0, 50)
        self.direction = random.choice([-1 ,1])
        self.speed = random.randint(1,2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y  
       
    
    def update(self, scroll):
        #power up platform 
        

        #moving platform side to side if its a moving platform
        if self.moving == True:
            self.moveCounter += 1
            self.rect.x += self.direction * self.speed
        #change platform direction if it has moved fully pr hit a wall
        if self.moveCounter >= 100 or self.rect.left < 0 or self.rect.right > screenWidth:
            self.direction *= -1
            self.moveCounter = 0

        # this will update the platforms verticle postiion
        self.rect.y += scroll
        #Check if platform gone off the screen

        if self.rect.top > screenLength:
            self.kill()


#player creation
Alien = player(screenWidth // 2, screenLength - 150)

#create sprite groups
platformGroup = pygame.sprite.Group()

#create starting platform
platform = Platform(screenWidth // 2 - 50, screenLength - 50, 100, False)
platformGroup.add(platform)
#game loop
keepRunning = True
while keepRunning:
    # FPS
    clock.tick(FPS)

    # Move Sprite
    if gameOver == False:
        scroll = Alien.move()

        # Draw the background
        if bgScroll >= 600:
            bgScroll = 0
        bgScroll += scroll
        drawBg(bgScroll)

        # Generate platforms
        if len(platformGroup) < maxPlatform:
            platformWidth = random.randint(40, 60)
            platformX = random.randint(0, screenWidth - platformWidth)
            platformY = platform.rect.y - random.randint(80, 120)
            platformType = random.randint(1, 2)
            if platformType == 1 and score > 500:
                platformMoving = True
            else:
                platformMoving = False
                
            platform = Platform(platformX, platformY, platformWidth, platformMoving)
            platformGroup.add(platform)


        # Update platforms
        platformGroup.update(scroll)

        #update score
        if scroll > 0:
            score += scroll

        #draw line at highscore
        pygame.draw.line(screen, white, (0, score - highScore + scrollThresh), (screenWidth, score - highScore + scrollThresh), 3)
        drawText('HIGH SCORE', fontSmall, white, screenWidth - 130,score - highScore + scrollThresh)

        #draw highscore 
        
        # Draw sprites
        platformGroup.draw(screen)
        Alien.draw()

        #DrawPanels 
        drawPanel()

        # Check game over
        if Alien.rect.top > screenLength:
            gameOver = True      
    else:
        if fadeCounter < screenWidth:
            fadeCounter += 6.7
            pygame.draw.rect(screen, black, (0, 0, fadeCounter, screenLength))
        else:
            drawText('GAME OVER!', fontLarge, white, 130, 200)
            drawText('SCORE: ' + str(score), fontLarge, white, 130, 250)
            drawText('PRESS SPACE TO PLAY AGAIN', fontLarge, white, 40, 350)

            #update highschore
            if score > highScore:
                highScore = score
                with open('score.txt', 'w') as file:
                    file.write(str(highScore))

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                # Your code continues here for handling the space key press.
                    gameOver = False
                    score = 0
                    scroll = 0
                    fadeCounter = 0
                    #reset player
                    Alien.rect.center = (screenWidth // 2, screenLength - 150)
                    #reset platform
                    platformGroup.empty()
                    platform = Platform(screenWidth // 2 - 50, screenLength - 50, 100, False)
                    platformGroup.add(platform) 
                

    # Handle how to quit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #update highschore
            if score > highScore:
                highScore = score
                with open('score.txt', 'w') as file:
                    file.write(str(highScore))
            keepRunning = False

    pygame.display.update()

pygame.quit()







