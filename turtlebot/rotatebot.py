#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
import time
import subprocess
from kobuki_msgs.msg import BumperEvent
twist=Twist()
bump = False
x = 300
p = subprocess.Popen(['python', '/home/duncan/Desktop/turtlebot/Initial.py'])
count = 0

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    
    rospy.init_node('rotate_robot', anonymous=True, disable_signals=True)
    rospy.Subscriber('coordinates', Float32, callback)
    rospy.Subscriber('direction', String, callback2)
    rospy.Subscriber('mobile_base/events/bumper', BumperEvent, processBump)
    # spin() simply keeps python from exiting until this node is stopped
    while not rospy.core.is_shutdown():
	if(bump == True):
	    s = subprocess.Popen(['python', '/home/duncan/Desktop/turtlebot/ReturnHome.py'])
	    time.sleep(5)
	    exit()
        rospy.rostime.wallsleep(0.5)

def callback(data):
    global count
    rospy.loginfo(rospy.get_caller_id() + "I heard %f", data.data)
    pub = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=5)
    if(data.data>50 and count >= 3 and x >= 200 and x <= 400):
	p.terminate()
	twist.linear.x=0.3
    elif(data.data>50):
	count = count + 1
       	twist.linear.x=0
    else:
	twist.linear.x=0
	count = 0
    pub.publish(twist)

def callback2(data):
    rospy.loginfo(rospy.get_caller_id() + "I saw %s", data.data)
    pub = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=5)
    global x
    x = float(data.data)
    if(x >= 0 and x < 200):
	twist.angular.z = 0.9 #pos for left, neg for right
	twist.linear.x=0
    elif(x >= 200 and x <= 400):
	twist.angular.z = 0 
    elif(x > 400 and x <= 600):
	twist.angular.z = -0.9
	twist.linear.x=0
    pub.publish(twist)

    #if bump data is received, process here
    #data.bumper: LEFT (0), CENTER (1), RIGHT (2)
    #data.state: RELEASED(0), PRESSED(1)
def processBump(data):
    global bump
    if (data.state == BumperEvent.PRESSED):
        bump = True

if __name__ == '__main__':
    listener()
