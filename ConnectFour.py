class Board:
    def __init__(self,x,y,winlength):
        self.board = [[' ' for i in xrange(y)] for j in xrange(x)]
        self.winlength = winlength
    def visualize(self):
        for column in [list(i) for i in reversed(zip(*self.board))]:
            print '|' + ".".join(column) + '|'
    def vis_with_num(self):
        self.visualize()
        print ' ' + ' '.join([str(x) for x in range(len(self.board))]) + ' '
    def is_game_over_with_piece(self,x,y): #or do I make piece a class?
        #bad implementation probably
        piece_value = self.board[x][y]
        for streak in self.get_surrounding_streaks(piece_value,x,y):
            if streak >= self.winlength:
                return True

        if self.col_is_full(self.board[x]):
            for i in self.board:
                if not self.col_is_full(i):
                    break
            else:
                return True

    def col_is_full(self,col):
        if ' ' in col:
            return False
        else:
            return True        

    def get_surrounding_streaks(self,value,x,y):
        if self.board[x][y] == value:
            startat = 1
        else:
            startat = 0
        for hor_dif,ver_dif in [(1,0),(1,1),(0,1),(-1,1)]:
            streak = startat + self.get_streak(value, x, y, hor_dif, ver_dif) + self.get_streak(value, x, y, -1*hor_dif, -1*ver_dif)
            yield streak
            
    def get_streak(self,value,x,y,hor_dif,ver_dif,streak=0):
        newx, newy = x+hor_dif, y+ver_dif
        try:
            if newx>=0 and newy>=0 and self.board[newx][newy] == value:
                return self.get_streak(value,newx,newy,hor_dif,ver_dif,streak+1)
            else:
                return streak
        except IndexError:
            return streak
    
    def add_piece(self,column,piece):
        for index, space in enumerate(self.board[column]):
            if space == ' ':
                self.board[column][index] = piece
                return column, index
        return False

#class Piece:
#    def __init__(self,value):
#        self.value = value


class Player:
    def __init__(self,value,board):
        self.value = value
        self.board = board


class Human(Player):
    def move(self):
        while True:
            col = raw_input("which column? ")
            if col == 'q':
                return 'quit'
            try:
                col = int(col)
                if col in range(len(self.board.board)):
                    piece = self.board.add_piece(col,self.value)
                    if piece == False:
                        print "that column is full"
                    else:
                        return piece
                else: print "not a valid column"
            except ValueError:
                print "that's not a number.  type 'q' to quit."
            
            

class AI(Player):
    def move(self):
        pass
            
class Game:
    def __init__(self,x,y,winlen):
        self.game_board = Board(x,y,winlen)
        self.players = [Human('X',self.game_board), Human('O',self.game_board)]
        self.turnplnum = 0
        self.turnpl = self.players[self.turnplnum]
        self.play()
    def play(self):
        while True:
            print ''
            self.game_board.vis_with_num()
            turn_res = self.turn()
            if turn_res == 'quit':
                break
            if self.game_board.is_game_over_with_piece(*turn_res):
                print ''
                self.game_board.vis_with_num()
                break
            else:
                newturnplnum = self.turnplnum + 1
                if newturnplnum >= len(self.players):
                    self.turnplnum = 0
                else:
                    self.turnplnum +=1
                self.turnpl = self.players[self.turnplnum]
        
    def turn(self):
        return self.turnpl.move()
        #return self.game_board.add_piece(col,self.turnpl.value)

g = Game(7,6,4)
