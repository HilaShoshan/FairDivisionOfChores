import networkx as nx
from tabulate import tabulate


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


def isEF(first, second):
    if first >= second:
        return True
    return False


def isEF1_two(first, second, worst, best, i, j):
    """
    :param first: some agent's utility on his bundle
    :param second: first's utility on other agent's bundle
    :param worst: the worst chore in first's bundle (in his eyes)
    :param best: the best good in second's bundle (in the first's eyes)
    :return: true if the first envious the second up to one item
    """
    if first-worst >= second or first >= second-best:
        # print(i + " envious " + j + " up to one item :)")
        return True
    # print(i + " envious " + j + " a lot :(")
    return False


def isEF1(A1, A2, A3, utilities, ax, w1, w2, w3, colors_dict):
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
    """
    print(tabulate([['u1', u1A1, u1A2, u1A3, worst1],
                    ['u2', u2A1, u2A2, u2A3, worst2],
                    ['u3', u3A1, u3A2, u3A3, worst3]],
                   headers=['', 'A1', 'A2', 'A3', 'worst']))
    print("_______________________________________")
    """
    ans = True
    if not isEF1_two(u1A1, u1A2, worst1, best1in2, "1", "2"):
        ans = False
    if not isEF1_two(u1A1, u1A3, worst1, best1in3, "1", "3"):
        ans = False
    if not isEF1_two(u2A2, u2A1, worst2, best2in1, "2", "1"):
        ans = False
    if not isEF1_two(u2A2, u2A3, worst2, best2in3, "2", "3"):
        ans = False
    if not isEF1_two(u3A3, u3A1, worst3, best3in1, "3", "1"):
        ans = False
    if not isEF1_two(u3A3, u3A2, worst3, best3in2, "3", "2"):
        ans = False

    # draw a point
    """
    if -epsilon < w3 < epsilon:  # we are on the edge (1,2)
        if isEF(u1A1, u1A2) and isEF(u1A1, u1A3):  # agent 1 is not envy
            ax.plot(w1, w2, w3, "or", markersize=2, color=colors_dict[1])
        elif isEF(u2A2, u2A1) and isEF(u2A2, u2A3):  # agent 2 is not envy
            ax.plot(w1, w2, w3, "or", markersize=2, color=colors_dict[2])
    elif -epsilon < w2 < epsilon:  # we are on edge (1,3)
        if isEF(u1A1, u1A2) and isEF(u1A1, u1A3):  # agent 1 is not envy
            ax.plot(w1, w2, w3, "or", markersize=2, color=colors_dict[1])
        elif isEF(u3A3, u3A1) and isEF(u3A3, u3A2):  # agent 3 is not envy
            ax.plot(w1, w2, w3, "or", markersize=2, color=colors_dict[3])
    elif -epsilon < w1 < epsilon:  # we are on edge (2,3)
        if isEF(u2A2, u2A1) and isEF(u2A2, u2A3):  # agent 2 is not envy
            ax.plot(w1, w2, w3, "or", markersize=2, color=colors_dict[2])
        elif isEF(u3A3, u3A1) and isEF(u3A3, u3A2):  # agent 3 is not envy
            ax.plot(w1, w2, w3, "or", markersize=2, color=colors_dict[3])
    else:  # we are inside the triangle
        if isEF(u1A1, u1A2) and isEF(u1A1, u1A3):  # agent 1 is not envy
            ax.plot(w1, w2, w3, "or", markersize=2, color=colors_dict[1])
        elif isEF(u2A2, u2A1) and isEF(u2A2, u2A3):  # agent 2 is not envy
            ax.plot(w1, w2, w3, "or", markersize=2, color=colors_dict[2])
        else:  # agent 3 is not envy
            ax.plot(w1, w2, w3, "or", markersize=2, color=colors_dict[3])
    """
    return ans