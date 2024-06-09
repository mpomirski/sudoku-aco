"""
Author: Michał Pomirski
Pseudocode from Lloyd, Huw & Amos, Martyn. (2019).
Solving Sudoku With Ant Colony Optimization.
IEEE Transactions on Games. PP. 1-1.
10.1109/TG.2019.2942773.

read in puzzle
for all cells with fixed values:
    propagate constraints (according to Section 3.1)
     - Eliminate from a cell's value set all values that are fixed
       in any of the cell's peers.
     - If any values in a cell's value set are in the only possible
       place in any of the cell's units, then fix that value.

initialize global pheromone matrix
while puzzle is not solved:
    give each ant a local copy of puzzle
    assign each ant to a different cell
    for number of cells:
        for each ant:
            if current cell value not set:
                choose value from current cell's value set
                set cell value
                propagate constraints
                update local pheromone
            move to next cell
    find best ant
    do global pheromone update
    do best value evaporation
"""
from Sudoku import Sudoku
from Ant import Ant
from constants import SUDOKU_SIZE, C, EVAPORATION_RATE, EVAPORATION_PARAMETER, MAX_ITERS
from copy import deepcopy
from time import time

def solve(sudoku: Sudoku) -> tuple[Sudoku, list[list[list[float]]]]:
    sudoku.propagate_constraints()
    pheromone_matrix: list[list[list[float]]] = [
        [[1/C for i in range(9)] for _ in range(SUDOKU_SIZE)] for _ in range(SUDOKU_SIZE)]
    best_pheromone_to_add: float = 0
    iters: int = 0
    while not sudoku.is_solved():
        ants: list[Ant] = []
        for i in range(sudoku.size):
            for j in range(sudoku.size):
                # Position each ant in a different cell
                ants.append(Ant(deepcopy(sudoku), pheromone_matrix, [i, j], i*10+j))

        for i in range(SUDOKU_SIZE):
            for j in range(SUDOKU_SIZE):
                for ant in ants:
                    # Update pheromone matrix for each ant
                    ant.set_new_pheromone_matrix(pheromone_matrix)
                    # If current cell value not set
                    if not ant.sudoku.is_fixed(i, j):
                        # Choose value from current cell's value set, set it and propagate constraints
                        new_value: str = ant.choose_value()
                        ant.set_cell_value(new_value)
                        # TODO: Check if constraints are correctly propagated
                        ant.propagate_constraints()
                        # Local pheromone update
                        pheromone_matrix = ant.update_pheromone()
                    ant.move_to_next_cell()
        # Find best peforming ant
        best_ant: Ant = max(ants, key=lambda x: x.get_score())
        # Calculate pheromone to add, if it's the best so far, save it
        best_pheromone_to_add = max(C / (C - best_ant.get_score()), best_pheromone_to_add)
        # Update pheromones in cells where best ant has fixed the value
        for i in range(SUDOKU_SIZE):
            for j in range(SUDOKU_SIZE):
                if best_ant.sudoku.is_fixed(i, j):
                    pheromone_matrix[i][j][int(best_ant.sudoku.board[i][j][0])-1] *= (1 - EVAPORATION_PARAMETER)
                    pheromone_matrix[i][j][int(best_ant.sudoku.board[i][j][0])-1] += EVAPORATION_PARAMETER * best_pheromone_to_add
        # Evaporate current best pheromone
        best_pheromone_to_add *= (1 - EVAPORATION_RATE)
        print(f"--------------------\nIteration {iters}\n--------------------")
        iters += 1
        if iters == MAX_ITERS:
            print("Max iterations reached")
            sudoku = best_ant.sudoku
            return sudoku, pheromone_matrix
    return sudoku, pheromone_matrix

def main() -> None:
    simple_files = ["data/simple_0.txt", "data/simple_1.txt", "data/simple_2.txt", "data/simple_3.txt", "data/simple_4.txt"]
    easy_files = ["data/easy_0.txt", "data/easy_1.txt","data/easy_2.txt", "data/easy_3.txt", "data/easy_4.txt"]
    medium_files = ["data/medium_0.txt", "data/medium_1.txt", "data/medium_2.txt", "data/medium_3.txt", "data/medium_4.txt"]
    hard_files = ["data/hard_0.txt", "data/hard_1.txt", "data/hard_2.txt", "data/hard_3.txt", "data/hard_4.txt"]
    with open("res10.txt", 'w') as f:
        f.write("Ant colony\tBrute force\n")
        f.write("Simple:\n")
        for file in simple_files:
            start_time1 = time()
            sudoku = Sudoku(file, SUDOKU_SIZE)
            solution, matrix = solve(sudoku)
            end_time1 = time()
            start_time2 = time()
            sudoku2 = Sudoku(file, SUDOKU_SIZE)
            sudoku2.brute_force()
            end_time2 = time()
            f.write(f"{end_time1 - start_time1:.2f}\t{end_time2 - start_time2}\n")
            f.write(f"{solution.confirm_solution()}\t{sudoku2.confirm_solution()}\n")
        f.write("Easy:\n")
        for file in easy_files:
            start_time1 = time()
            sudoku = Sudoku(file, SUDOKU_SIZE)
            solution, matrix = solve(sudoku)
            end_time1 = time()
            start_time2 = time()
            sudoku2 = Sudoku(file, SUDOKU_SIZE)
            sudoku2.brute_force()
            end_time2 = time()
            f.write(f"{end_time1 - start_time1:.2f}\t{end_time2 - start_time2}\n")
            f.write(f"{solution.confirm_solution()}\t{sudoku2.confirm_solution()}\n")
        f.write("Medium:\n")
        for file in medium_files:
            start_time1 = time()
            sudoku = Sudoku(file, SUDOKU_SIZE)
            solution, matrix = solve(sudoku)
            end_time1 = time()
            start_time2 = time()
            sudoku2 = Sudoku(file, SUDOKU_SIZE)
            sudoku2.brute_force()
            end_time2 = time()
            f.write(f"{end_time1 - start_time1:.2f}\t{end_time2 - start_time2}\n")
            f.write(f"{solution.confirm_solution()}\t{sudoku2.confirm_solution()}\n")
        f.write("Hard:\n")
        for file in hard_files:
            start_time1 = time()
            sudoku = Sudoku(file, SUDOKU_SIZE)
            solution, matrix = solve(sudoku)
            end_time1 = time()
            start_time2 = time()
            sudoku2 = Sudoku(file, SUDOKU_SIZE)
            sudoku2.brute_force()
            end_time2 = time()
            f.write(f"{end_time1 - start_time1:.2f}\t{end_time2 - start_time2}\n")
            f.write(f"{solution.confirm_solution()}\t{sudoku2.confirm_solution()}\n")
    

if __name__ == "__main__":
    main()