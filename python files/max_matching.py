import math

import networkx as nx


def create_G(m, utilities, s, point=(1, 0), n=2):
    """
    Create G_{a,b,c} graph for general chores in each category & 2 agents
    :param m: number of chores in the current category
    :param utilities: a list of m-tuples representing the agent's utilities: {(u_11,u_21),...,(u_1m,u_2m)}
    :param s: category's capacity constraint
    :param point: (a,b) point
    :param n: number of agents
    :return: a networkx graph according to our definition
    """
    num_chores = s*2
    # num_dummy = num_chores-m
    num_agents_copies = s
    agents = ('A', 'B')
    G = nx.Graph()
    chores = []  # a list of all the chores, include dummies
    count = 0
    for x in range(n):
        for i in range(num_agents_copies):
            agent = agents[x] + str(i)
            for j in range(num_chores):
                if j < m:  # real chore
                    chore = 't' + str(j)
                    weight = utilities[j][x] * point[x]
                else:  # dummy chore
                    chore = 'd' + str(j-m)
                    weight = 0
                if x == 0 and i == 0:
                    chores.append(chore)
                G.add_edge(agent, chore, weight=weight)
                # print("added: ", agent, chore, weight)
                count += 1
    # print(count)
    return G, chores


def recognize_agent(match):
    if match[0][0] == 'A' or match[1][0] == 'A':
        return 1
    return 2


def get_chore(match):
    if match[0][0] == 't':
        return 't'+match[0][1]
    elif match[1][0] == 't':
        return 't'+match[1][1]
    elif match[0][0] == 'd':  # a dummy chore
        return 'd'+match[0][1]
    else:  # match[1][0] == 'd'
        return 'd'+match[1][1]


def get_partial_divisions(matching):
    A1 = []
    A2 = []
    for match in matching:
        agent = recognize_agent(match)
        chore = get_chore(match)
        if agent == 1:  # this is the allocation of agent 1
            A1.append(chore)
        else:  # 2's allocation
            A2.append(chore)
    return A1, A2


def isEF1(matching, utilities):
    utility1_A = 0
    utility1_B = 0
    utility2_A = 0
    utility2_B = 0
    worst1 = 0
    worst2 = 0
    for match in matching:
        agent = recognize_agent(match)
        chore = get_chore(match)
        if chore[0] == 'd':  # a dummy chore
            continue
        chore_indx = int(chore[1])
        # add the utility
        u1 = utilities[chore_indx][0]
        u2 = utilities[chore_indx][1]
        if agent == 1:  # this is the allocation of agent 1
            if u1 < worst1:  # update minimum of 1
                worst1 = u1
            utility1_A += u1
            utility2_A += u2
        else:  # 2's allocation
            if u2 < worst2:  # update minimum of 2
                worst2 = u2
            utility1_B += u1
            utility2_B += u2
    A1, A2 = get_partial_divisions(matching)
    print("A1: ", A1)
    print("A2: ", A2)
    # check EF1
    print("u1(A1): ", utility1_A, " u1(A2): ", utility1_B, " worst: ", worst1)
    print("u2(A2): ", utility2_B, " u2(A1): ", utility2_A, " worst: ", worst2)
    if utility1_A-worst1 >= utility1_B and utility2_B-worst2 >= utility2_A:
        return True
    return False


def new_point(old_a, old_b):
    """
    "Moving knife" idea, but in the discrete case
    Ascend up the line in constant jumps
    :return: the new point: (old_a-val, old_b+val)
    """
    val = 0.1
    a = old_a - val
    b = old_b + val
    return (a, b)


def divideToGroups(G, chores):
    diff_dict = {}
    for chore in chores:  # include dummy chores
        u1 = G.get_edge_data('A0', chore)['weight']
        u2 = G.get_edge_data('B0', chore)['weight']
        diff = u1-u2
        # print("chore: ", chore, " diff: ", diff)
        if diff in diff_dict:  # already exists
            diff_dict[diff] = diff_dict[diff] + [chore]  # concat the new chore
        else:
            diff_dict[diff] = [chore]
    return diff_dict


def how_much(A, group):
    """
    returns the number of chores an agent with partial allocation A gets from the given group
    """
    count = 0
    for chore in A:
        if chore in group:
            count += 1
    return count


print("Division A = (A1,A2)\n")
utilities = ((-2,-2),(-2,-2),(-2,-2),(-2,-2),(-2,-2),(-5,-5),(-3,-1),(-2,0),(0,-1))

a = 1.0
b = 0.0

while True:
    print("Point:", (a, b))
    G, chores = create_G(9, utilities, 6, point=(a, b))
    matching = nx.max_weight_matching(G, maxcardinality=True)  # initial division
    if isEF1(matching, utilities):
        break
    # check if exists an EF1 max-matching with the same point (a,b)
    groups = divideToGroups(G, chores)  # does not depend on the matching
    A1, A2 = get_partial_divisions(matching)
    for group in groups:
        # print("group: ", groups[group])
        num = how_much(A1, groups[group])  # the number of chores agent 1 gets from this group
        if num == 0 or num == 1:
            continue
        # choose another set of size num each time
        # check the new matching
        if isEF1(matching, utilities):
            break
    break
    a, b = new_point(a, b)
    if a < 0:
        print("end.")
        break
