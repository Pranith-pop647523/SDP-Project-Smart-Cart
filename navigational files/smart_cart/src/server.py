#!/usr/bin/env python

import rospy

from dynamic_reconfigure.server import Server
from smart_cart.cfg import movebase

def callback(config, level):
    rospy.loginfo("""Reconfigure Request: {yaw_goal_tolerance}""".format(**config))
    return config

def main():
    rospy.init_node("test", anonymous = False)

    srv = Server(movebase, callback)
    rospy.spin()