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
# from Ant import Ant
SUDOKU_SIZE: int = 9
NUMBER_OF_ANTS: int = SUDOKU_SIZE**2
T_0: float = 1/SUDOKU_SIZE**2
KSI: float = 0.1
EVAPORATION_RATE: float = 0.3
C: int = SUDOKU_SIZE**2

def solve(sudoku: Sudoku) -> Sudoku:
    raise NotImplementedError
    sudoku.propagate_constraints()
    pheromone_matrix: list[list[list[float]]] = [
        [[1/C for i in range(9)] for _ in range(SUDOKU_SIZE)] for _ in range(SUDOKU_SIZE)]
    while not sudoku.is_solved():
        ants: list[Ant] = []
        for i in range(sudoku.size):
            for j in range(sudoku.size):
                ants.append(Ant(sudoku, pheromone_matrix, [i, j]))

        for i in range(SUDOKU_SIZE):
            for j in range(SUDOKU_SIZE):
                for ant in ants:
                    ant.set_new_pheromone_matrix(pheromone_matrix)
                    if len(ant.sudoku[ant.current_cell[0]][ant.current_cell[1]]) > 1:
                        new_value: str = ant.choose_value()
                        ant.set_cell_value(new_value)
                        ant.propagate_constraints()
                        pheromone_matrix = ant.update_pheromone()
                    ant.move_to_next_cell()
        best_ant: Ant = max(ants, key=lambda x: x.get_score())
        for i in range(SUDOKU_SIZE):
            for j in range(SUDOKU_SIZE):
                if len(sudoku[i][j]) > 1:
                    pheromone_matrix[i][j] = [(1 - EVAPORATION_RATE) * x for x in pheromone_matrix[i][j]]
        # evaporate_best_value()

def main() -> None:
    sudoku = Sudoku("data/easy_to_solve/example.txt", SUDOKU_SIZE)
    sudoku.propagate_constraints()
    print(sudoku)
    

if __name__ == "__main__":
    main()