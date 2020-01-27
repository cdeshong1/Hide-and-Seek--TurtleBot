#!/usr/bin/env python
import time
from subprocess import call

call(['gnome-terminal', '-e', "roslaunch turtlebot_gazebo turtlebot_world.launch world_file:=/home/robert/helloworld/turtlebot_custom_maps/KEC118"])
time.sleep(8)
call(['gnome-terminal', '-e', "roslaunch turtlebot_gazebo gmapping_demo.launch"])
time.sleep(5)
call(['gnome-terminal', '-e', "roslaunch turtlebot_rviz_launchers view_navigation.launch"])
time.sleep(5)
call(['gnome-terminal', '-e', "roslaunch turtlebot_teleop xbox360_teleop.launch"])
time.sleep(5)
