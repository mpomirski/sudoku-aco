import numpy as np

class Sudoku:
    def __init__(self, filename: str, size: int) -> None:
        self.size: int = size
        self._block_size = int(size**0.5)
        self.board = self.read_sudoku(filename)
        self.unsolved_cells = self.get_unsolved_cells()

    def read_sudoku(self, file: str) -> np.ndarray:
        with open(file, 'r') as f:
            board = [
                [
                    [int(x) - 1] if x != "-" else list(range(9))
                    for x in line.rstrip()
                ]
                for line in f
            ]
        return np.array(board, dtype=object)

    def get_unsolved_cells(self):
        unsolved = []
        for i in range(self.size):
            for j in range(self.size):
                if len(self.board[i, j]) > 1:
                    unsolved.append((i, j))
        return unsolved

    def fixed_peer_values(self, i: int, j: int) -> set:
        fixed_peer_values: set = set()

        # Check row and column
        for k in range(self.size):
            if k != j and len(self.board[i, k]) == 1:
                fixed_peer_values.add(self.board[i, k][0])
            if k != i and len(self.board[k, j]) == 1:
                fixed_peer_values.add(self.board[k, j][0])
        
        # Calculate block coordinates
        block_start_row = (i // self._block_size) * self._block_size
        block_start_col = (j // self._block_size) * self._block_size
        
        # Check block
        for _i in range(block_start_row, block_start_row + self._block_size):
            for _j in range(block_start_col, block_start_col + self._block_size):
                if (_i != i or _j != j) and len(self.board[_i, _j]) == 1:
                    fixed_peer_values.add(self.board[_i, _j][0])

        return fixed_peer_values


    def propagate_constraints(self) -> None:
        changes_made = True
        max_iterations = 100
        while changes_made and max_iterations > 0:
            changes_made = False
            for (i, j) in self.unsolved_cells:
                cell = self.board[i, j]
                if len(cell) > 1:
                    peer_values = self.fixed_peer_values(i, j)
                    new_values = [x for x in cell if x not in peer_values]
                    if len(new_values) != len(cell):
                        self.board[i, j] = new_values
                        changes_made = True
            max_iterations -= 1


    def set_cell_value(self, i: int, j: int, value: list) -> None:
        self.board[i, j] = value
        if (i, j) in self.unsolved_cells:
            self.unsolved_cells.remove((i, j))

    def find_unassigned_location(self):
        if self.unsolved_cells:
            return self.unsolved_cells[0]
        return -1, -1

    def brute_force(self):
        self.propagate_constraints()
        i, j = self.find_unassigned_location()
        if i == -1 and j == -1:
            return self.confirm_solution()

        for value in self.board[i, j]:
            backup = self.board.copy()  # Backup the current state
            self.set_cell_value(i, j, [value])
            self.propagate_constraints()
            if self.brute_force():
                return True
            self.board = backup  # Restore the previous state
            self.unsolved_cells.insert(0, (i, j))  # Reinsert the cell as unsolved
        return False

    def confirm_solution(self) -> bool:
        # Check rows, columns, and blocks for uniqueness
        for i in range(self.size):
            if not self.is_unit_valid(self.board[i, :]) or not self.is_unit_valid(self.board[:, i]):
                return False
        for i in range(0, self.size, self._block_size):
            for j in range(0, self.size, self._block_size):
                if not self.is_unit_valid(self.board[i:i+self._block_size, j:j+self._block_size].flatten()):
                    return False
        return True

    def is_unit_valid(self, unit) -> bool:
        unit = [cell[0] for cell in unit if len(cell) == 1]
        return len(unit) == len(set(unit))

    def __repr__(self) -> str:
        res: str = ''
        for i, row in enumerate(self.board):
            for j, col in enumerate(row):
                col_to_write: str = ''.join(map(str, col)).center(9)
                res += col_to_write
                if j % self._block_size == self._block_size - 1:
                    res += '|'
            res += '\n'
            if i % self._block_size == self._block_size - 1:
                res += '-' * len(col_to_write) * self.size + '\n'
        return res

    def is_solved(self) -> bool:
        return all(len(cell) == 1 for row in self.board for cell in row)

    def is_fixed(self, i: int, j: int) -> bool:
        return len(self.board[i, j]) == 1