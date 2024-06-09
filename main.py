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

def solve(sudoku: Sudoku) -> Sudoku:
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
            return sudoku
    return sudoku

def main() -> None:
    sudoku = Sudoku("data/easy_to_solve/example.txt", SUDOKU_SIZE)
    sudoku.propagate_constraints()
    solution = solve(sudoku)
    print(solution)
    print(f"Is solution correct? {solution.confirm_solution()}")
    

if __name__ == "__main__":
    main()