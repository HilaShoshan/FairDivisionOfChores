# FairDivisionOfTasks
## Research Final Project

I started my project with the theme of fair division of tasks (objects with non-positive utility), in a continuous period of time. 
That is, a group of agents should write their preferences every day (for a week for example), and we should divide the tasks between them. 
To solve this problem, we decided to treat each day as a category.
This way we could find an algorithm that limits the number of tasks an agent can get from each category (i.e. every day), thus preventing an unbalanced division.

With the help of the articles: Fair allocation of combinations of indivisible goods and chores and Fair Division Under Cardinality Constraints, I wrote a polynomial time algorithm that finds a fair division (EF1) of the tasks with the cardinality constraints.

Terms / Assumptions:
* Indivisible Tasks (non-positive utility for all agents)
* Additive valuations
* Cardinality Constraints (An allocation called feasible iff each agent gets at most k_h tasks from each category h)
* superior_value(|Ch|/n) ≤ kh
* Tasks cannot be discarded

We then moved on to a slightly different topic: fair division of courses
