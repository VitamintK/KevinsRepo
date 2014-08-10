class Board:
    def __init__(self,x,y,winlength):
        self.board = [[' ' for i in xrange(y)] for j in xrange(x)]
        self.winlength = winlength
    def visualize(self):
        for column in [list(i) for i in reversed(zip(*self.board))]:
            print ".".join(column)
    def check_game_over():
        pass
    def add_piece(self,column,piece):
        for index, space in enumerate(self.board[column]):
            if space == ' ':
                self.board[column][index] = piece
                return True
        else:
            return False

class Game:
    def __init__(self):
        self.game_board = Board(7,6,4)
