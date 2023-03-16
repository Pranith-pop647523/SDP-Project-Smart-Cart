# Smart Cart Navigation
This assumes that you have ROS set up using the tutorial/worksheet on the SDP site. Master process must be set to the turtlebot.
## Map Files
Place all map files in your home directory **NOT** in catkin_ws.
Remember to change "image" in map.yaml to your home directory as well.

## param folder
Replace param folder in `catkin_ws/src/turtlebot3/turtlebot3_navigation`

## smart_cart folder
Place the smart_cart folder into `catkin_ws/src`

# Setup
Once files/folders are in the right place, make sure the folder smart_cart and the **files in smart_cart** are executable. This is done by navigating via a terminal to the directory that holds the folder, making the folder executable, cd-ing into the folder and setting each seperate file as executable in turn. The command for this is:  
```chmod +x FileOrFolderName```  
After that, cd .. back to catkin_ws and run `catkin_make`  
If problems occur when doing `catkin_make`, remove the build and devel folders within catkin_ws and try again.

# How to setup the turtlebot
Position turtlebot in starting corner and turn it on. Once the turtlebot is turned on, ssh into it and run the command: `source catkin_ws/devel/setup.bash` before starting the ros service using `roscore` .   
Next, ssh back into the turtlebot in another terminal and run `roslaunch turtlebot3_bringup turtlebot3_robot.launch`

# Running Scripts
## Without custom launcher 
Now open a terminal and **from your computer,** run the command `roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$HOME/map.yaml
` which will launch the program "rviz". Rviz allows you to set navigation goals manually but we have some set coordinates as an example of running scripts. If you want to try it manually, go to the [Robotis Navigation Tutorial](https://emanual.robotis.com/docs/en/platform/turtlebot3/navigation/#navigation).  
To run a script from smart_cart, do `rosrun smart_cart scriptname.py` where the script name is either top_left, top_right, bottom_left, bottom_right, or movebase_client (travels to all of the coordinates from the other scripts)  
 ## With custom launcher
 Run the command `roslaunch smart_cart smart_cart.launch map_file:=$HOME/map.yaml`. That will both open rviz and run the script movebase_client.
