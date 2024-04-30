from sense_hat import SenseHat
from time import sleep
import random

sense = SenseHat()

GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
START_DELAY = 3
MATRIX_MIN_VALUE = 0
MATRIX_MAX_VALUE = 7
MATRIX_SIZE = 8

def growSnake():
    snakePosX.append(0)
    snakePosY.append(0)
    
def generateFood():
   foodPosXY = []
   while True:
        foodPosX = random.randint(0,7)
        foodPosY = random.randint(0,7)
        #find food spot that is not on top of the snake
        if (foodPosX != snakePosX[0] or foodPosY != snakePosY[0]):
            foodPosXY.append(foodPosX)
            foodPosXY.append(foodPosY)
            return foodPosXY
        
def move(movementX, movementY):
    for event in sense.stick.get_events():
        #move left if not moving right
        if event.direction == "left" and movementX != 1:
            movementX = -1
            movementY = 0
        #move right if not moving left
        elif event.direction == "right" and movementX != -1:
            movementX = 1
            movementY = 0
        #move up if not moving down
        elif event.direction == "up" and movementY != 1:
            movementX = 0
            movementY = -1
        #move down if not moving up
        elif event.direction == "down" and movementY != -1:
            movementX = 0
            movementY = 1
    movement = []
    movement.append(movementX)
    movement.append(movementY)
    return movement
    
def death(snakeX, snakeY):
    gameOver = False
    for i in range(1, len(snakeX)):
        if snakeX[i] == snakeX[0] and snakeY[i] == snakeY[0]:
            gameOver = True
    return gameOver
    
while True:
    gameOver = False
    growSnake = False
    randomFood = False
    movementDelay = 0.35
    movement = [0,0]
    wrappedSnake = [0,0]
    score = 0
    
    sense.clear()
    sense.show_message("SNAKEY")
    
    snakePosX = [3]
    snakePosY = [3]
        
    sense.clear()
    foodPos = generateFood()
    sense.set_pixel(foodPos[0], foodPos[1], RED)
    
    #show snake
    sense.set_pixel(snakePosX[0], snakePosY[0], GREEN)
    
    #start movement
    while not gameOver:
        #if snake eats food
        if snakePosX[0] == foodPos[0] and snakePosY[0] == foodPos[1]:
            score += 1
            foodPos = generateFood()
            snakePosX.append(0)
            snakePosY.append(0)
        
        #check if snake bites itsel
        gameOver = death(snakePosX, snakePosY)  
        
        #Move Snake
        for i in range ((len(snakePosX) - 1), 0, -1):
            snakePosX[i] = snakePosX[i-1]
            snakePosY[i] = snakePosY[i-1]

        movement = move(movement[0], movement[1])
        snakePosX[0] += movement[0]
        snakePosY[0] += movement[1]
        
        if snakePosX[0] > MATRIX_MAX_VALUE or snakePosX[0] < MATRIX_MIN_VALUE:
            gameOver = True
            
        if snakePosY[0] > MATRIX_MAX_VALUE or snakePosY[0] < MATRIX_MIN_VALUE:
            gameOver = True
            
        if gameOver:
            sense.clear()
            sense.show_message("slaughtered")
            sense.show_message("Score: {}".format(score))
            score = 0
            break
        
        #Update Matix
        sense.clear()
        for x,y in zip(snakePosX, snakePosY):
            sense.set_pixel(x, y, GREEN)
        print(foodPos[0])
        print(foodPos[1])
        sense.set_pixel(foodPos[0], foodPos[1], RED)
        sleep(movementDelay)