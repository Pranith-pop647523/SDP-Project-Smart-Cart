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
from pathlib import Path
import roslaunch
import spin
import rewrite_params
import find_space
import json
from socket import *

IP = '0.0.0.0'

PORT = 50000

BUFLEN = 512

home = str(Path.home())

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
    #wait = client.wait_for_result()
   # If the result doesn't arrive, assume the Server is not available
    #if not wait:
    #    rospy.logerr("Action server not available!")
    #    rospy.signal_shutdown("Action server not available!")
    #else:
    # Result of executing the action
    #    return client.get_result()   


def get_pos():
    rate = rospy.Rate(10) # 10hz 
    listenSocket = socket(AF_INET,SOCK_STREAM,IPPROTO_TCP)
    listenSocket.bind((IP,PORT))
    listenSocket.listen()
    dataSocket, addr = listenSocket.accept()
    print('Accept a client to connect:', addr)
    
    #For when we listen for parking and stopping
    park = False
    pause = False
    while not park:
        if not pause:
            recved = dataSocket.recv(BUFLEN)
            if not recved:
                break
            info = json.loads(recved.decode())
            info['y'] = (float(info['y'])+.4)*(-2.3/3.1)
            info['x'] = (float(info['x']))*(3.5/4.25)
            print(f'info: {info}')
            dataSocket.send(f'info: {info}'.encode())
            movebase_client(info['x'], info['y'])
        else:
            rate.sleep()
            
    dataSocket.close()
    listenSocket.close()
        


# If the python node is executed as main process (sourced directly)
def launch_movebase(home):
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    launch = roslaunch.parent.ROSLaunchParent(uuid, [home+ "/catkin_ws/src/turtlebot3/turtlebot3_navigation/launch/move_base.launch"])
    return launch


def park_cart(launch):
    # For parking
    result = movebase_client(0, 0)
    if result:
        rospy.loginfo("Goal execution done!")
    # rewriting params to parking params before node shuts down to make sure it is ready for the launcher to read when it is set back up
    rewrite_params.rewrite_file(
        home + "/catkin_ws/src/smart_cart/param_settings/dwa_local_planner_params_waffle_pi_parking.yaml")
    launch.shutdown()
    # initialising parking param movebase
    launch = launch_movebase(home)
    launch.start()
    # Bottom Right/ Initial position
    result = movebase_client(0, 0)


if __name__ == '__main__':
    try:
        rewrite_params.rewrite_file(home + "/catkin_ws/src/smart_cart/param_settings/dwa_local_planner_params_waffle_pi_normal.yaml")
        try:
            #initialising normal param move base
            launch = launch_movebase(home)
            launch.start()
            rospy.init_node('movebase_client_py')
            rate = rospy.Rate(10) # 10hz
            for i in range(0,30):
                rate.sleep()   
            #Doing setup movements
            find_space.main()
            spin.main()
            get_pos()
            park_cart(launch)

        except rospy.ROSInterruptException:
            rospy.loginfo("Navigation test finished.")

    except FileNotFoundError:
        rospy.loginfo("Param files were not found.")
    