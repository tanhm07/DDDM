import pulp

# Define the problem
prob = pulp.LpProblem("Hart_Enterprise_Investment", pulp.LpMaximize)

# Decision variables
# Each investment alternative can be made in one of the three years
investments = ['E', 'B', 'T', 'A', 'R', 'P']
years = [1, 2, 3]

# Expected profits for each investment
profits = {
    'E': 4.0,
    'B': 6.0,
    'T': 10.5,
    'A': 4.0,
    'R': 8.0,
    'P': 3.0
}

# Capital requirements for each investment in each year
capital_requirements = {
    'E': {1: 3.0, 2: 1.0, 3: 4.0},
    'B': {1: 2.5, 2: 3.5, 3: 3.5},
    'T': {1: 6.0, 2: 4.0, 3: 5.0},
    'A': {1: 2.0, 2: 1.5, 3: 1.8},
    'R': {1: 4.0, 2: 1.0, 3: 4.0},
    'P': {1: 1.0, 2: 0.5, 3: 0.9}
}

# Capital funds available each year
initial_capital_funds = {1: 8.5, 2: 6.0, 3: 8.0}

# Create a binary variable for each investment in each year
investment_vars = pulp.LpVariable.dicts("Invest",
                                        [(i, y) for i in investments for y in years],
                                        cat='Binary')

# Create variables for unused capital funds at the end of each year
unused_funds = pulp.LpVariable.dicts("Unused_Funds", years, lowBound=0, cat='Continuous')

# Objective function: maximize total expected profit
prob += pulp.lpSum([profits[i] * investment_vars[(i, y)] for i in investments for y in years]), "Total_Profit"

# Constraints
# 1. Each investment can be made only once over the three years
for i in investments:
    prob += pulp.lpSum([investment_vars[(i, y)] for y in years]) <= 1, f"One_Investment_{i}"

# 2. Capital constraints for each year with carryover funds
# Year 1
prob += pulp.lpSum([capital_requirements[i][1] * investment_vars[(i, 1)] for i in investments]) <= initial_capital_funds[1], "Capital_Constraint_Year_1"
# Year 2
prob += pulp.lpSum([capital_requirements[i][2] * investment_vars[(i, 2)] for i in investments]) <= initial_capital_funds[2] + unused_funds[1], "Capital_Constraint_Year_2"
# Year 3
prob += pulp.lpSum([capital_requirements[i][3] * investment_vars[(i, 3)] for i in investments]) <= initial_capital_funds[3] + unused_funds[2], "Capital_Constraint_Year_3"

# 3. Calculate unused funds at the end of each year
# Unused funds at the end of Year 1
prob += unused_funds[1] == initial_capital_funds[1] - pulp.lpSum([capital_requirements[i][1] * investment_vars[(i, 1)] for i in investments]), "Unused_Funds_Year_1"
# Unused funds at the end of Year 2
prob += unused_funds[2] == initial_capital_funds[2] + unused_funds[1] - pulp.lpSum([capital_requirements[i][2] * investment_vars[(i, 2)] for i in investments]), "Unused_Funds_Year_2"
# Unused funds at the end of Year 3
prob += unused_funds[3] == initial_capital_funds[3] + unused_funds[2] - pulp.lpSum([capital_requirements[i][3] * investment_vars[(i, 3)] for i in investments]), "Unused_Funds_Year_3"

# 4. Non-negativity constraints for unused funds
for y in years:
    prob += unused_funds[y] >= 0, f"Non_Negative_Constraint_Year_{y}"
    
# Solve the problem
prob.solve()

# Print the results
print("Status:", pulp.LpStatus[prob.status])
print("Optimal Investment Plan:")
for i in investments:
    for y in years:
        if pulp.value(investment_vars[(i, y)]) == 1:
            print(f"Invest in {i} in year {y}")
print("Total Expected Profit:", pulp.value(prob.objective))
print("Unused Funds at the end of each year:")
for y in years:
    print(f"Year {y}: {pulp.value(unused_funds[y])} million dollars")