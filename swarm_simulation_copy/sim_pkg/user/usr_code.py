"""Srikanth Schelbert ME 409 Lab 3 usr_code.py"""
def usr(robot):
    import struct
    import math
    from random import uniform
    import numpy as np

    # adding a commment
    k = 6.7
    c_rand = 0.4
    x_rep_list = []
    y_rep_list = []
    rep_avg = 5
    velocity = 5
    while True:
        robot.delay(10)
        if (robot.assigned_id == 0):
            radius = 0.06
            # if we received a message, print out info in message
            robot.set_led(100,0,0)
            vrepx = 0.0
            vrepy = 0.0

            # Create random vector
            rand_theta = uniform(0.0,1.0)
            vrandx = np.cos(np.pi * rand_theta * 2)
            vrandy = np.sin(np.pi * rand_theta * 2)

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
                x_rep_list.append(pose_rxed[0])
                y_rep_list.append(pose_rxed[1])

            if len(x_rep_list) > rep_avg and pose_t and len(x_rep_list) % 5 == 0:
                x_center = np.average(x_rep_list[-rep_avg:])
                y_center = np.average(y_rep_list[-rep_avg:])
                dx1 = x_center- pose_t[0]
                dy1 = y_center - pose_t[1]
                dist1 = math.sqrt(dy1**2 + dx1**2)

                # Calculate repulsion vector
                if dist1 < 2*radius:
                    # calculates repulsion vector !!!!!!!!!! NEED TO INCLUDE SENSING!!!!!!!!!!!!!!!!!!
                    magnitude = -k*(2*radius - dist1)
                    vrepx = magnitude * (dx1/dist1)
                    vrepy = magnitude * (dy1/dist1)
                    # robot.set_led(100,100,100)
                else:
                    # ignores repulsion if no robots in range
                    vrepx = 0.0
                    vrepy = 0.0
            else:
                continue

            vix =  vtaxisx  + vrepx + (c_rand * vrandx)
            viy =  vtaxisy  + vrepy + (c_rand * vrandy)
            
            v_headx = np.cos(pose_t[2])
            v_heady = np.sin(pose_t[2])
            v_head = [v_headx, v_heady]
            vi = [vix, viy]
            theta_turn = math.atan2(np.linalg.det([v_head,vi]),np.dot(v_head,vi))


            while abs(theta_turn) > 0.1:
                if theta_turn > 0.1:
                    robot.set_vel(-1,1)
                elif theta_turn < -0.1:
                    robot.set_vel(1,-1)

                pose_t = robot.get_pose()
                v_headx = np.cos(pose_t[2])
                v_heady = np.sin(pose_t[2])
                v_head = [v_headx, v_heady]        
                theta_turn = math.atan2(np.linalg.det([v_head,vi]),np.dot(v_head,vi))

            robot.set_vel(velocity, velocity)
            robot.delay(20)
            
        if (robot.assigned_id == 1):
            robot.set_led(0,100,0)
            radius = 0.7
            vrepx = 0.0
            vrepy = 0.0

            # Create random vector
            rand_theta = uniform(0.0,1.0)
            vrandx = np.cos(np.pi * rand_theta * 2)
            vrandy = np.sin(np.pi * rand_theta * 2)

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
                x_rep_list.append(pose_rxed[0])
                y_rep_list.append(pose_rxed[1])

            if len(x_rep_list) > rep_avg and pose_t and len(x_rep_list) % 5 == 0:
                x_center = np.average(x_rep_list[-rep_avg:])
                y_center = np.average(y_rep_list[-rep_avg:])
                dx1 = x_center- pose_t[0]
                dy1 = y_center - pose_t[1]
                dist1 = math.sqrt(dy1**2 + dx1**2)

                # Calculate repulsion vector
                if dist1 < 2*radius:
                    # calculates repulsion vector !!!!!!!!!! NEED TO INCLUDE SENSING!!!!!!!!!!!!!!!!!!
                    magnitude = -k*(2*radius - dist1)
                    vrepx = magnitude * (dx1/dist1)
                    vrepy = magnitude * (dy1/dist1)
                    # robot.set_led(100,100,100)
                else:
                    # ignores repulsion if no robots in range
                    vrepx = 0.0
                    vrepy = 0.0
            else:
                continue

            vix =  vtaxisx  + vrepx + (c_rand * vrandx)
            viy =  vtaxisy  + vrepy + (c_rand * vrandy)
            
            v_headx = np.cos(pose_t[2])
            v_heady = np.sin(pose_t[2])
            v_head = [v_headx, v_heady]
            vi = [vix, viy]
            theta_turn = math.atan2(np.linalg.det([v_head,vi]),np.dot(v_head,vi))


            while abs(theta_turn) > 0.1:
                if theta_turn > 0.1:
                    robot.set_vel(-1,1)
                elif theta_turn < -0.1:
                    robot.set_vel(1,-1)

                pose_t = robot.get_pose()
                v_headx = np.cos(pose_t[2])
                v_heady = np.sin(pose_t[2])
                v_head = [v_headx, v_heady]        
                theta_turn = math.atan2(np.linalg.det([v_head,vi]),np.dot(v_head,vi))

            robot.set_vel(velocity, velocity)
            robot.delay(20)

        if (robot.assigned_id == 2):
            robot.set_led(0,0,100)
            radius = 1.3
            vrepx = 0.0
            vrepy = 0.0

            # Create random vector
            rand_theta = uniform(0.0,1.0)
            vrandx = np.cos(np.pi * rand_theta * 2)
            vrandy = np.sin(np.pi * rand_theta * 2)

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
                x_rep_list.append(pose_rxed[0])
                y_rep_list.append(pose_rxed[1])

            if len(x_rep_list) > rep_avg and pose_t and len(x_rep_list) % 5 == 0:
                x_center = np.average(x_rep_list[-rep_avg:])
                y_center = np.average(y_rep_list[-rep_avg:])
                dx1 = x_center- pose_t[0]
                dy1 = y_center - pose_t[1]
                dist1 = math.sqrt(dy1**2 + dx1**2)

                # Calculate repulsion vector
                if dist1 < 2*radius:
                    # calculates repulsion vector !!!!!!!!!! NEED TO INCLUDE SENSING!!!!!!!!!!!!!!!!!!
                    magnitude = -k*(2*radius - dist1)
                    vrepx = magnitude * (dx1/dist1)
                    vrepy = magnitude * (dy1/dist1)
                    # robot.set_led(100,100,100)
                    print("Detected robot")
                else:
                    # ignores repulsion if no robots in range
                    vrepx = 0.0
                    vrepy = 0.0
            else:
                continue


            vix = vtaxisx  + vrepx + (c_rand * vrandx) #
            viy = vtaxisy  + vrepy + (c_rand * vrandy) #
            
            v_headx = np.cos(pose_t[2])
            v_heady = np.sin(pose_t[2])
            v_head = [v_headx, v_heady]
            vi = [vix, viy]
            theta_turn = math.atan2(np.linalg.det([v_head,vi]),np.dot(v_head,vi))

            while abs(theta_turn) > 0.1:
                if theta_turn > 0.1:
                    robot.set_vel(-1,1)
                elif theta_turn < -0.1:
                    robot.set_vel(1,-1)

                pose_t = robot.get_pose()
                v_headx = np.cos(pose_t[2])
                v_heady = np.sin(pose_t[2])
                v_head = [v_headx, v_heady]        
                theta_turn = math.atan2(np.linalg.det([v_head,vi]),np.dot(v_head,vi))

            robot.set_vel(velocity, velocity)
            robot.delay(10)