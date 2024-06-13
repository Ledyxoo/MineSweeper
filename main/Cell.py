class Cell:
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

    def set_mine(self, is_mine):
        self.is_mine = is_mine

    def is_mine(self):
        return self.is_mine

    def set_revealed(self, is_revealed):
        self.is_revealed = is_revealed

    def is_revealed(self):
        return self.is_revealed

    def set_flagged(self, is_flagged):
        self.is_flagged = is_flagged

    def is_flagged(self):
        return self.is_flagged

    def set_adjacent_mines(self, adjacent_mines):
        self.adjacent_mines = adjacent_mines
