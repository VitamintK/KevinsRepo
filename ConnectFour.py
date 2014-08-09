class Board:
    def __init__(self):
        self.board = [['0' for x in xrange(7)] for y in xrange(6)]
    def graph(self):
        for row in self.board:
            print " ".join(row)
