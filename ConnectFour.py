class Board:
    def __init__(self,x,y,winlength):
        self.board = [[' ' for i in xrange(y)] for j in xrange(x)]
        self.winlength = winlength
    def visualize(self):
        for column in [list(i) for i in reversed(zip(*self.board))]:
            print '|' + ".".join(column) + '|'
    def check_game_over_with_piece(self,x,y): #or do I make piece a class?
        #bad implementation probably
        piece_value = self.board[x][y]
        for streak in self.get_surrounding_streaks(piece_value,x,y):
            if streak >= self.winlength:
                return True
        #check for tie (board full)
        

    def get_surrounding_streaks(self,value,x,y):
        for hor_dif,ver_dif in [(1,0),(1,1),(0,1),(-1,-1)]:
            streak = 1
            if self.board[x+hor_dif][y+ver_dif] == value:
                streak += self.get_streak(value, x+hor_dif, y+ver_dif, hor_dif, ver_dif)
            if self.board[x-hor_dif][y-ver_dif] == value:
                streak += self.get_streak(value, x-hor_dif, y-ver_dif, -1*hor_dif, -1*ver_dif)
            yield streak
            
    def get_streak(self,value,x,y,hor_dif,ver_dif,streak=1):
        if self.board[x+hor_dif][y+ver_dif] == value:
            return self.get_streak(value,x+hor_dif,y+ver_dif,hor_dif,ver_dif,streak+1)
        else:
            return streak
            
    
    def add_piece(self,column,piece):
        for index, space in enumerate(self.board[column]):
            if space == ' ':
                self.board[column][index] = piece
                return (column, index)
        else:
            return False

class Game:
    def __init__(self):
        self.game_board = Board(7,6,4)
