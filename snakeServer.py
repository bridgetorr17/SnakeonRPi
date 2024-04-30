from pyrebase import pyrebase
import time


config = {
    "apiKey" : "AIzaSyDedSlCbUhzYqjmjqaa2cuno5mRGKk9Dl4",
    "authDomain" : "raspi-snake.firebaseapp.com",
    "databaseURL" : "https://raspi-snake-default-rtdb.firebaseio.com",
    "storageBucket" : "raspi-snake.appspot.com"
    }

firebase = pyrebase.initialize_app(config)
db = firebase.database()

username = "name"

data = {"User":str(username), "Score":int(10)}
db.child("Scores").set(data)

test = db.child("Scores").get().val()

print(test)

test2 = test.get("Score")

print(test2)

sleep(2)

