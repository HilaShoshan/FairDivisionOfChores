from general_functions import *
from numpy.random import randint

def new_point(old_a, old_b):
    """
    "Moving knife" idea, but in the discrete case
    Ascend up the line in constant jumps
    :return: the new point: (old_a-step, old_b+step)
    """
    step = 0.05  # 0.1
    a = old_a - step
    b = old_b + step
    return (a, b)


print("Division A = (A1,A2)\n")
# only one category!!!                                                                 #   a     b    chores   capacity
utilities = ((-2,-2),(-2,-2),(-2,-2),(-2,-2),(-2,-2),(-5,-5),(-3,-1),(-2,0),(0,-1))  #  0.5   0.5     9         6
# utilities = ((0,-1),(-2,-3),(-4,-6),(-10,-10))                                       #  0.6   0.4     4       2,3,4
# utilities = ((0,-1),(-2,-3),(-4,-6))                                                 #  0.6   0.4     3        3,2
# utilities = ((-1,0),(-3,-2),(-6,-4))                                                 #  0.4   0.6     3        3,2
# utilities = ((-1,-5),(-2,-10),(-3,-20))                                              #  0.85  0.15    3         2
# utilities = ((-1,-5),(-10,-2),(-3,-20))                                              #   1     0      3         2

# utilities = list(( (randint(-1000,-1),randint(-1000,-1)) for _ in range(10) ))
# print("utilities: ",utilities)

a = 1.0
b = 0.0
capacity = 6

while True:
    print("Point:", (a, b))
    G, chores = create_G(len(utilities), utilities, capacity, point=(a, b))
    matching = nx.max_weight_matching(G, maxcardinality=True)  # initial division
    A1, A2 = get_partial_divisions(matching)
    print("A1: ", A1)
    print("A2: ", A2)
    found_EF1 = False
    if isEF1(A1, A2, utilities):
        print("done :)")
        found_EF1 = True
        exit()
    # check if exists an EF1 max-matching with the same point (a,b)
    groups = divideToGroups(G, chores)  # does not depend on the matching
    for diff in groups:
        group = groups[diff]
        print("group: ", group, "diff: ", diff)
        num1, reducedA1 = how_much(A1, group)  # the number of chores agent 1 gets from this group and the allocation without these chores
        num2, reducedA2 = how_much(A2, group)  # same for 2
        print("num1, num2: ", num1, num2)
        if num1 == 0 or num1 == 1 or num1 == len(group) or num1 == len(group)-1:  # no other options
            continue
        # choose another set of size num1 each time
        for i in range(len(group)-num1+1):
            A1 = reducedA1 + group[i:i+num1]
            A2 = reducedA2 + group[0:i] + group[i+num1:]
            print("A1: ", A1)
            print("A2: ", A2)
            # check the new matching
            if isEF1(A1, A2, utilities):
                print("done :)")
                found_EF1 = True
                exit()
            break  # do the switch once
    print("__________________________________________________________")
    if found_EF1:
        exit()
    a, b = new_point(a, b)
    if a < 0:
        print("An EF1 division has not found :(")
        exit()
