# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 14:18:51 2024

@author: Liu Qizhang
"""

import pulp

def solve_sudoku(grid):
    
    # Define the problem
    prob = pulp.LpProblem("Sudoku", pulp.LpMinimize)

    # Define variables
    choices = pulp.LpVariable.dicts("Choice", (range(9), range(9), range(1, 10)), cat='Binary')

    # Objective function (dummy, as we are not optimizing but just finding a feasible solution)
    prob += 0

    # Constraints
    # Each cell must contain exactly one number
    for row in range(9):
        for col in range(9):
            prob += pulp.lpSum(choices[row][col][num] for num in range(1, 10)) == 1

    # Each number must appear exactly once in each row
    for row in range(9):
        for num in range(1, 10):
            prob += pulp.lpSum(choices[row][col][num] for col in range(9)) == 1

    # Each number must appear exactly once in each column
    for col in range(9):
        for num in range(1, 10):
            prob += pulp.lpSum(choices[row][col][num] for row in range(9)) == 1

    # Each number must appear exactly once in each 3x3 subgrid
    for box_row in range(3):
        for box_col in range(3):
            for num in range(1, 10):
                prob += pulp.lpSum(choices[row][col][num]
                                   for row in range(box_row * 3, (box_row + 1) * 3)
                                   for col in range(box_col * 3, (box_col + 1) * 3)) == 1

    # Initial values from the puzzle
    for row in range(9):
        for col in range(9):
            if grid[row][col] != 0:
                prob += choices[row][col][grid[row][col]] == 1

    # Solve the problem
    prob.solve()

    # Extract the solution
    solution = [[0 for _ in range(9)] for _ in range(9)]
    for row in range(9):
        for col in range(9):
            for num in range(1, 10):
                if pulp.value(choices[row][col][num]) == 1:
                    solution[row][col] = num

    return solution

# Example Sudoku puzzle (0 represents empty cells)
grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]


# Solve the Sudoku puzzle
solution = solve_sudoku(grid)

# Print the solution
for row in solution:
    print(row)