"""Srikanth Schelbert ME 409 Lab 1 usr_code.py"""
def usr(robot):
    import struct
    import math
    desired_distance = 0.3 #will vary from 0.3-0.5
    diff = 0.0
    vel1 = 15
    vel2 = 10
    while True:

        if (robot.id == 0):
            # if we received a message, print out info in message
            msgs = robot.recv_msg()
            if len(msgs) > 0:
                pose_rxed = struct.unpack('ffi', msgs[0][:12])

            pose_t = robot.get_pose()
                # if there is a new postion sensor update, print out and transmit the info
            if pose_t: # check pose is valid before using
                robot.send_msg(struct.pack('ffi', round(pose_t[0],4), round(pose_t[1],4), robot.id))
                # send pose x,y in message

            if len(msgs) > 0 and pose_t:
                dx1 = pose_rxed[0] - pose_t[0]
                dy1 = pose_rxed[1] - pose_t[1]
                dist1 = math.sqrt(dy1**2 + dx1**2)
                # diff = dist - desired_distance
                print(f"Dist: {dist1}")
                if dist1 <= desired_distance: # Red if out green if in
                    robot.set_led(0,100,0)

                else:
                    robot.set_led(100,0,0)

        if (robot.id == 1):
            # if we received a message, print out info in message
            msgs = robot.recv_msg()
            if len(msgs) > 0:
                pose_rxed = struct.unpack('ffi', msgs[0][:12])

            pose_t = robot.get_pose()
                # if there is a new postion sensor update, print out and transmit the info
            if pose_t: # check pose is valid before using
                robot.send_msg(struct.pack('ffi', round(pose_t[0],4), round(pose_t[1],4), robot.id))
                # send pose x,y in message

            if len(msgs) > 0 and pose_t:
                dx = pose_rxed[0] - pose_t[0]
                dy = pose_rxed[1] - pose_t[1]
                dist = math.sqrt(dy**2 + dx**2)
                diff = dist - desired_distance

                if diff <= 0:
                    # move wheels so the robot goes further out
                    robot.set_vel(vel1,vel2+1)
                    robot.set_led(0,100,0)
                elif diff > 0:
                    # move wheels so the robot goes further in
                    robot.set_vel(vel1,vel2-1)
                    robot.set_led(100,0,0)




            



