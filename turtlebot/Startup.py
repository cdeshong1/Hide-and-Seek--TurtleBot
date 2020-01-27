#!/usr/bin/env python
import paramiko
import time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh = paramiko.SSHClient()
ssh.connect('10.127.16.129', username='turtlebot2', password='a')
shell = client.invoke_shell()
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("roslaunch turtlebot_bringup minimal.launch")

roslaunch turtlebot_rviz_launchers view_navigation.launch --screen
roslaunch turtlebot_navigation amcl_demo.launch map_file:=/home/robert/map.yaml
roslaunch turtlebot_gazebo turtlebot_world.launch world_file:=/home/robert/helloworld/turtlebot_custom_maps/KEC118
