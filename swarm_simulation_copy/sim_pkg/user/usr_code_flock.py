"""Srikanth Schelbert ME 409 Lab 4 usr_code.py"""


def usr(robot):
    import struct
    import math
    from random import uniform
    import numpy as np
    import modern_robotics

    # adding a commment
    rep_avg = 2
    velocities = [10, 10]
    x_neighbor_list = []
    y_neighbor_list = []
    th_neighbor_list = []
    bot_radius = 0.2
    k = 10.0
    # motor_full_speed = 180  # rpm -100,100 set vel
    # set_vel_to_rads = (9/5) * (np.pi/60)
    # half_radius_of_wheel = 0.0075
    # wheel_rad = 2*half_radius_of_wheel
    # dist_between_wheel = 0.08
    postions = {0: [0, 0],
                1: [0, 0],
                2: [0, 0],
                3: [0, 0],
                4: [0, 0],
                5: [0, 0],
                6: [0, 0],
                7: [0, 0],
                8: [0, 0],
                9: [0, 0]}
    # COM = [0.0, 0.0]
    while True:
        """Note for grader:
        The robots are able to exhibit decent flocking behavior though
        depending on the run, they have 1 of two issues. 
        1) the repulsion isn't enough and they get stuck which throws off
        their heading.
        2) they don't receive frequent enough messages and are unable to
        update heading.
        When these issues are minimal, they can move as a cohesive flock
        using their centering, repulsion, cohesion, and average heading
        vectors.

        I also added a multiplier to the center force so that they were
        less likely to get stuck on the wall outside of a certain 
        boundary."""

        # wheel set vel in rpm = 9/5
        # wheel rad/s = rpm * (1/60) * (2pirad/rev)
        # wheel rad/s = (9/5) * (2pi/60) * set vel

        robot.set_led(0, 90, 70)
        # F = np.array([[-1/dist_between_wheel, 1/dist_between_wheel],
        #               [0.5, 0.5],
        #               [0.0, 0.0]])

        # V_twist = F@velocities
        # # print(f"Vtwist: {V_twist}")
        robot.delay(10)
        pose_t = robot.get_pose()
        # if there is a new postion sensor update, print out and transmit the info
        if pose_t:  # check pose is valid before using then send x, y, theta
            robot.send_msg(struct.pack('ffif', round(
                pose_t[0], 4), round(pose_t[1], 4), robot.assigned_id, pose_t[2]))

            # Create the taxis vector
            # norm = math.sqrt(pose_t[0]**2 + pose_t[1]**2)
            vtaxisx = (0.0 - pose_t[0])/5
            vtaxisy = (0.0 - pose_t[1])/5

            # Strengthen force if too close to wall
            if pose_t[0] > 3.5:
                vtaxisx = vtaxisx * 1.5
            if pose_t[1] > 3.5:
                vtaxisy = vtaxisy * 1.5

            postions[robot.assigned_id] = [pose_t[0], pose_t[1]]

        # gets message from nearby robot to see if it is within vision range and radius.
        msgs = robot.recv_msg()
        if len(msgs) > 5:
            pose_rxed = struct.unpack('ffif', msgs[-1][:16])
            postions[pose_rxed[2]] = [pose_rxed[0], pose_rxed[1]]
            x_neighbor_list.append(pose_rxed[0])
            y_neighbor_list.append(pose_rxed[1])
            th_neighbor_list.append(pose_rxed[3])
            # collect positions of all robots and get cohesion vector

        # # Calculate the center of mass based on a running position dict
        # xlist = []
        # ylist = []
        # for i in range(0, 10):
        #     if postions[i] is not [0, 0]:
        #         xlist.append(postions[i][0])
        #         ylist.append(postions[i][1])
        # COM = [np.average(xlist), np.average(ylist)]
        # # Create the taxis vector
        # norm = math.sqrt(COM[0]**2 + COM[1]**2)
        # vcomx = (0.0 - COM[0])/norm
        # vcomy = (0.0 - COM[1])/norm

        # Average velocity vec of all robots
        vcohy = 0.0
        vcohx = 0.0
        if len(x_neighbor_list) > rep_avg and pose_t and len(x_neighbor_list) % 5 == 0:
            x_center = np.average(x_neighbor_list[-rep_avg:])
            y_center = np.average(y_neighbor_list[-rep_avg:])
            dx1 = x_center - pose_t[0]
            dy1 = y_center - pose_t[1]
            dist1 = math.sqrt(dy1**2 + dx1**2)

            # Calculate cohesion vector
            magnitude_c = 1.3  # -k*(2*bot_radius - dist1)
            vcohx = magnitude_c * (dx1/dist1)
            vcohy = magnitude_c * (dy1/dist1)
            # robot.set_led(100,100,100)

        # Normalized repulsion vector of each robot from dist
        vrepx = 0.0
        vrepy = 0.0
        if len(x_neighbor_list) > rep_avg and pose_t:
            x_neigh = np.average(x_neighbor_list[-2:])
            y_neigh = np.average(y_neighbor_list[-2:])
            dx2 = x_neigh - pose_t[0]
            dy2 = y_neigh - pose_t[1]
            dist2 = math.sqrt(dy2**2 + dx2**2)

            # Calculate repulsion vector
            if dist2 < 2*bot_radius:
                # calculates repulsion vector !!!!!!!!!! NEED TO INCLUDE SENSING!!!!!!!!!!!!!!!!!!
                magnitude = -k*(2*bot_radius - dist2)
                vrepx = magnitude * (dx2/dist2)
                vrepy = magnitude * (dy2/dist2)
                # robot.set_led(100,100,100)
            else:
                # ignores repulsion if no robots in range
                vrepx = 0.0
                vrepy = 0.0

        # get average heading of robot for alignment vector
        if th_neighbor_list:
            vavgx = np.cos(np.average(th_neighbor_list[-6:]))
            vavgy = np.sin(np.average(th_neighbor_list[-6:]))
        else:
            vavgx = 0.0
            vavgy = 0.0

        # Get total vector sum
        vix = vtaxisx + vavgx + vcohx + vrepx  # + vcomx
        viy = vtaxisy + vavgy + vcohy + vrepy  # + vcomy

        # Have robot align
        v_headx = np.cos(pose_t[2])
        v_heady = np.sin(pose_t[2])
        v_head = [v_headx, v_heady]
        vi = [vix, viy]
        theta_turn = math.atan2(np.linalg.det(
            [v_head, vi]), np.dot(v_head, vi))

        while abs(theta_turn) > 0.15:
            if theta_turn > 0.1:
                robot.set_vel(-1, 1)
            elif theta_turn < -0.1:
                robot.set_vel(1, -1)

            pose_t = robot.get_pose()
            v_headx = np.cos(pose_t[2])
            v_heady = np.sin(pose_t[2])
            v_head = [v_headx, v_heady]
            theta_turn = math.atan2(np.linalg.det(
                [v_head, vi]), np.dot(v_head, vi))

        robot.set_vel(velocities[0], velocities[1])
