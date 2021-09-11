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
                G.add_edge(agent, chore, weight=weight)
                # print("added: ", agent, chore, weight)
                count += 1
    # print(count)
    return G


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


def isEF1(matching, utilities):
    utility1 = 0
    utility2 = 0
    worst1 = 0
    worst2 = 0
    for match in matching:
        agent = recognize_agent(match)
        chore_indx = get_chore_indx(match)
        if chore_indx == -1:  # a dummy chore
            continue
        # add the utility
        if agent == 1:
            utility = utilities[chore_indx][0]
            if utility < worst1:  # update minimum
                worst1 = utility
            utility1 += utility
        else:
            utility = utilities[chore_indx][1]
            if utility < worst2:
                worst2 = utility
            utility2 += utility
    # check EF1
    if utility1-worst1 >= utility2 and utility2-worst2 >= utility1:
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


utilities = ((-1,-2),(-5,-5),(-3,-1),(-2,0),(0,-1))

G = create_G(5, utilities, 4)
nx.max_weight_matching(G, maxcardinality=True)
matching = nx.max_weight_matching(G, maxcardinality=True)  # initial division
print(matching)

while not isEF1(matching, utilities):
    t_indx, t_star_indx = get_ts(matching, utilities)
    print("t, t*:", t_indx, t_star_indx)
    if t_star_indx == -1:  # dummy
        u1_t_star = 0
        u2_t_star = 0
    else:
        u1_t_star = utilities[t_star_indx][0]
        u2_t_star = utilities[t_star_indx][1]
    a, b = get_point(utilities[t_indx][0], u1_t_star, utilities[t_indx][1], u2_t_star)
    print("a, b:", a, b)
    G = create_G(5, utilities, 4, point=(a, b))
    nx.max_weight_matching(G, maxcardinality=True)
    matching = nx.max_weight_matching(G, maxcardinality=True)  # initial division
    print(matching)



