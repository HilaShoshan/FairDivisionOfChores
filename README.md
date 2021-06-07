# FairDivisionOfChores
## Research Final Project

We focus on the theme of fair division of chores (objects with non-positive utility), in a continuous period of time. 
That is, a group of agents should write their preferences every day (for a week for example), and we should divide the tasks between them. 
To solve this problem, we decided to treat each day as a category.
Our goal is to find an algorithm that limits the number of tasks an agent can get from each category (i.e. each day), thus preventing an unbalanced division.

Terms / Assumptions:
* Indivisible Chores (non-positive utility for all agents)
* Additive valuations
* Capacity Constraints (An allocation called feasible iff each agent gets at most k_h tasks from each category h)
* superior_value(|Ch|/n) ≤ kh
* Tasks cannot be discarded
