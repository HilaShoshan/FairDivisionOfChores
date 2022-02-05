from general_functions import *


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
utilities = (((-1,-5),(-10,-2),(-3,-20)),((0,-1),(-2,-3),(-4,-6),(-10,-10)))
capacities = (2, 2)

a = 1.0
b = 0.0

while True:
    print("Point:", (a, b))
    A1 = []
    A2 = []
    Graphs = []
    Chores = []
    for c in range(len(utilities)):
        category = utilities[c]
        G, chores = create_G(c, category, capacities[c], point=(a, b))
        Graphs.append(G)
        Chores.append(chores)  # add the chores from the current category
        matching = nx.max_weight_matching(G, maxcardinality=True)  # initial division
        partialA1, partialA2 = get_partial_divisions(matching)  # the allocations in the current category (c)
        A1.append(partialA1)
        A2.append(partialA2)
    print("A1: ", A1)
    print("A2: ", A2)
    if isEF1(A1, A2, utilities):  # need to fix it!!!!
        print("done :)")
        exit()
    # check if exists an EF1 max-matching with the same point (a,b), for each category
    for c in range(len(utilities)):
        groups = divideToGroups(Graphs[c], Chores[c])  # does not depend on the matching
        for diff in groups:
            group = groups[diff]
            num1, reducedA1 = how_much(A1[c], group)  # the number of chores agent 1 gets from this group and the allocation without these chores
            num2, reducedA2 = how_much(A2[c], group)  # same for 2
            if num1 == 0 or num1 == len(group):  # no other options
                continue
            # choose another set of size num1 each time
            for i in range(len(group)-num1+1):
                partialA1 = reducedA1 + group[i:i+num1]
                partialA2 = reducedA2 + group[0:i] + group[i+num1:]
                A1[c] = partialA1
                A2[c] = partialA2
                print("A1: ", A1)
                print("A2: ", A2)
                # check the new matching
                if isEF1(A1, A2, utilities):
                    print("done :)")
                exit()
    print("__________________________________________________________")
    a, b = new_point(a, b)
    if a < 0:
        print("An EF1 division has not found :(")
        exit()
