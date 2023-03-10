#!/usr/bin/env python
# license removed for brevity

    #goal.target_pose.pose.position.x = 0
    #goal.target_pose.pose.position.y = 0
    #TOP LEFT CORNER:
    #goal.target_pose.pose.position.x = 3.30
    #goal.target_pose.pose.position.y = 2.15
    #TOP RIGHT CORNER:
    #goal.target_pose.pose.position.x = 3.50
    #goal.target_pose.pose.position.y = 0.00
    #BOTTOM LEFT CORNER:
    #goal.target_pose.pose.position.x = 1.32
    #goal.target_pose.pose.position.y = 2.17


import rospy

# Brings in the SimpleActionClient
import actionlib
# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Twist
import spin
import client
import server

def initialise_position():
    return




def movebase_client(goal_x ,goal_y):

   # Create an action client called "move_base" with action definition file "MoveBaseAction"
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
 
   # Waits until the action server has started up and started listening for goals.
    client.wait_for_server()

   # Creates a new goal with the MoveBaseGoal constructor
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

    
    goal.target_pose.pose.position.x = goal_x
    goal.target_pose.pose.position.y = goal_y
    

    goal.target_pose.pose.orientation.w = 1.0

   # Sends the goal to the action server.
    client.send_goal(goal)
   # Waits for the server to finish performing the action.
    wait = client.wait_for_result()
   # If the result doesn't arrive, assume the Server is not available
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
    # Result of executing the action
        return client.get_result()   

# If the python node is executed as main process (sourced directly)
if __name__ == '__main__':
    try:
        rospy.init_node('movebase_client_py')
        spin.main()
        server.main()
        client.normal()
       # Initializes a rospy node to let the SimpleActionClient publish and subscribe
        #Top Right
        result = movebase_client(3.497,0.38)
        if result:
            rospy.loginfo("Goal execution done!")
        #Bottom Left
        result = movebase_client(1.064,2.42)
        if result:
            rospy.loginfo("Goal execution done!")
        #Top Left
        result = movebase_client(3.30,2.15)
        if result:
            rospy.loginfo("Goal execution done!")
        #Bottom Right/ Initial position
        client.park()
        result = movebase_client(0,0)
        if result:
            rospy.loginfo("Goal execution done!")
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
