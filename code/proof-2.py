#!python3

"""
Try to prove the theorem for general tasks, fixed number of categories.
"""


import cvxpy

r = 100

CATEGORIES = 10
CURRENT_CATEGORY = 7
ITEMS_PER_CATEGORY = 2

PREVIOUS_CATEGORIES = range(0, CURRENT_CATEGORY)
NEXT_CATEGORIES = range(CURRENT_CATEGORY+1, CATEGORIES)

print(f"PREVIOUS_CATEGORIES={list(PREVIOUS_CATEGORIES)}, CURRENT_CATEGORY={CURRENT_CATEGORY}, NEXT_CATEGORIES={list(NEXT_CATEGORIES)}")


EASIER = 0
HARDER = 1

u1 = cvxpy.Variable((CATEGORIES, ITEMS_PER_CATEGORY))
u2 = cvxpy.Variable((CATEGORIES, ITEMS_PER_CATEGORY))

task_constraints = \
    [u1[c,EASIER] >= u1[c,HARDER] for c in range(CATEGORIES)] +\
    [u2[c,EASIER] >= u2[c,HARDER] for c in range(CATEGORIES)]

negativity_constraints = \
    [u1[c,t] <= 0 for c in range(CATEGORIES) for t in range(ITEMS_PER_CATEGORY)] +\
    [u2[c,t] <= 0 for c in range(CATEGORIES) for t in range(ITEMS_PER_CATEGORY)]

x = [u1[c,HARDER]-u1[c,EASIER] for c in range(CATEGORIES)]
y = [u2[c,HARDER]-u2[c,EASIER] for c in range(CATEGORIES)]

ratio_constraints = \
    [y[c] <= r * x[c] for c in PREVIOUS_CATEGORIES] + \
    [y[CURRENT_CATEGORY] == r * x[CURRENT_CATEGORY]] + \
    [y[c] >= r * x[c] for c in NEXT_CATEGORIES] 

u1A1before = sum([u1[c,HARDER] for c in PREVIOUS_CATEGORIES] + [u1[CURRENT_CATEGORY,EASIER]] + [u1[c,EASIER] for c in NEXT_CATEGORIES])
u1A1after  = sum([u1[c,HARDER] for c in PREVIOUS_CATEGORIES] + [u1[CURRENT_CATEGORY,HARDER]] + [u1[c,EASIER] for c in NEXT_CATEGORIES])

u2A1before = sum([u2[c,HARDER] for c in PREVIOUS_CATEGORIES] + [u2[CURRENT_CATEGORY,EASIER]] + [u2[c,HARDER] for c in NEXT_CATEGORIES])
u2A1after  = sum([u2[c,HARDER] for c in PREVIOUS_CATEGORIES] + [u2[CURRENT_CATEGORY,HARDER]] + [u2[c,HARDER] for c in NEXT_CATEGORIES])

u1A2before = sum([u1[c,EASIER] for c in PREVIOUS_CATEGORIES] + [u1[CURRENT_CATEGORY,HARDER]] + [u1[c,HARDER] for c in NEXT_CATEGORIES])
u1A2after  = sum([u1[c,EASIER] for c in PREVIOUS_CATEGORIES] + [u1[CURRENT_CATEGORY,EASIER]] + [u1[c,HARDER] for c in NEXT_CATEGORIES])

u2A2before = sum([u2[c,EASIER] for c in PREVIOUS_CATEGORIES] + [u2[CURRENT_CATEGORY,HARDER]] + [u2[c,HARDER] for c in NEXT_CATEGORIES])
u2A2after  = sum([u2[c,EASIER] for c in PREVIOUS_CATEGORIES] + [u2[CURRENT_CATEGORY,EASIER]] + [u2[c,HARDER] for c in NEXT_CATEGORIES])

violation = cvxpy.Variable()

agent1_envies_after  = [u1A1after  - u1[CURRENT_CATEGORY,HARDER] <= u1A2after - violation]
agent2_envies_before = [u2A2before - u2[CURRENT_CATEGORY,HARDER] <= u2A1before - violation]

agent1_not_envies_before = [u1A1before >= u1A2before]
agent2_not_envies_after = [u2A2after >= u2A1after]


prob = cvxpy.Problem(cvxpy.Maximize(1), 
    constraints = 
        task_constraints +
        negativity_constraints +
        ratio_constraints +
        agent1_envies_after +
        agent2_envies_before +
        agent1_not_envies_before + 
        agent2_not_envies_after +
        [violation >= 0.01]
        # u1A1 == -3,
        # u1A2 == -0.5,
        # u2A1 == -1.5,
        # u2A2 == -1.5,
        # u1t == -6,
    )
prob.solve()
print("status:", prob.status)
if prob.status=="optimal":
    print(f"u1={u1.value:.2}, u2={u2.value:.2}, violation={violation.value:.2}")
    print(f"Values before transfer (t* is in A2):")
    print(f"   Agent 1: for 1: {u1A1before.value:.2}, for 2: {u1A2before.value:.2}")
    print(f"   Agent 2: for 1: {u2A1before.value:.2}, for 2: {u2A2before.value:.2}")
    print(f"Values after transfer (t* is in A1):")
    print(f"   Agent 1: for 1: {u1A1after.value:.2}, for 2: {u1A2after.value:.2}")
    print(f"   Agent 2: for 1: {u2A1after.value:.2}, for 2: {u2A2after.value:.2}")
