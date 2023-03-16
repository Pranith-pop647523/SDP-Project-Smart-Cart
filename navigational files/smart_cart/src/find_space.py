import rospy
import math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

vel = Twist()
foundSpace = False

#Aim: get away from any walls by a comfortable distance
def callback(msg):
    global vel
    global foundSpace
    minVal = math.inf
    set_deg_min_val = math.inf
    
    #msg.ranges is an array of 360 values corresponding to the distance the lidar picked up at that degree. Starts at the front.
    for i in range(0,360):
        if msg.ranges[i]<minVal and msg.ranges[i] >0.15:
            minVal = msg.ranges[i]
        
    if minVal<0.4:
        #0 = front, 89 = right, 179 = back, 269 = left
        #set_deg_min_val = the min value of the set degrees
        if msg.ranges[0] < set_deg_min_val:
            set_deg_min_val = msg.ranges[0]
        if msg.ranges[179] <set_deg_min_val:
            set_deg_min_val = msg.ranges[179]
    
        if msg.ranges[89] <set_deg_min_val and msg.ranges[89]>0.2:
            set_deg_min_val = msg.ranges[89]
        if msg.ranges[269] <set_deg_min_val and msg.ranges[269]>0.2:
            set_deg_min_val = msg.ranges[269]

        if set_deg_min_val == msg.ranges[0]:
            vel.linear.x = -0.3
        elif set_deg_min_val == msg.ranges[179]:
            vel.linear.x = 0.3
        elif set_deg_min_val == msg.ranges[89]:
            vel.angular.z = 1
        else:
            vel.angular.z = -1

    else:
        vel.linear.x = 0.0
        vel.angular.z = 0.0
        foundSpace = True

def main():
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    sub = rospy.Subscriber('scan',LaserScan,callback)
    rate = rospy.Rate(10) # 10hz
    while foundSpace!=True:
        pub.publish(vel)
        rate.sleep()
    #Leaving a cmd_vel publisher running messes with the movebase nodes
    pub.unregister
    sub.unregister
