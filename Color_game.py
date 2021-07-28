import tkinter
import random
from tkinter import Label, font

# List of possible colors
colors = ['Red','Blue','Green','Yellow','Black','White','Pink','Purple','Orange','Brown']

score = 0
# Game time left
timeLeft = 30

# Function that will start the game
def startGame(event):

    if timeLeft == 30:
        # start the timer
        countdown()
    # function to choose the next color
    nextColor()

def nextColor():

    global score
    global timeLeft
    # if the game is still on
    if timeLeft>0:
        # make the entry box active
        e.focus_set()
        
        # if color typed is correct
        if e.get().lower() == colors[1].lower():
            score += 1
        
        # clear the box entry
        e.delete(0,tkinter.END)

        random.shuffle(colors)
        
        # Now change the color and text type
        label.config(fg = str(colors[1]), text = str(colors[0]))

        # update the score
        scoreLabel.config(text = "Score: " + str(score))

# countdown function
def countdown():
    global timeLeft

    if timeLeft > 0:
        timeLeft -= 1

        timeLabel.config(text = "Time Left: " + str(timeLeft))

        timeLabel.after(1000, countdown)

# creating GUI window
root = tkinter.Tk()
root.title("COLOR GAME")
root.geometry("375x200")

instructions = tkinter.Label(root, text = "Type in the color of the words and not the word text",font = ('Helvetica', 12))

instructions.pack()

# adding a score label
scoreLabel = tkinter.Label(root, text ="Press enter to start", font = ('Helvetica', 12))

scoreLabel.pack()

# adding a time left label
timeLabel = tkinter.Label(root, text="Time Left: "+str(timeLeft), font=('Helvetica',12))

timeLabel.pack()

# adding a label
label = tkinter.Label(root, font = ('Helvetica',60))
label.pack()

# adding entry box for typing colors
e = tkinter.Entry(root)

root.bind('<Return>', startGame)
e.pack()

# set focus on the entry box
e.focus_set()

# start the GUI
root.mainloop()

