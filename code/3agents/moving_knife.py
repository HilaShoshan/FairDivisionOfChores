""""
    3 agents
    3 items in each category
    same order of utilities 
"""""

from general_functions import *
from numpy.random import randint
import numpy as np

print("Division A = (A1,A2,A3)\n")

"""""
utilities template:

                        item 1                       item 2                       item 3
                        
category 1   [((u1(o_11), u2(o_11), u3(o_11)), (u1(o_12), u2(o_12), u3(o_12)), (u1(o_13), u2(o_13), u3(o_13))),
...
category n    ((u1(o_n1), u2(o_n1), u3(o_n1)), (u1(o_n2), u2(o_n2), u3(o_n2)), (u1(o_n3), u2(o_n3), u3(o_n3)))]
"""""

# utilities = [((-1,0,-1),(-4,-1,-1),(-5,-2,-3)),
#            ((-4,-1,0),(-5,-3,-2),(-6,-4,-6)),
#            ( (0,0,0), (-2,-6,-7),(-4,-6,-7))]


def get_category(m):
    """
    :return: a category with m items and random utilities for the 3 agents.
    """
    return list(( (randint(-(k+1)*100, -k*100), randint(-(k+1)*100, -k*100), randint(-(k+1)*100, -k*100)) for k in range(m) ))


utilities = [get_category(3), get_category(3), get_category(3)]
print("utilities: ", utilities)
capacities = (1, 1, 1)

w1 = 1.0
w2 = 0.0
w3 = 0.0

step = 0.05

done = False
for w3 in np.arange(0, 1, step):
    for w2 in np.arange(0, 1-w3, step):
        w1 = 1-w2-w3
        if w1 < 0:
            print("An EF1 division has not found.")
            exit()
        print("point: ", (w1, w2, w3))
        G = create_G(utilities, capacities, (w1, w2, w3))
        matching = nx.max_weight_matching(G, maxcardinality=True)
        A1, A2, A3 = get_allocations(matching)
        print("A1: ", A1)
        print("A2: ", A2)
        print("A3: ", A3)
        if isEF1(A1, A2, A3, utilities):
            print("done!!!!!!!!!!!!!!!")
            done = True
            # break
        print("_______________________________________")
    # if done:
        # break