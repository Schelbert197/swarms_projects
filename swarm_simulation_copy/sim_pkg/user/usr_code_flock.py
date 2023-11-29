"""Srikanth Schelbert ME 409 Lab 4 usr_code.py"""
def usr(robot):
    import struct
    import math
    from random import uniform
    import numpy as np

    # adding a commment
    rep_avg = 5
    velocity = 5
    while True:
        # TODO calculate w, calculate v, average values from each robot, 
        robot.delay(10)
        pose_t = robot.get_pose()
            # if there is a new postion sensor update, print out and transmit the info
        if pose_t: # check pose is valid before using then send x, y, theta
            robot.send_msg(struct.pack('ffi', round(pose_t[0],4), round(pose_t[1],4), robot.assigned_id))

            # Create the taxis vector
            norm = math.sqrt(pose_t[0]**2 + pose_t[1]**2)
            vtaxisx = (0.0 - pose_t[0])/norm
            vtaxisy = (0.0 - pose_t[1])/norm
            
        # gets message from nearby robot to see if it is within vision range and radius.
        msgs = robot.recv_msg()
        if len(msgs) > 0:
            pose_rxed = struct.unpack('ffi', msgs[0][:12])