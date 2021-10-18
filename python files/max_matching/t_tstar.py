from general_functions import *
import math


def get_ts(matching, utilities):
    min = 0
    max = -math.inf
    t_indx = -1
    t_star_indx = -1
    for match in matching:
        agent = recognize_agent(match)
        chore = get_chore(match)
        if chore[0] == 'd':  # a dummy chore
            chore_indx = -1
            utility = 0
        else:
            chore_indx = int(chore[1:])
            utility = utilities[chore_indx][agent-1]
        if agent == 1:  # it's a matching to 1
            if utility > max:
                max = utility
                t_star_indx = chore_indx
        else:
            if utility < min:
                min = utility
                t_indx = chore_indx
    # if t_star_indx == -math.inf  # 1 got just dummy chores ??
    return t_indx, t_star_indx


def get_point(u1_t, u1_t_star, u2_t, u2_t_star):
    x = u1_t - u1_t_star
    y = u2_t - u2_t_star
    a = y / (x+y)
    return (a, 1-a)


print("Division A = (A1,A2)\n")
# utilities = ((-2,-2),(-2,-2),(-2,-2),(-2,-2),(-2,-2),(-5,-5),(-3,-1),(-2,0),(0,-1))
utilities = ((-1,-5),(-2,-10),(-3,-20))
a = 1.0
b = 0.0

while True:
    print("Point:", (a, b))
    # G, chores = create_G(9, utilities, 6, point=(a, b))
    G, chores = create_G(3, utilities, 2, point=(a, b))
    matching = nx.max_weight_matching(G, maxcardinality=True)  # initial division
    A1, A2 = get_partial_divisions(matching)
    print("A1: ", A1)
    print("A2: ", A2)
    if isEF1(A1, A2, utilities):
        print("done :)")
        exit()
    # check if exists an EF1 max-matching with the same point (a,b)
    groups = divideToGroups(G, chores)  # does not depend on the matching
    for diff in groups:
        group = groups[diff]
        num1, reducedA1 = how_much(A1, group)  # the number of chores agent 1 gets from this group and the allocation without these chores
        num2, reducedA2 = how_much(A2, group)  # same for 2
        # print("num1, num2: ", num1, num2)
        if num1 == 0 or num1 == 1 or num1 == len(group) or num1 == len(group)-1:  # no other options
            continue
        # choose another set of size num1 each time
        for i in range(len(group)-num1):
            A1 = reducedA1 + group[i:i+num1]
            A2 = reducedA2 + group[0:i] + group[i+num1:]
            print("A1: ", A1)
            print("A2: ", A2)
            # check the new matching
            if isEF1(A1, A2, utilities):
                print("done :)")
                exit()
    print("__________________________________________________________")
    t_indx, t_star_indx = get_ts(matching, utilities)
    print("t, t*:", t_indx, t_star_indx)
    if t_star_indx == -1:  # dummy
        u1_t_star = 0
        u2_t_star = 0
    else:
        u1_t_star = utilities[t_star_indx][0]
        u2_t_star = utilities[t_star_indx][1]
    a, b = get_point(utilities[t_indx][0], u1_t_star, utilities[t_indx][1], u2_t_star)
    if a < 0:
        print("An EF1 division has not found :(")
        exit()
