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
    chores = []
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


def get_chore_indx(match):
    if match[0][0] == 't':
        return int(match[0][1])
    elif match[1][0] == 't':
        return int(match[1][1])
    else:  # a dummy chore
        return -1


def print_division(matching):
    A1 = []
    A2 = []
    for match in matching:
        agent = recognize_agent(match)
        chore_indx = get_chore_indx(match)
        if chore_indx == -1:  # a dummy chore
            continue
        if agent == 1:  # this is the allocation of agent 1
            A1.append("t"+str(chore_indx))
        else:  # 2's allocation
            A2.append("t"+str(chore_indx))
    # check EF1
    print("A1: ", A1)
    print("A2: ", A2)


def isEF1(matching, utilities):
    utility1_A = 0
    utility1_B = 0
    utility2_A = 0
    utility2_B = 0
    worst1 = 0
    worst2 = 0
    for match in matching:
        agent = recognize_agent(match)
        chore_indx = get_chore_indx(match)
        if chore_indx == -1:  # a dummy chore
            continue
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
    print_division(matching)
    # check EF1
    print("u1(A1): ", utility1_A, " u1(A2): ", utility1_B, " worst: ", worst1)
    print("u2(A2): ", utility2_B, " u2(A1): ", utility2_A, " worst: ", worst2)
    if utility1_A-worst1 >= utility1_B and utility2_B-worst2 >= utility2_A:
        return True
    return False


def get_ts(matching, utilities):
    min = 0
    max = -math.inf
    t_indx = -1
    t_star_indx = -1
    for match in matching:
        agent = recognize_agent(match)
        chore_indx = get_chore_indx(match)
        if chore_indx == -1:  # a dummy chore
            utility = 0
        else:
            utility = utilities[chore_indx][1]
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


def new_point(old_a, old_b):
    """
    "Moving knife" idea, but in the discrete case
    Ascend up the line in constant jumps
    :return: the new point: (old_a-val, old_b+val)
    """
    val = 0.001
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


print("Division A = (A1,A2)\n")
# utilities = ((-1,-2),(-5,-5),(-3,-1),(-2,0),(0,-1))
utilities = ((-2,-2),(-2,-2),(-2,-2),(-2,-2),(-2,-2),(-5,-5),(-3,-1),(-2,0),(0,-1))

# G = create_G(5, utilities, 4)
G, stam = create_G(9, utilities, 6)  # a=1, b=0
matching = nx.max_weight_matching(G, maxcardinality=True)  # initial division
print("Point: (1, 0)")
a = 1.0
b = 0.0

while not isEF1(matching, utilities):
    """
    # second idea --> not working
    t_indx, t_star_indx = get_ts(matching, utilities)
    print("t, t*:", t_indx, t_star_indx)
    if t_star_indx == -1:  # dummy
        u1_t_star = 0
        u2_t_star = 0
    else:
        u1_t_star = utilities[t_star_indx][0]
        u2_t_star = utilities[t_star_indx][1]
    a, b = get_point(utilities[t_indx][0], u1_t_star, utilities[t_indx][1], u2_t_star)  
    """
    print()
    a, b = new_point(a, b)  # third idea
    if a < 0:
        print("end.")
        break
    print("Point:", (a, b))
    # G = create_G(5, utilities, 4, point=(a, b))
    G, chores = create_G(9, utilities, 6, point=(a, b))
    groups = divideToGroups(G, chores)
    print("groups: ", groups)
    break
    matching = nx.max_weight_matching(G, maxcardinality=True)  # initial division
    # print(matching)



