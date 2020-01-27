#! /usr/bin/python

import sys
from subprocess import call
import time

call(['gnome-terminal', '-e', "roscore"])
time.sleep(5)
call(['gnome-terminal', '-e', "rosrun rviz_python_tutorial TurtleGui.py"])

