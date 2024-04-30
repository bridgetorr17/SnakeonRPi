from sense_hat import SenseHat
from time import sleep
import random
import smbus
import RPi.GPIO as GPIO
from pyrebase import pyrebase

sense = SenseHat()

#Joystick i2c variables
address = 0x48
bus = smbus.SMBus(1)
cmd = 0x40

#server configurations
config = {
    "apiKey" : "AIzaSyDedSlCbUhzYqjmjqaa2cuno5mRGKk9Dl4",
    "authDomain" : "raspi-snake.firebaseapp.com",
    "databaseURL" : "https://raspi-snake-default-rtdb.firebaseio.com",
    "storageBucket" : "raspi-snake.appspot.com"
    }

firebase = pyrebase.initialize_app(config)
db = firebase.database()

username = "demo"

#sound variables
SPEED = 1

tones = {
    "C6":1047,
    "B5":988,
    "A5":880,
    "G5":784,
    "F5":698,
    "E5":659,
    "EB5":622,
    "D5":587,
    "C5":523,
    "B4":494,
    "A4":440,
    "AB4":415,
    "G4":392,
    "F4":349,
    "E4":330,
    "D4":294,
    "C4":262}

move_sound = [["E5",32], ["D5", 32],["G4",32],["E4",32]]
eat_sound = [["E5", 16],["C6",16],["C5",16]]
death_sound = [["F4",8],["E4",8],["D4",8],["C4",4]]

#display colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
START_DELAY = 3
MATRIX_MIN_VALUE = 0
MATRIX_MAX_VALUE = 7
MATRIX_SIZE = 8

#GPIO pins 
Z_Pin = 24
Speaker_pin = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(Speaker_pin, GPIO.OUT)
GPIO.setup(Z_Pin, GPIO.IN, GPIO.PUD_UP)

highscore = 0

def playTone(p, t):
    duration = (1./(t[1]*0.25*SPEED))
    
    if (t[0]=="P"):
        sleep(duration)
    else:
        frequency = tones[t[0]]
        p.ChangeFrequency(frequency)
        p.start(0.5)
        sleep(duration)
        p.stop()
    
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
        
def analogRead(chn):
    bus.write_byte(address, cmd+chn)
    value = bus.read_byte(address)
    return value
        
def getJoystickDir():
    direction = ""
    val_Z = GPIO.input(Z_Pin)
    val_Y = analogRead(0) #Y output at AIN0
    val_X = analogRead(1) #X output at AIN1
    if (val_Y < 100) and (190<val_X<235): #up
        direction = "up"
    if (val_Y > 150) and (190<val_X<235): #down
        direction = "down"
    if (val_X > 235) and (100<val_Y<150): #right
        direction = "right"
    if (val_X < 100) and (100<val_Y<150): #left
        direction = "left"
    print(direction) #debugging
    return direction
        
def move(movementX, movementY, p):
    joyDirection = getJoystickDir()
    #move left if not moving right
    if joyDirection == "left" and movementX != 1:
        movementX = -1
        movementY = 0
        playTone(p, move_sound[3]);
    #move right if not moving left
    elif joyDirection == "right" and movementX != -1:
        movementX = 1
        movementY = 0
        playTone(p, move_sound[1]);
    #move up if not moving down
    elif joyDirection == "up" and movementY != 1:
        movementX = 0
        movementY = -1
        playTone(p, move_sound[0]);
    #move down if not moving up
    elif joyDirection == "down" and movementY != -1:
        movementX = 0
        movementY = 1
        playTone(p, move_sound[2]);
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
    p = GPIO.PWM(Speaker_pin, 440)
    
    sense.clear()
    sense.show_message("Go!")
    
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

        movement = move(movement[0], movement[1], p)
        snakePosX[0] += movement[0]
        snakePosY[0] += movement[1]
        
        if snakePosX[0] > MATRIX_MAX_VALUE or snakePosX[0] < MATRIX_MIN_VALUE:
            gameOver = True
            
        if snakePosY[0] > MATRIX_MAX_VALUE or snakePosY[0] < MATRIX_MIN_VALUE:
            gameOver = True
            
        if gameOver:
            for t in death_sound:
                playTone(p, t)
            
            #show messages on sense hat
            sense.clear()
            sense.show_message("Dead")
            sense.show_message("Score: {}".format(score))
            
            #interact with server
            scoreList = db.child(username).get().val()
            if(scoreList != None):
                curr = scoreList.get("Score")
            else: # first score
                data = {"Score":int(score)}
                db.child(username).set(data)
                highscore = score
                curr = score
            
            if (score > curr):
                data = {"Score":int(score)}
                db.child(username).set(data)
                highscore = score
            else:
                highscore = curr
                
            sense.show_message("Hi Sc: {}".format(highscore))
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