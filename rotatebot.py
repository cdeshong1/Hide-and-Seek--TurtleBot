#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
import time
twist=Twist()

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('rotate_robot', anonymous=True)

    rospy.Subscriber('coordinates', Float32, callback)
    rospy.Subscriber('direction', String, callback2)
    time.sleep(5)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %f", data.data)
    pub = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=5)
    if(data.data>50):
	twist.linear.x=0.3
    else:
	twist.linear.x=0
    pub.publish(twist)

def callback2(data):
    rospy.loginfo(rospy.get_caller_id() + "I saw %s", data.data)
    pub = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=5)
    x = float(data.data)
    if(x >= 0 and x < 200):
	twist.angular.z = 0.9 #pos for left, neg for right
    elif(x >= 200 and x <= 400):
	twist.angular.z = 0 
    elif(x > 400 and x <= 600):
	twist.angular.z = -0.9
    pub.publish(twist)

if __name__ == '__main__':
    listener()
    
