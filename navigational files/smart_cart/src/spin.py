import rospy
from geometry_msgs.msg import Twist
import actionlib

    
from geometry_msgs.msg import Twist #

def callback():
    

        move.linear.x = 0.0 # stop
        move.angular.z = 0.5 # rotate counter-clockwise

    pub.publish(move) # publish the move object


move = Twist() # Creates a Twist message type object
rospy.init_node('obstacle_avoidance_node') # Initializes a node
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)  # Publisher object which will publish "Twist" type messages
                            				 # on the "/cmd_vel" Topic, "queue_size" is the size of the
                                                         # outgoing message queue used for asynchronous publishing



rospy.spin() # Loops infinitely until someone stops the program execution

#if __name__ == '__main__':
   # try:
    #    callback():
    #except rospy.ROSInterruptException:
     #   pass
callback()