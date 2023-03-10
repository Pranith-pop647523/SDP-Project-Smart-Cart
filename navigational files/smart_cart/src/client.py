#!/usr/bin/env python

import rospy

import dynamic_reconfigure.client


def callback(config):
    rospy.loginfo("Config set to {yaw_goal_tolerance}".format(**config))

client = dynamic_reconfigure.client.Client("move_base/dwa_local_planner/DWAPlannerROS", timeout=30, config_callback=callback)

def park():
    client.update_configuration({"yaw_goal_tolerance":"Parking"})

def normal():
    client.update_configuration({"yaw_goal_tolerance":"Normal"})


    

    