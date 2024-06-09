from Sudoku import Sudoku
from constants import SUDOKU_SIZE, KSI, T_0, DEBUG
from numpy.random import choice
class Ant:
    def __init__(self, sudoku: Sudoku, global_pheromone_matrix: list[list[list[float]]], cell: list[int], id: int) -> None:
        self.sudoku: Sudoku = sudoku
        self.id = id
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

        if DEBUG:
            print(f"Ant {self.id} at position {self.current_cell} with pheromones {self.global_pheromone_matrix[self.current_cell[0]][self.current_cell[1]]} chose value {self._chosen_value}")
        return self._chosen_value

    def set_cell_value(self, new_value: str) -> None:
        self.sudoku.set_cell_value(self.current_cell[0], self.current_cell[1], [new_value])
        self._correct_guesses += 1
    
    def propagate_constraints(self) -> None:
        self.sudoku.propagate_constraints()

    def update_pheromone(self) -> list[list[list[float]]]:
        old_pheromone_value: float = self.global_pheromone_matrix[self.current_cell[0]][self.current_cell[1]][int(self._chosen_value)-1]
        new_value: float = (1 - KSI) * old_pheromone_value + KSI * T_0
        self.global_pheromone_matrix[self.current_cell[0]][self.current_cell[1]][int(self._chosen_value)-1] = new_value
        if DEBUG:
            print(f"Ant {self.id} updated pheromone for cell {self.current_cell} value {self._chosen_value} from {old_pheromone_value:.5f} to {new_value:.5f}")
        return self.global_pheromone_matrix
    def move_to_next_cell(self) -> None:
        # Goes row by row, column by column
        row, col = self.current_cell
        col += 1
        if col == SUDOKU_SIZE:
            col = 0
            row += 1
        if row == SUDOKU_SIZE:
            row = 0
        self.current_cell = [row, col]

        

    def get_score(self) -> int:
        return self._correct_guesses

    def set_new_pheromone_matrix(self, pheromone_matrix: list[list[list[float]]]) -> None:
        self.global_pheromone_matrix = pheromone_matrix
