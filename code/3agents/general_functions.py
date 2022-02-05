import numpy as np
import networkx as nx

epsilon = 0.0001  # to solve numeric problems


def create_G(utilities, capacities, point=(1, 0, 0), n=3):
    G = nx.Graph()
    for c in range(len(utilities)):  # for each category
        category = utilities[c]
        for j in range(len(category)):
            item = "o_" + str(c) + "," + str(j)
            for i in range(n):
                weight = utilities[c][j][i] * point[i]
                agent = "Agent_" + str(i) + "_" + str(c)
                G.add_edge(agent, item, weight=weight)
                # print("(", agent, ",", item, ") added with weight ", weight)
    return G


def recognize_agent_and_item(match):
    if match[0].split("_")[0] == "o":  # the first index is the item
        item = match[0]
        agent = int(match[1].split("_")[1])
    else:  # the second is the item
        item = match[1]
        agent = int(match[0].split("_")[1])
    return agent, item


def get_allocations(matching):
    A1 = []
    A2 = []
    A3 = []
    for match in matching:
        agent, item = recognize_agent_and_item(match)
        if agent == 0:  # this is the allocation of agent 1
            A1.append(item)
        elif agent == 1:  # 2's allocation
            A2.append(item)
        else:  # 3's allocation
            A3.append(item)
    return A1, A2, A3


def map_to_utilities(A, utilities):
    """
    map the given partial division, A, to utilities lists
    @:param A: a list of lists representing what the agent get from each category
    :return: u1 - a list that contains the utility values on agent 1's eyes of each item in A
             u2 - similar to agent 2
             u3 - similar to agent 3
    """
    u1 = []
    u2 = []
    u3 = []
    for item in A:
        category_indx = int(item.split("_")[1].split(",")[0])
        item_indx = int(item.split("_")[1].split(",")[1])
        u1.append(utilities[category_indx][item_indx][0])
        u2.append(utilities[category_indx][item_indx][1])
        u3.append(utilities[category_indx][item_indx][2])
    return u1, u2, u3


def isEF1(A1, A2, A3, utilities):
    u1A1_lst, u2A1_lst, u3A1_lst = map_to_utilities(A1, utilities)
    u1A2_lst, u2A2_lst, u3A2_lst = map_to_utilities(A2, utilities)
    u1A3_lst, u2A3_lst, u3A3_lst = map_to_utilities(A3, utilities)
    # the worst chores in each allocation
    worst1 = min(u1A1_lst)
    worst2 = min(u2A2_lst)
    worst3 = min(u3A3_lst)
    # the best goods in each other agent's allocation
    best1in2 = max(u1A2_lst)
    best1in3 = max(u1A3_lst)
    best2in1 = max(u2A1_lst)
    best2in3 = max(u2A3_lst)
    best3in1 = max(u3A1_lst)
    best3in2 = max(u3A2_lst)
    # check EF1
    u1A1 = sum(u1A1_lst)
    u2A1 = sum(u2A1_lst)
    u3A1 = sum(u3A1_lst)
    u1A2 = sum(u1A2_lst)
    u2A2 = sum(u2A2_lst)
    u3A2 = sum(u3A2_lst)
    u1A3 = sum(u1A3_lst)
    u2A3 = sum(u2A3_lst)
    u3A3 = sum(u3A3_lst)
    if u1A1-worst1 >= u1A2 or u1A1 >= u1A2-best1in2 \
        and \
        u1A1-worst1 >= u1A3 or u1A1 >= u1A3-best1in3 \
        and \
        u2A2-worst2 >= u2A1 or u2A2 >= u2A1-best2in1 \
        and \
        u2A2-worst2 >= u2A3 or u2A2 >= u2A3-best2in3 \
        and \
        u3A3-worst3 >= u3A1 or u3A3 >= u3A1-best3in1 \
        and \
        u3A3-worst3 >= u3A2 or u3A3 >= u3A2-best3in2:
        return True
    return False