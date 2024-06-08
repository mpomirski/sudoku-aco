from Sudoku import Sudoku
class Ant:
    raise NotImplementedError
    def __init__(self, sudoku: Sudoku, global_pheromone_matrix: list[list[list[float]]], cell: list[int]) -> None:
        self.sudoku: Sudoku = sudoku
        self.current_cell: list[int] = cell
        self._chosen_value: str = ""
        self._correct_guesses: int = 0
        self.global_pheromone_matrix: list[list[list[float]]] = global_pheromone_matrix

    def choose_value(self) -> str:
        # Choose value with highest pheromone
        max_value: int = 0
        for i, value in enumerate(self.global_pheromone_matrix[self.current_cell[0]][self.current_cell[1]]):
            if value == max(self.global_pheromone_matrix[self.current_cell[0]][self.current_cell[1]]):
                max_value = i+1
        self._chosen_value = str(max_value)
        return self._chosen_value

    def set_cell_value(self, new_value: str) -> None:
        self.sudoku.set_cell_value(self.current_cell[0], self.current_cell[1], [new_value])
        self._correct_guesses += 1
    
    def propagate_constraints(self) -> None:
        self.sudoku = propagate_constraints(self.sudoku)

    def update_pheromone(self) -> list[list[list[float]]]:
        old_pheromone_value: float = self.global_pheromone_matrix[self.current_cell[0]][self.current_cell[1]][int(self._chosen_value)-1]
        new_value: float = (1 - KSI) * old_pheromone_value + KSI * T_0
        self.global_pheromone_matrix[self.current_cell[0]][self.current_cell[1]][int(self._chosen_value)-1] = new_value
        return self.global_pheromone_matrix
    def move_to_next_cell(self) -> None:
        # Goes row by row, column by column
        self.current_cell[1] += 1
        if self.current_cell[1] == SUDOKU_SIZE-1:
            self.current_cell[1] = 0
            self.current_cell[0] += 1
            if self.current_cell[0] == SUDOKU_SIZE-1:
                self.current_cell[0] = 0

    def get_score(self) -> int:
        return self._correct_guesses

    def set_new_pheromone_matrix(self, pheromone_matrix: list[list[list[float]]]) -> None:
        self.global_pheromone_matrix = pheromone_matrix
