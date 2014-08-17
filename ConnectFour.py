import random
import numpy

class Board:
    def __init__(self,x,y,winlength):
        self.board = [[' ' for i in xrange(y)] for j in xrange(x)]
        self.winlength = winlength

    def clear(self):
        self.board = [[' ' for i in j] for j in self.board]
        #change this to change the value of each element in self.board
        #to ' ' instead of creating an entirely new list.

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
                return piece_value

        if self.col_is_full(self.board[x]):
            for i in self.board:
                if not self.col_is_full(i):
                    break
            else:
                return ' '

    def col_is_full(self,col):
        if ' ' in col:
            return False
        else:
            return True        #replace usage of this with next_space and delete this method.

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

    def next_space(self,col):
        for index, space in enumerate(col):
            if space == ' ':
                return index
        return False

    def add_piece(self,col_num,piece): #move piece to first parameter
        next_space = self.next_space(self.board[col_num])
        if next_space is not False:
            self.board[col_num][next_space] = piece
            return col_num, next_space
        else:
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
    pass

class ShitAI(AI):
    def move(self):
        while True:
            col_num = random.randint(0,len(self.board.board)-1)
            if not self.board.col_is_full(self.board.board[col_num]):
            #get col_is_full to accept col num instead?
                #print ' '*(1 + col_num * 2) + 'V'
                return self.board.add_piece(col_num, self.value)

class trashAI(AI):
    def move(self):
        while True:
            col_num = numpy.random.binomial(6,0.5)
            if not self.board.col_is_full(self.board.board[col_num]):
            #get col_is_full to accept col num instead?
                #print ' '*(1 + col_num * 2) + 'V'
                return self.board.add_piece(col_num, self.value)

class dumbAI(AI):
    def move(self):
        streaks = [max(x) for x in zip(list(self.max_surrounding_streaks('O')), list(self.max_surrounding_streaks('X')))]
        if max(streaks) > 0:
            return self.board.add_piece(streaks.index(max(streaks)), self.value)
        else:
            while True:
                col_num = numpy.random.binomial(6,0.5)
                if not self.board.col_is_full(self.board.board[col_num]):
                #get col_is_full to accept col num instead?
                #print ' '*(1 + col_num * 2) + 'V'
                    return self.board.add_piece(col_num, self.value)

    def max_surrounding_streaks(self, value = None):
        if value is None:
            value = self.value
        for col_num, col in enumerate(self.board.board):
            next_space = self.board.next_space(col)
            if next_space is not False:
                yield max(self.board.get_surrounding_streaks(value,col_num,next_space))
            else:
                yield False

class infantAI(dumbAI):
    """This AI is as smart as a 3 year old.
    It plays like dumbAI (placing its piece where it creates the longest streak of its own pieces
    OR prevents a longer streak of opponent pieces), BUT without as extreme short-sightedness, because
    3yoAI will not place a piece that will allow its opponent to win the game immediately."""
    def move(self):
        streaks = [max(x) for x in zip(list(self.max_surrounding_streaks('O')), list(self.max_surrounding_streaks('X')))]
        if max(streaks) > 0:
            if (not self.board.next_space(self.board.board[streaks.index(max(streaks))]) + 1 < len(self.board.board[0])) or (
                max(streaks) >= 3 or (max(self.board.get_surrounding_streaks(
                'O',streaks.index(max(streaks)),
                self.board.next_space(self.board.board[streaks.index(max(streaks))]) + 1)) < 3
                and max(self.board.get_surrounding_streaks(
                'X',streaks.index(max(streaks)),
                self.board.next_space(self.board.board[streaks.index(max(streaks))]) + 1)) < 3)):
                try:
                    print (max(self.board.get_surrounding_streaks(
                    'O',streaks.index(max(streaks)),
                    self.board.next_space(self.board.board[streaks.index(max(streaks))]) + 1)))
                except:
                    print 'top'
                try:
                    print (max(self.board.get_surrounding_streaks(
                    'X',streaks.index(max(streaks)),
                    self.board.next_space(self.board.board[streaks.index(max(streaks))]) + 1)))
                except:
                    print 'top'

                return self.board.add_piece(streaks.index(max(streaks)), self.value)
            else:
                print "not blocking myself! infant power!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                m1, m2 = (None,None), (None,None)
                for ind,x in enumerate(streaks):
                    print x
                    if x > m1[1]:
                        m1, m2 = (ind,x), m1
                    elif x > m2[1] or m2 is False:
                        m2 = (ind,x)
                print m1, ' is best'
                print m2, ' is second best'
                return self.board.add_piece(m2[0], self.value)
            #streaks.index(sorted(streaks)[-2])

        else:
            while True:
                col_num = numpy.random.binomial(6,0.5)
                if not self.board.col_is_full(self.board.board[col_num]):
                #get col_is_full to accept col num instead?
                #print ' '*(1 + col_num * 2) + 'V'
                    return self.board.add_piece(col_num, self.value) 
            

#when opponent plays a move, look for streaks surrounding the piece which is
#freshly opened up - aka the space directly above the piece that the opponent
#just played.  Instead of just streaks of one value, modify get_streak() to look for
#streaks of all values besides opponent values - aka, if AI is 'x', look for streaks
#of all blank spaces and 'x's.

class Game:
    def __init__(self,x,y,winlen):
        self.game_board = Board(x,y,winlen)
        self.players = [infantAI('X',self.game_board), dumbAI('O',self.game_board)]
        self.turnplnum = 0
        self.turnpl = self.players[self.turnplnum]
    def play(self): #make this function better!!!!!
        while True:
            print ''
            self.game_board.vis_with_num()
            turn_res = self.turn()
            if turn_res == 'quit':
                break
            winner = self.game_board.is_game_over_with_piece(*turn_res)
            if winner:
                print ''
                self.game_board.vis_with_num()
                return winner
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
g.play()

def test(amt):
    counter = {'X':0, 'O':0, ' ':0}
    for i in xrange(amt):
        g.game_board.clear()
        counter[g.play()]+=1
    return counter
