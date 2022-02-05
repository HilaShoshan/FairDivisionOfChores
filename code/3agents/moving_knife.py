""""
    3 agents
    3 items in each category
    same order of utilities
"""""

from general_functions import *

print("Division A = (A1,A2,A3)\n")

"""""
utilities template:

                        item 1                       item 2                       item 3
                        
category 1   [((u1(o_11), u2(o_11), u3(o_11)), (u1(o_12), u2(o_12), u3(o_12)), (u1(o_13), u2(o_13), u3(o_13)))
...
category n    ((u1(o_n1), u2(o_n1), u3(o_n1)), (u1(o_n2), u2(o_n2), u3(o_n2)), (u1(o_n3), u2(o_n3), u3(o_n3)))]
"""""

utilities = [((-1,0,-1),(-5,-3,-2),(-5,-4,-3)),
             ((-4,-1,0),(-5,-3,-2),(-6,-4,-6)),
             ((0,0,0),(-2,-6,-7),(-4,-9,-9))]
capacities = (1,1,1)

w1 = 1.0
w2 = 0.0
w3 = 0.0

step = 0.05

done = False
while w3 <= 1.0:
    while w2 <= 1-w3:
        w1 = 1-w2-w3
        print("point: ", (w1,w2,w3))
        G = create_G(utilities, capacities, (w1,w2,w3))
        matching = nx.max_weight_matching(G, maxcardinality=True)
        A1, A2, A3 = get_allocations(matching)
        print("A1: ", A1)
        print("A2: ", A2)
        print("A3: ", A3)
        print("_________________________")
        if isEF1(A1, A2, A3, utilities):
            print("done")
            done = True
            break
        w2 += step
    if done:
        break
    w3 += step