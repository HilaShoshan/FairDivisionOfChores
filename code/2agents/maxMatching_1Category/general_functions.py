import numpy as np
import networkx as nx

epsilon = 0.0001  # to solve numeric problems


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
            u1.append(0)
            u2.append(0)
            continue
        chore_indx = int(chore[1:])
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


def divideToGroups(G, chores):
    """
    returns a dictionary with u1-u2 differential as keys, and groups of all the chores
    with this differential value as values.
    each group of chores is sorted by the utility value (from the best chore to the worst)
    """
    diff_dict = {}
    values_dict = {}  # saves the utility values by agent 1 for each group (in the same order)
    for chore in chores:  # include dummy chores
        u1 = G.get_edge_data('A0', chore)['weight']
        u2 = G.get_edge_data('B0', chore)['weight']
        diff = u1-u2
        # print("chore: ", chore, " diff: ", diff)
        flag = False
        for key in diff_dict:
            if key-epsilon <= diff <= key+epsilon:
                diff_dict[key] = diff_dict[key] + [chore]  # concat the new chore to the group
                values_dict[key] = values_dict[key] + [u1]
                flag = True
        if not flag:  # we haven't add the new chore to the dict yet
            diff_dict[diff] = [chore]
            values_dict[diff] = [u1]
    # sort each group in diff_dict from the best chore to the worst one
    for diff in diff_dict:
        group = diff_dict[diff]
        vals = np.array(values_dict[diff])
        indices = (-vals).argsort()  # get the indices on the right order
        diff_dict[diff] = [group[index] for index in indices]
    return diff_dict


def how_much(A, group):
    """
    returns the number of chores an agent with partial allocation A gets from the given group
    and A without these chores
    """
    reduced = A.copy()
    count = 0
    for chore in A:
        if chore in group:
            count += 1
            reduced.remove(chore)
    return count, reduced

