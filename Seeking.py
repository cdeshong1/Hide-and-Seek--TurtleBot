#!/usr/bin/env python
from __future__ import print_function

import roslib
roslib.load_manifest('color_package')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from collections import deque
from std_msgs.msg import Float32
import numpy as np
import argparse
import imutils
import time
from geometry_msgs.msg import Twist
msg=Twist()
class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("image_topic_2",Image, queue_size = 1)
    self.cv_image = None
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.callback)

  def callback(self,data):
    try:
      self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    (rows,cols,channels) = self.cv_image.shape
    if cols > 60 and rows > 60 :
      cv2.circle(self.cv_image, (50,50), 10, 255)
	
    cv2.waitKey(3)
    self.talker()
   
  def talker(self):
	pub=rospy.Publisher('coordinates',Float32,queue_size=5)
	pub2=rospy.Publisher('direction',String,queue_size=5)
  	rate = rospy.Rate(20) # 10hz
        ap = argparse.ArgumentParser()
	ap.add_argument("-b", "--buffer", type=int, default=64,help="max buffer size")
	args = vars(ap.parse_args())

	greenLower = (29, 86, 150)
	greenUpper = (55, 255, 220)
	pts = deque(maxlen=64)
	camera = self.cv_image
	#print(camera)
	frame = camera
	frame = imutils.resize(frame, width=600)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	if len(cnts) > 0:
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		#print(center)
		pub.publish(int(M["m01"] / M["m00"]))
		pub2.publish(str(x))
		rospy.loginfo(int(M["m01"] / M["m00"]))
		rate.sleep()
		if radius > 10:
			cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
	pts.appendleft(center)
	for i in xrange(1, len(pts)):
		if pts[i - 1] is None or pts[i] is None:
			continue
		thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

	cv2.imshow("Frame", frame)

def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
