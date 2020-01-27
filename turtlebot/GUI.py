#!/usr/bin/env python3

import Tkinter
import time
from subprocess import call

def startButtonHandler():
    global running
    if running == 0:
        running += 1
        timerLabel(1)

def stopButtonHandler():
    global running
    if running == 1:
        running -= 1
        timerLabel(0)

def setupButtonHandler():
    call(['gnome-terminal', '-e', "roslaunch turtlebot_gazebo turtlebot_world.launch"])
    time.sleep(5)
    call(['gnome-terminal', '-e', "roslaunch turtlebot_gazebo gmapping_demo.launch"])
    time.sleep(5)
    call(['gnome-terminal', '-e', "roslaunch turtlebot_rviz_launchers view_navigation.launch"])
    time.sleep(5)
    call(['gnome-terminal', '-e', "roslaunch turtlebot_teleop xbox360_teleop.launch"])
    time.sleep(5)

def timerLabel(stopGoFlag):
    if stopGoFlag == 1:
        countdown(timeLabel)

def countdown(label):
    def count():
        global timer
        global running
        timer -= 1
        mins, secs = divmod(timer, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        label.config(text=str(timeformat)+' remaining')
        if running == 1:
            label.after(1000, count)
    count()

window = Tkinter.Tk()
window.title('Hide and seek but the with robot turtles')
window.geometry('450x150')

running = 0
timer = 300

timeLabel = Tkinter.Label(window)
timeLabel.pack()

startButton = Tkinter.Button(window, text='START', width = 15, height = 5, fg = "green", command = lambda : startButtonHandler())
startButton.pack(side = Tkinter.LEFT)

setupButton = Tkinter.Button(window, text='LAUNCH', width = 15, height = 5, fg = "blue", command = lambda : setupButtonHandler())
setupButton.pack(side = Tkinter.LEFT)

stopButton = Tkinter.Button(window, text='STOP', width = 15, height = 5, fg = "red", command = lambda : stopButtonHandler())
stopButton.pack(side = Tkinter.LEFT)

window.mainloop()
