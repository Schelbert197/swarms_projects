"""Srikanth Schelbert ME 409 Lab 4 usr_code.py"""
def usr(robot):
    import struct
    import math
    from random import uniform
    import numpy as np
    import modern_robotics

    # adding a commment
    rep_avg = 5
    velocities = [10,10]
    motor_full_speed = 180 #rpm -100,100 set vel
    set_vel_to_rads = (9/5) * (np.pi/60)
    half_radius_of_wheel = 0.0075
    wheel_rad = 2*half_radius_of_wheel
    dist_between_wheel = 0.08
    while True:
        # TODO calculate w, calculate v, average values from e# ach robot, 
        # wheel set vel in rpm = 9/5
        # wheel rad/s = rpm * (1/60) * (2pirad/rev)
        # wheel rad/s = (9/5) * (2pi/60) * set vel

        F = np.array([[-1/dist_between_wheel, 1/dist_between_wheel],
                      [0.5, 0.5]
                      [0.0,0.0]])
        
        V_twist = F@velocities

        
        
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

            # collect positions of all robots and get cohesion vector

            # Average velocity vec of all robots

            # Normalized repulsion vector of each robot from dist 