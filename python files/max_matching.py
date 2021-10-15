import math
import numpy as np
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


def map_to_utilities(A, utilities):
    """
    map the given partial division, A, to utilities lists
    :return: u1 - a list that contains the utility values on agent 1's eyes of each chore in A
             u2 - similar to agent 2
    """
    u1 = []
    u2 = []
    for chore in A:
        if chore[0] == 'd':  # a dummy chore
            continue
        chore_indx = int(chore[1])
        # add chore's utility
        u1.append(utilities[chore_indx][0])
        u2.append(utilities[chore_indx][1])
    return u1, u2


def isEF1(A1, A2, utilities):
    u1A1_lst, u2A1_lst = map_to_utilities(A1, utilities)
    u1A2_lst, u2A2_lst = map_to_utilities(A2, utilities)
    worst1 = min(u1A1_lst)
    worst2 = min(u2A2_lst)
    # check EF1
    u1A1 = sum(u1A1_lst)
    u2A1 = sum(u2A1_lst)
    u1A2 = sum(u1A2_lst)
    u2A2 = sum(u2A2_lst)
    print("u1(A1): ", u1A1, " u1(A2): ", u1A2, " worst: ", worst1)
    print("u2(A2): ", u2A2, " u2(A1): ", u2A1, " worst: ", worst2)
    if u1A1-worst1 >= u1A2 and u2A2-worst2 >= u2A1:
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
    values_dict = {}  # saves the utility values for each group (in the same order)
    for chore in chores:  # include dummy chores
        u1 = G.get_edge_data('A0', chore)['weight']
        u2 = G.get_edge_data('B0', chore)['weight']
        diff = u1-u2
        # print("chore: ", chore, " diff: ", diff)
        if diff in diff_dict:  # already exists
            diff_dict[diff] = diff_dict[diff] + [chore]  # concat the new chore
            values_dict[diff] = values_dict[diff] + u1
        else:
            diff_dict[diff] = [chore]
            values_dict[diff] = u1
    return diff_dict, values_dict


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
    A1, A2 = get_partial_divisions(matching)
    print("A1: ", A1)
    print("A2: ", A2)
    if isEF1(A1, A2, utilities):
        break
    # check if exists an EF1 max-matching with the same point (a,b)
    groups, vals_dict = divideToGroups(G, chores)  # does not depend on the matching
    for diff in groups:
        group = groups[diff]
        num = how_much(A1, group)  # the number of chores agent 1 gets from this group
        if num == 0 or num == 1:
            continue
        vals = np.array(vals_dict[diff])
        indices = (-vals).argsort()[:num]  # get 'num' maximum indices of vals
        best = [group[index] for index in indices]
        # choose another set of size num each time
        # check the new matching
        if isEF1(A1, A2, utilities):
            break
    break
    a, b = new_point(a, b)
    if a < 0:
        print("end.")
        break
