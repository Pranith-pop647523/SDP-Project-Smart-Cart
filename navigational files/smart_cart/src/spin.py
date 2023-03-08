#!/usr/bin/env python

import rospy
import FindEnoughSpace
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

#TODO callback needs to return the ranges. Try using a class.



def spin(pub,rate): 
    
    for i in range(0,60):
        velocity = Twist()
        velocity.angular.z = 1
        pub.publish(velocity)
        rate.sleep()

def main():
    rate = rospy.Rate(10) # 10hz
    print("Sleeping until rviz loads")
    for i in range(0,30):
        rate.sleep()
    try:
        pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        FindEnoughSpace.main()
        spin(pub,rate)
        return
    except rospy.ROSInterruptException:
        pass