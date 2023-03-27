#include <custom_recovery/custom_recovery.h>
#include <pluginlib/class_list_macros.h>
#include <nav_core/parameter_magic.h>
#include <tf2/utils.h>
#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <geometry_msgs/Point.h>
#include <angles/angles.h>
#include <algorithm>
#include <string>
#include <sensor_msgs/LaserScan.h>
geometry_msgs::Twist vel;
bool foundSpace = false;


void callback(const sensor_msgs::LaserScan::ConstPtr& msg){
  int nums[360];
  for (int i = 0; i < 360; i++){
    nums[i] = msg->ranges[i];
    }
  double minVal = std::numeric_limits<double>::infinity();
  double set_deg_min_val = std::numeric_limits<double>::infinity();
  for (int i = 0; i < 360; i++){
    if (nums[i]< minVal && nums[i] >0.15){
        minVal = nums[i];
    }
  }
  if (minVal<0.4){
    //0 = front, 89 = right, 179 = back, 269 = left
    //set_deg_min_val = the min value of the set degrees
    if (nums[0] < set_deg_min_val){
        set_deg_min_val = nums[0];
    }
    if (nums[179] <set_deg_min_val){
      set_deg_min_val = nums[179];
    }
         
    if (nums[89] <set_deg_min_val && nums[89]>0.2){
      set_deg_min_val = nums[89];
    }
    if (nums[269] <set_deg_min_val && nums[269]>0.2){
      set_deg_min_val = nums[269];
    }     
    if (set_deg_min_val == nums[0]){
      vel.linear.x = -0.3;
    }
        
    else if (set_deg_min_val == nums[179]){
      vel.linear.x = 0.3;
    }
    else if (set_deg_min_val == nums[89]){
      vel.angular.z = 1;
    }
            
    else{
      vel.angular.z = -1;
      }
  }
  else {
    vel.linear.x = 0.0;
    vel.angular.z = 0.0;
    foundSpace = true;
  }
}



// register this planner as a RecoveryBehavior plugin
PLUGINLIB_EXPORT_CLASS(custom_recovery::CustomRecovery, nav_core::RecoveryBehavior)

namespace custom_recovery
{
CustomRecovery::CustomRecovery(): local_costmap_(NULL), initialized_(false), world_model_(NULL)
{
}
  
void CustomRecovery::initialize(std::string name, tf2_ros::Buffer*,
                                costmap_2d::Costmap2DROS*, costmap_2d::Costmap2DROS* local_costmap)
{
  if (!initialized_)
  {
    local_costmap_ = local_costmap;

    // get some parameters from the parameter server
    ros::NodeHandle private_nh("~/" + name);
    ros::NodeHandle blp_nh("~/TrajectoryPlannerROS");

    // we'll simulate every degree by default
    private_nh.param("sim_granularity", sim_granularity_, 0.017);
    private_nh.param("frequency", frequency_, 20.0);

    acc_lim_th_ = nav_core::loadParameterWithDeprecation(blp_nh, "acc_lim_theta", "acc_lim_th", 3.2);
    max_rotational_vel_ = nav_core::loadParameterWithDeprecation(blp_nh, "max_vel_theta", "max_rotational_vel", 1.0);
    min_rotational_vel_ = nav_core::loadParameterWithDeprecation(blp_nh, "min_in_place_vel_theta", "min_in_place_rotational_vel", 0.4);
    blp_nh.param("yaw_goal_tolerance", tolerance_, 0.10);

    world_model_ = new base_local_planner::CostmapModel(*local_costmap_->getCostmap());

    initialized_ = true;
  }
  else
  {
    ROS_ERROR("You should not call initialize twice on this object, doing nothing");
  }
}
  
CustomRecovery::~CustomRecovery()
{
  delete world_model_;
}

void CustomRecovery::runBehavior()
{
  if (!initialized_)
  {
    ROS_ERROR("This object must be initialized before runBehavior is called");
    return;
  }

  if (local_costmap_ == NULL)
  {
    ROS_ERROR("The costmap passed to the RotateRecovery object cannot be NULL. Doing nothing.");
    return;
  }
  ROS_WARN("Rotate recovery behavior started.");

  ros::Rate r(frequency_);
  ros::NodeHandle n;
  ros::Publisher vel_pub = n.advertise<geometry_msgs::Twist>("cmd_vel", 10);
  ros::Subscriber scanner_sub = n.subscribe<sensor_msgs::LaserScan>("scan",10,callback);
  while(!foundSpace) {
    vel_pub.publish(vel);
    r.sleep();
  }
  scanner_sub.shutdown();
  vel_pub.shutdown();
}
};  // namespace rotate_recovery
