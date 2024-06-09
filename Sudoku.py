class Sudoku:
    def __init__(self, filename: str, size: int) -> None:
        self.board: list[list[list[str]]] = self.read_sudoku(filename)
        self.size: int = size
        self._block_size = int(size**0.5)

    def read_sudoku(self, file) -> list[list[list[str]]]:
        with open(file, 'r') as f:
            return [[[x] if x != "-" else list(map(str, range(1,10))) for x in line.rstrip()] for line in f]

    def fixed_peer_values(self, i: int, j: int) -> set[str]:
        fixed_peer_values: set[str] = set()

        for idx in range(len(self.board)):
            # Check row
            row_cell = self.board[i][idx]
            if idx != j and len(row_cell) == 1:
                fixed_peer_values.add(row_cell[0])
            
            # Check column
            col_cell = self.board[idx][j]
            if idx != i and len(col_cell) == 1:
                fixed_peer_values.add(col_cell[0])
        
        # Calculate block coordinates
        block_start_row = (i // self._block_size) * self._block_size
        block_start_col = (j // self._block_size) * self._block_size
        
        # Check block
        for _i in range(block_start_row, block_start_row + self._block_size):
            for _j in range(block_start_col, block_start_col + self._block_size):
                if (_i != i or _j != j) and len(self.board[_i][_j]) == 1:
                    fixed_peer_values.add(self.board[_i][_j][0])

        return fixed_peer_values

    def possible_peer_values(self, i: int, j: int) -> set[str]:
        possible_peer_values: set[str] = set()
        for _i, row in enumerate(self.board):
            for _j, cell in enumerate(row):
                if _i == i and cell != self.board[i][j] and len(cell) > 1:
                    possible_peer_values.update(cell)
                if _j == j and cell != self.board[i][j] and len(cell) > 1:
                    possible_peer_values.update(cell)
                if _i // self._block_size == i // self._block_size and _j // self._block_size == j // self._block_size and cell != self.board[i][j] and len(cell) != 1:
                    possible_peer_values.update(cell)
        return possible_peer_values

    def is_fixed(self, i: int, j: int) -> bool:
        return len(self.board[i][j]) == 1

    def propagate_constraints(self) -> None:
        changes_made = True
        max_iterations = 100
        while changes_made and max_iterations > 0:
            changes_made = False
            for i, row in enumerate(self.board):
                for j, cell in enumerate(row):
                    if len(cell) > 1:
                        copy: list[str] = self.board[i][j]
    #Eliminate from a cell's value set all values that are fixed in any of the cell's peers.
                        peer_values: set[str] = self.fixed_peer_values(i, j)
                        self.board[i][j] = [x for x in cell if x not in peer_values]

    #If any values in a cell's value set are in the only possible place in any of the cell's units, then fix that value.
                        # self.board[i][j] = [x for x in cell if x not in self.possible_peer_values(i, j)]
                        if len(self.board[i][j]) != len(copy):
                            changes_made = True
            max_iterations -= 1
            if max_iterations == 0:
                print("Max iterations reached")

    def set_cell_value(self, i: int, j: int, value: list[str]) -> None:
        self.board[i][j] = value

    def find_unassigned_location(self):
            for i, row in enumerate(self.board):
                for j, cell in enumerate(row):
                    if len(cell) > 1:
                        return i, j
            return -1, -1

    def brute_force(self):
        self.propagate_constraints()
        i, j = self.find_unassigned_location()
        if i == -1 and j == -1:
            if self.confirm_solution():
                return True
            else:
                return False

        for value in self.board[i][j]:
            backup = [row[:] for row in self.board]  # Backup the current state
            self.set_cell_value(i, j, [value])
            self.propagate_constraints()
            if self.brute_force():
                return True
            self.board = backup  # Restore the previous state
        return False


    def confirm_solution(self) -> bool:
        # Check rows
        for row in self.board:
            if any([len(cell) != 1 for cell in row]):
                return False
            if len(set([x[0] for x in row])) != len(row):
                return False
        # Check columns
        cols: list[list[list[str]]] = []
        for i in range(self.size):
            col: list[list[str]] = []
            for row in self.board:
                col.append(row[i])
            cols.append(col)
        for col in cols:
            if len(set([x[0] for x in col])) != len(col):
                return False
        # Check blocks
        blocks: list[list[list[str]]] = []
        for i in range(self._block_size):
            for j in range(self._block_size):
                block: list[list[str]] = []
                for row in self.board[i*self._block_size:(i+1)*self._block_size]:
                    block.extend(row[j*self._block_size:(j+1)*self._block_size])
                blocks.append(block)
        for block in blocks:
            if len(set([x[0] for x in block])) != len(block):
                return False
        return True
        



    def __repr__(self) -> str:
        res: str = ''
        for i, row in enumerate(self.board):
            for j, col in enumerate(row):
                col_to_write: str = ''.join(col).center(9)
                res += col_to_write
                if j % self._block_size == self._block_size - 1:
                    res += '|'
            res += '\n'
            if i % self._block_size == self._block_size - 1:
                res += '-' * len(col_to_write) * self.size + '\n'
        return res

    def is_solved(self) -> bool:
        for row in self.board:
            for cell in row:
                if len(cell) != 1:
                    return False
        return True
