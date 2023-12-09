'''
Firefly

Function to initialize agent's poses.
Input:
    swarmsize --  swarmsize.
    x -- An array to store  agents' x positions, the length of this array is the same as swarmsize
    y -- An array to store agents' y positions, the length of this array is the same as swarmsize
    theta -- An array to store agents' orientations, the length of this is the same as swarmsize

Usage:
    Usr can configure an agent's initial x, y, theta by modifying the value of the corresponding element in array x, y, and theta.
    For example, initialize agent 0's pose to x = 0, y = 1, theta = 2:
    x[0] = 0
    y[0] = 1
    theta[0] = 2

Constraints to be considered:
    x -- the value should range between -2.5 to 2.5.
    y -- the value should range between -1.5 to 1.5.
    theta -- the value should range between -pi to pi.

    The minimal pairwise inter-agent distance should be greater than 0.12

def init(swarmsize, x, y, theta, a_ids):
    import math
    import random
    for i in range(swarmsize):
        x[i] = (i % 16 ) * 0.11-1
        y[i] = (i / 16 ) * 0.11-1
        a_ids[i] = 0
        theta[i] = 0
        if i==0:
            a_ids[i]=1
        elif i==15:
            a_ids[i]=2
    pass
# '''
# def init(swarmsize, x, y, theta, a_ids):
#     import math
#     import random

#     for i in range(swarmsize):
#         x[i] = random.uniform(-4, 4)
#         y[i] = random.uniform(-4, 4)
#         a_ids[i] = i
#         theta[i] = random.uniform(-math.pi, math.pi)
#         if i%3==0:
#             a_ids[i]=0
#         elif i%3==1:
#             a_ids[i]=1
#         else:
#             a_ids[i]=2

#     return x, y, theta, a_ids


# def init(swarmsize, x, y, theta, a_ids):
#     import math
#     import random

#     for i in range(swarmsize):
#         x[i] = random.uniform(-4, 4)
#         y[i] = random.uniform(-4, 4)
#         a_ids[i] = i
#         theta[i] = random.uniform(-math.pi, math.pi)
#         if i % 2 == 0:
#             a_ids[i] = 0
#         else:
#             a_ids[i] = 1


#     return x, y, theta, a_ids

def init(swarmsize, x, y, theta, a_ids):
    import math
    import random

    for i in range(swarmsize):
        x[i] = random.uniform(-4, 4)
        y[i] = random.uniform(-4, 4)
        a_ids[i] = i
        theta[i] = random.uniform(-math.pi, math.pi)

    return x, y, theta, a_ids


# def init(swarmsize, x, y, theta, a_ids):
#     x[0] = 0
#     y[0] = -0.3
#     theta[0] = 1.5
#     a_ids[0]=0
#     x[1] = 0
#     y[1] = .3
#     theta[1] = 0
#     a_ids[1]=1
#     return x, y, theta, a_ids
'''
Firefly

Function to initialize agent's poses.
Input:
    swarmsize --  swarmsize.
    x -- An array to store  agents' x positions, the length of this array is the same as swarmsize
    y -- An array to store agents' y positions, the length of this array is the same as swarmsize
    theta -- An array to store agents' orientations, the length of this is the same as swarmsize

Usage:
    Usr can configure an agent's initial x, y, theta by modifying the value of the corresponding element in array x, y, and theta.
    For example, initialize agent 0's pose to x = 0, y = 1, theta = 2:
    x[0] = 0
    y[0] = 1
    theta[0] = 2

Constraints to be considered:
    x -- the value should range between -2.5 to 2.5.
    y -- the value should range between -1.5 to 1.5.
    theta -- the value should range between -pi to pi.

    The minimal pairwise inter-agent distance should be greater than 0.12

def init(swarmsize, x, y, theta, a_ids):
    import math
    import random
    for i in range(swarmsize):
        x[i] = (i % 16 ) * 0.11-1
        y[i] = (i / 16 ) * 0.11-1
        a_ids[i] = 0
        theta[i] = 0
        if i==0:
            a_ids[i]=1
        elif i==15:
            a_ids[i]=2
    pass
'''
# def init(swarmsize, x, y, theta, a_ids):
#     # Init for brazil nut
#     import math
#     spacey=0.5

#     spacex=0.5
#     import random
#     for i in range(swarmsize):
#         y[i] = (i % 10 ) * spacey-5*spacey
#         x[i] = math.floor(i / 10 ) * spacex-5*spacex
#         if x[i] == 0 and y[i] == 0:
#             x[i] = 0.002
#         a_ids[i] = 0
#         theta[i] = 0
#         if i%3 == 0:
#             a_ids[i]=0
#         elif i%3 == 1:
#             a_ids[i]=1
#         else:
#             a_ids[i]=2


#     return x, y, theta, a_ids
