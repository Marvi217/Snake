import os
import turtle
import time
import random
import sys

delay = 0.1
running = True

# Function to get the correct file path in EXE mode
def get_resource_path(relative_path):
    """ Returns the correct path to the resource depending on whether running in EXE mode or development mode """
    try:
        # EXE version
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            # Development version
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    except Exception as e:
        print(f"Error getting path: {e}")
        return relative_path

# Open score file
score_file_path = get_resource_path("resources/Score.txt")
with open(score_file_path, "r") as file:
    data = file.read()

# Score
if data:
    high_score = data
else:
    high_score = 0

high_score = int(high_score)
score = 0

# Window
wn = turtle.Screen()
wn.title("Snake")
wn.bgcolor("green")
wn.setup(800, 800)
wn.tracer(0)

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("black")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Snake body
segments = []

# Food
food = turtle.Turtle()
food.speed(0)
food.shape("square")
food.color("red")
food.penup()
food.goto(random.randint(-14, 14) * 20, random.randint(-14, 14) * 20)

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.penup()
pen.hideturtle()
pen.goto(0, 360)
pen.write("Score: {} High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

# Author
author = turtle.Turtle()
author.speed(0)
author.shape("square")
author.penup()
author.hideturtle()
author.goto(200,-350)
author.write("Author: Marvi", align="center", font=("Courier", 24, "normal"))

# Border
border = turtle.Turtle()
border.speed(0)
border.color("blue")
border.penup()
border.goto(-290, 290)
border.pendown()
border.pensize(4)
for _ in range(4):
    border.forward(582)
    border.right(90)
border.hideturtle()

# Functions
def move():
    match head.direction:
        case "up":
            head.sety(head.ycor() + 20)
        case "down":
            head.sety(head.ycor() - 20)
        case "right":
            head.setx(head.xcor() + 20)
        case "left":
            head.setx(head.xcor() - 20)

def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def quit():
    global running
    running = False

# Keyboard bindings
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_right, "d")
wn.onkeypress(go_right, "Right")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_left, "Left")
wn.onkeypress(quit, "Escape")

# Main game loop
def save_score():
    # Save the score to the Score.txt file in the resources folder
    with open(score_file_path, "w") as file:
        file.write(str(high_score))


try:
    while running:
        wn.update()

        # Check collision with the border
        if (head.xcor() > 280 or head.xcor() < -280 or
            head.ycor() > 280 or head.ycor() < -280):
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()
            save_score()
            score = 0
            delay = 0.1
            pen.clear()
            pen.write("Score: {} High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

        # Check collision with the food
        if head.distance(food) < 20:
            # Move food to random coordinates
            food.goto(random.randint(-14, 14) * 20, random.randint(-14, 14) * 20)
            # Add snake segment
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("dark green")
            new_segment.penup()
            segments.append(new_segment)

            # Increase the score
            score += 10

            if score > high_score:
                high_score = score

            pen.clear()
            pen.write("Score: {} High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

        # Move the end segments first
        for i in range(len(segments)-1, 0, -1):
            segments[i].goto(segments[i-1].xcor(), segments[i-1].ycor())
        # Move segment 0 behind head
        if len(segments) > 0:
            segments[0].goto(head.xcor(), head.ycor())

        move()

        # Check for collision with itself
        for segment in segments:
            if segment.distance(head) < 20:
                time.sleep(1)
                head.goto(0, 0)
                head.direction = "stop"
                for segment in segments:
                    segment.goto(1000, 1000)

                segments.clear()
                save_score()
                score = 0
                delay = 0.1
                pen.clear()
                pen.write("Score: {} High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))
        time.sleep(delay)

except turtle.Terminator:  # Handles window closure by clicking the "X"
    print("Quit")
