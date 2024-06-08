"""
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
SUDOKU_SIZE = 9
SUDOKU_BLOCK_SIZE = 3
NUMBER_OF_ANTS = SUDOKU_SIZE**2
def fixed_peer_values(sudoku: list[list[list[str]]], i: int, j: int) -> set[str]:
    fixed_peer_values: set[str] = set()
    for _i, row in enumerate(sudoku):
        for _j, cell in enumerate(row):
            if _i == i and cell != sudoku[i][j] and len(cell) == 1:
                fixed_peer_values.add(cell[0])
            if _j == j and cell != sudoku[i][j] and len(cell) == 1:
                fixed_peer_values.add(cell[0])
            if _i // SUDOKU_BLOCK_SIZE == i // SUDOKU_BLOCK_SIZE and _j // SUDOKU_BLOCK_SIZE == j // SUDOKU_BLOCK_SIZE and cell != sudoku[i][j] and len(cell) == 1:
                fixed_peer_values.add(cell[0])
    return fixed_peer_values

def possible_peer_values(sudoku: list[list[list[str]]], i: int, j: int) -> set[str]:
    possible_peer_values: set[str] = set()
    for _i, row in enumerate(sudoku):
        for _j, cell in enumerate(row):
            if _i == i and cell != sudoku[i][j] and len(cell) > 1:
                possible_peer_values.update(cell)
            if _j == j and cell != sudoku[i][j] and len(cell) > 1:
                possible_peer_values.update(cell)
            if _i // SUDOKU_BLOCK_SIZE == i // SUDOKU_BLOCK_SIZE and _j // SUDOKU_BLOCK_SIZE == j // SUDOKU_BLOCK_SIZE and cell != sudoku[i][j] and len(cell) != 1:
                possible_peer_values.update(cell)
    return possible_peer_values

def propagate_constraints(sudoku: list[list[list[str]]]) -> list[list[list[str]]]:
    changes_made = True
    max_iterations = 100
    while changes_made and max_iterations > 0:
        changes_made = False
        for i, row in enumerate(sudoku):
            for j, cell in enumerate(row):
                if len(cell) > 1:
                    print(cell)
                    copy: list[str] = sudoku[i][j]
#Eliminate from a cell's value set all values that are fixed in any of the cell's peers.
                    peer_values: set[str] = fixed_peer_values(sudoku, i, j)
                    sudoku[i][j] = [x for x in cell if x not in peer_values]

#If any values in a cell's value set are in the only possible place in any of the cell's units, then fix that value.
                    # sudoku[i][j] = [x for x in cell if x not in possible_peer_values(sudoku, i, j)]
                    # Is this needed?
                    if len(sudoku[i][j]) != len(copy):
                        changes_made = True
        max_iterations -= 1
        if max_iterations == 0:
            print("Max iterations reached")
    return sudoku

def read_sudoku(file) -> list[list[list[str]]]:
    with open(file, 'r') as f:
        return [[[x] if x != "-" else list(map(str, range(1,10))) for x in line.rstrip()] for line in f]

def print_sudoku(sudoku: list[list[list[str]]]) -> None:
    for row in sudoku:
        print("\t".join([''.join(cell) for cell in row]))

def is_solved(sudoku: list[list[list[str]]]) -> bool:
    for row in sudoku:
        for cell in row:
            if len(cell) != 1:
                return False
    return True

class Ant:
    def __init__(self, sudoku: list[list[list[str]]]) -> None:
        self.sudoku: list[list[list[str]]] = sudoku
        self.current_cell: list[int] = [0, 0]
        self.local_pheromone: float = 1/SUDOKU_SIZE**2

    def choose_value(self) -> None:
        raise NotImplementedError

    def set_cell_value(self) -> None:
        raise NotImplementedError
    
    def propagate_constraints(self) -> None:
        self.sudoku = propagate_constraints(self.sudoku)

    def update_local_pheromone(self) -> None:
        raise NotImplementedError

    def move_to_next_cell(self) -> None:
        raise NotImplementedError

    def get_score(self) -> int:
        raise NotImplementedError

def solve(sudoku: list[list[list[str]]]) -> list[list[list[str]]]:
    sudoku = propagate_constraints(sudoku)
    pheromone_matrix: list[list[list[float]]] = [
        [[1/SUDOKU_SIZE**2 for i in range(9)] for _ in range(SUDOKU_SIZE)] for _ in range(SUDOKU_SIZE)]
    while not is_solved(sudoku):
        ants: list[Ant] = [Ant(sudoku) for _ in range(NUMBER_OF_ANTS)]
        for i in range(SUDOKU_SIZE**2):
            for ant in ants:
                if len(ant.sudoku[i]) > 1:
                    ant.choose_value()
                    ant.set_cell_value()
                    ant.propagate_constraints()
                    ant.update_local_pheromone()
                ant.move_to_next_cell()
        # best_ant: Ant
        # update_global_pheromone()
        # evaporate_best_value()
    raise NotImplementedError

def main() -> None:
    sudoku: list[list[list[str]]] = read_sudoku("data/easy_to_solve/example.txt")
    

if __name__ == "__main__":
    main()