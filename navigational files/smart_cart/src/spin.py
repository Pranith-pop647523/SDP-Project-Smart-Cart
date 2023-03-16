#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

#Aim: Spin once to more accurately place walls
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
        spin(pub,rate)
        #Leaving a cmd_vel publisher running messes with the movebase nodes
        pub.unregister
        return
    except rospy.ROSInterruptException:
        pass