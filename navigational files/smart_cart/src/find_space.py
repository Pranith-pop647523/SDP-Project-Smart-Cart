import rospy
import math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
vel = Twist()
foundSpace = False

def callback(msg):
    global vel
    global foundSpace
    minVal = math.inf
    rot_min_val = math.inf
    for i in range(0,360):
        if msg.ranges[i]<minVal and msg.ranges[i] >0.15:
            minVal = msg.ranges[i]
        
    if minVal<0.4:
        #0 = front, 90 = right, 180 = back, 270 = left
        if msg.ranges[0] < rot_min_val:
            rot_min_val = msg.ranges[0]
        if msg.ranges[179] <rot_min_val:
            rot_min_val = msg.ranges[179]
        if msg.ranges[89] <rot_min_val and msg.ranges[89]>0.1:
            rot_min_val = msg.ranges[89]
        if msg.ranges[269] <rot_min_val and msg.ranges[269]>0.1:
            rot_min_val = msg.ranges[269]

        if rot_min_val == msg.ranges[0]:
            vel.linear.x = -0.3
        elif rot_min_val == msg.ranges[179]:
            vel.linear.x = 0.3
        elif rot_min_val == msg.ranges[89]:
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
    sub.unregister
