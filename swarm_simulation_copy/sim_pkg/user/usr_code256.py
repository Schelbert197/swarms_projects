import struct
import math
import numpy as np


def usr(robot):
    hop_countl = 300
    hop_countr = 300
    r = 0
    g = 0
    b = 0
    starting_err = 1000.0
    x = 0.0
    y = 0.0

    smoothing = True

    ###### The below code was my first attempt at a hopcount grid. I have kept it for reference but use the code below ######
    # while True:
    #     robot.delay(10)
    #     if robot.assigned_id==1:
    #         msg=struct.pack('ffii',0.0,0.0,0,15)
    #         robot.send_msg(msg)
    #         robot.set_led(0,0,100)
    #     elif robot.assigned_id==2:
    #         msg=struct.pack('ffii',0.0,15.0,15,0)
    #         robot.send_msg(msg)
    #         robot.set_led(0,100,100)
    #     else:
    #         msgs = robot.recv_msg()
    #         if len(msgs) > 0:
    #             for i in range(len(msgs)):
    #                 test=struct.unpack('ffii',msgs[i][:16])
    #                 print(test)
    #                 c_hopl = test[3] + 1
    #                 c_hopr = test[2] + 1
    #                 if c_hopl < hop_countl:
    #                     hop_countl = c_hopl
    #                     if hop_countl%2 == 1:
    #                         r = 100
    #                 elif c_hopr < hop_countr:
    #                     hop_countr = c_hopr
    #                     if hop_countr%2 == 1:
    #                         g = 100
    while True:
        robot.delay(10)
        if robot.assigned_id == 1:
            msg = struct.pack('ffii', 0.0, 0.0, 0, 0)
            robot.send_msg(msg)
            robot.set_led(0, 0, 100)
        elif robot.assigned_id == 2:
            msg = struct.pack('ffii', 0.0, 15.0, 15, 0)
            robot.send_msg(msg)
            robot.set_led(0, 100, 100)
        else:
            msgs = robot.recv_msg()
            if len(msgs) > 0:
                for i in range(len(msgs)):
                    test = struct.unpack('ffii', msgs[i][:16])
                    print(test)
                    if test[2] == 0:
                        c_hopr = test[3] + 1
                        if test[3] < hop_countr:
                            hop_countr = c_hopr
                            msg = struct.pack('ffii', x, y, 0, hop_countr)
                            robot.send_msg(msg)  # send pose x,y in message
                    else:
                        c_hopl = test[3] + 1
                        if test[3] < hop_countl:
                            hop_countl = c_hopl
                            msg = struct.pack('ffii', x, y, 15, hop_countl)
                            robot.send_msg(msg)  # send pose x,y in message

                # Code to view the hop count gradients propogating (commented out since it was used in interim)
                # light up based on mod hopcount
                # if hop_countl%2 == 0 and hop_countr%2 == 0:
                #     robot.set_led(0,0,0)
                # elif hop_countl%2 == 0 and hop_countr%2 == 1:
                #     robot.set_led(0,g,0)
                # elif hop_countl%2 == 1 and hop_countr%2 == 0:
                #     robot.set_led(r,0,0)
                # else:
                #     robot.set_led(r,g,0)

                # Coordinate Creation
                for j in range(0, 15):
                    for k in range(0, 15):
                        # Not sure which if either pair works better
                        distr = math.dist([j, k], [0, 0])
                        distl = math.dist([j, k], [0, 15])
                        # distr = math.sqrt((0-j)**2 + (0-k)**2)
                        # distl = math.sqrt((0-j)**2 + (15-k)**2)

                        err = (distr-hop_countr)**2 + (distl-hop_countl)**2
                        if err < starting_err:
                            starting_err = err
                            x = float(j)
                            y = float(k)

                if smoothing == True:
                    # This should smooth for each message that comes in one at a time and add
                    # the average to the total. It seems to push the middle regions towards the edge
                    # and does not converge...maybe because it uses just two robots per message.
                    if 1 < test[1] <= 15.0 and 1 < test[0] <= 15.0:
                        avex = (test[0] + x)/2 - 0.5
                        avey = (test[1] + y)/2 - 0.5

                        x = x + 0.2 * avex
                        y = x + 0.2 * avey
                        msg = struct.pack('ffii', x, y, 15, hop_countl)

                if 4.0 < x < 12.0 and y < (12 - 1.2 * x):
                    robot.set_led(0, 0, 0)
                elif 4.0 < x < 11.0 and y > (20 - 1.2 * x):
                    robot.set_led(0, 0, 0)
                else:
                    robot.set_led(100, 0, 100)
