import random
import numpy



class Board:
    def __init__(self,x,y,winlength, blank = ' '):
        self.blank = blank
        self.board = [[blank for i in xrange(y)] for j in xrange(x)]
        self.winlength = winlength

    def clear(self):
        self.board = [[self.blank for i in j] for j in self.board]
        #change this to change the value of each element in self.board
        #to ' ' instead of creating an entirely new list.

    def visualize(self):
        #for column in [list(i) for i in reversed(zip(*self.board))]:
        #    print '|' + ".".join(column) + '|'

        print '\n'.join(['|' + ".".join(column) + '|' for column in [list(i) for i in reversed(zip(*self.board))]])
    def vis_with_num(self):
        self.visualize()
        print ' ' + ' '.join([str(x%10) for x in range(len(self.board))]) + ' '
    def is_game_over_with_piece(self,x,y): #or do I make piece a class?
        #bad implementation probably
        piece_value = self.board[x][y]
        for streak in self.get_surrounding_streaks([piece_value],x,y):
            if streak >= self.winlength:
                return piece_value

        if self.col_is_full(self.board[x]):
            for i in self.board:
                if not self.col_is_full(i):
                    break
            else:
                return self.blank

    def col_is_full(self,col):
        if self.blank in col:
            return False
        else:
            return True        #replace usage of this with next_space and delete this method.

    def get_surrounding_streaks(self,values,x,y): #either pass a parameter count_spaces = False OR change the value paramater to values list. 
        if self.board[x][y] in values:
            startat = 1
        else:
            startat = 0
        for hor_dif,ver_dif in [(1,0),(1,1),(0,1),(-1,1)]:
            streak = startat + self.get_streak(values, x, y, hor_dif, ver_dif) + self.get_streak(values, x, y, -1*hor_dif, -1*ver_dif)
            yield streak

    def get_bi_streaks(self, values, x, y, hor_dif, ver_dif):
        if self.board[x][y] in values:
            startat = 1
        else:
            startat = 0
        return startat + self.get_streak(values, x, y, hor_dif, ver_dif) + self.get_streak(values, x, y, -1*hor_dif, -1*ver_dif)

    def get_streak(self,values,x,y,hor_dif,ver_dif,streak=0):
        newx, newy = x+hor_dif, y+ver_dif
        try:
            if newx>=0 and newy>=0 and self.board[newx][newy] in values:
                return self.get_streak(values,newx,newy,hor_dif,ver_dif,streak+1)
            else:
                return streak
        except IndexError:
            return streak

    def next_space(self,col):
        for index, space in enumerate(col):
            if space == self.blank:
                return index
        return False

    def add_piece(self,col_num,piece): #move piece to first parameter
        next_space = self.next_space(self.board[col_num])
        if next_space is not False:
            self.board[col_num][next_space] = piece
            return col_num, next_space
        else:
            return False
#todo: make  piece class which is basically a node
# - it should basically have 8 tuples for streaks (or 4).  dunno if each pair will need to be separated (1,1) and (-1,-1) combined?
# - tuple has 2 streaks: the piece value, and the piece value + blank space.
# - and an "update" method which recomputes its own streak in a certain direction and recursively
# - calls the "update" method of the adjacent piece in that direction.

class Piece:
    def __init__(self,value,x,y,board):
        self.value = value
        self.x = x
        self.y = y

            
    def update_surrounding(self):
        for hor_dif, ver_dif in [(1,0),(1,1),(0,1),(-1,1)]:
            neighbor = board[x+hor_dif, y+ver_dif]
            neighbor.update_surrounding

    def update_next(self, x, y, hor_dif, ver_dif):
        self.neighbors[hor_dif][ver_dif]
        


class Player:
    def __init__(self,value,board,players=None):
        self.value = value
        self.board = board
        self.players = players
    def sort_players(self, players = None):
        """sorts the list so self is the 0th item"""
        if players:
            self.players = players
        self.players.sort(key= lambda x: False if x is self else True)


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

class TrashAI(AI):
    def move(self):
        while True:
            col_num = numpy.random.binomial(len(self.board.board)-1,0.5)
            if not self.board.col_is_full(self.board.board[col_num]):
            #get col_is_full to accept col num instead?
                #print ' '*(1 + col_num * 2) + 'V'
                return self.board.add_piece(col_num, self.value)

class DumbAI(AI):
    def move(self):
        streaks = [max(x) for x in zip(*[list(self.max_surrounding_streaks(player.value)) for player in self.players])]
        if max(streaks) > 0:
            return self.board.add_piece(streaks.index(max(streaks)), self.value)
        else:
            while True:
                col_num = numpy.random.binomial(len(self.board.board)-1,0.5)
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
                yield max(self.board.get_surrounding_streaks([value],col_num,next_space))
            else:
                yield False

class InfantAI(DumbAI):
    """This AI is as smart as a 3 year old.
    It plays like dumbAI (placing its piece where it creates the longest streak of its own pieces
    OR prevents a longer streak of opponent pieces), BUT without as extreme short-sightedness, because
    3yoAI will not place a piece that will allow its opponent to win the game immediately."""
    def move(self):
        streaks = [max(x) for x in zip(*[list(self.max_surrounding_streaks(player.value)) for player in self.players])]
        sorted_streaks = sorted(enumerate(streaks), key = lambda x: x[1], reverse = True) #(index, streak value) ordered by highest value first.
        if sorted_streaks[0][1] <= 0: #CHANGE THIS TO A SUPER CALL FROM SHITAI
            while True:
                col_num = numpy.random.binomial(len(self.board.board)-1, 0.5)
                if not self.board.col_is_full(self.board.board[col_num]):
                #get col_is_full to accept col num instead?
                #print ' '*(1 + col_num * 2) + 'V'
                    return self.board.add_piece(col_num, self.value)
        for considered_column in sorted_streaks:
            if considered_column[1] is not False:
                if (not self.board.next_space(self.board.board[considered_column[0]]) + 1 < len(self.board.board[considered_column[0]])) or (
                    considered_column[1] >= self.board.winlength - 1) or all([max(self.board.get_surrounding_streaks(
                        [player.value],considered_column[0], self.board.next_space(
                        self.board.board[considered_column[0]]) + 1)) < self.board.winlength - 1 for player in self.players]):
                    return self.board.add_piece(considered_column[0], self.value)
        else:
            return self.board.add_piece(sorted_streaks[0][0], self.value) #this should prefer blocking self over losing immediately
            
class ToddlerAI(InfantAI):
    #sort this way:
    #1. streaks of n length of my own piece. (max)
    #2. streaks of n length of opponent's piece. (max)
    #3. streaks of n-1 length of my own piece that is also a streak of at least win_length for the values [self.value, blank].
    #4. streaks of n-1 length of opponent's piece that is also a streak of at least win_length for the values [self.value, blank].
    #5. streaks of n-2 length that are like #3 et ak
    #6. streaks of n-2 length that are like #4 et al.
    # . streaks of n-1 length of my own piece that aren't a streak of at least win_length for [self.value, blank] (?)
    def move(self):
        
        streaks = zip(*[list(self.max_surrounding_streaks(player.value)) for player in self.players])
        sorted_streaks = sorted(enumerate(streaks), key = lambda x: (False, max(x[1]), x[1][0]), reverse = True)
        #(index, (mystreak, oppstreak)) ordered by highest value first, mystreak higher priority than oppstreak.
        print sorted_streaks
        if max(sorted_streaks[0][1]) <= 0: #CHANGE THIS TO A SUPER CALL FROM SHITAI
            while True:
                col_num = numpy.random.binomial(len(self.board.board)-1, 0.5)
                if not self.board.col_is_full(self.board.board[col_num]):
                #get col_is_full to accept col num instead?
                #print ' '*(1 + col_num * 2) + 'V'
                    return self.board.add_piece(col_num, self.value)
        for considered_column in sorted_streaks: #todo: clean this up more.  make it more readable.
            if max(considered_column[1]) is not False:
                if (not self.board.next_space(self.board.board[considered_column[0]]) + 1 < len(self.board.board[considered_column[0]])) or (
                    max(considered_column[1]) >= self.board.winlength - 1) or all([max(self.board.get_surrounding_streaks(
                        [player.value],considered_column[0], self.board.next_space(
                        self.board.board[considered_column[0]]) + 1)) < self.board.winlength - 1 for player in self.players]):
                    return self.board.add_piece(considered_column[0], self.value)
        else:
            return self.board.add_piece(sorted_streaks[0][0], self.value) #this should prefer blocking self over losing immediately

    def max_surrounding_streaks(self, value = None):
        if value is None:
            value = self.value
        for col_num, col in enumerate(self.board.board):
            next_space = self.board.next_space(col)
            if next_space is not False:

                yield max(self.board.get_surrounding_streaks([value],col_num,next_space))
            else:
                yield False

    def potential(self, value, x, y, hor_dif, ver_dif):
        if self.board.get_bi_streaks([value,self.board.blank],x,y,hor_dif,ver_dif) > self.winlength:
            return True
        else:
            return False
        



#when opponent plays a move, look for streaks surrounding the piece which is
#freshly opened up - aka the space directly above the piece that the opponent
#just played.  Instead of just streaks of one value, modify get_streak() to look for
#streaks of all values besides opponent values - aka, if AI is 'x', look for streaks
#of all blank spaces and 'x's.

class Game:
    def __init__(self,x,y,winlen,blank = ' '):
        self.game_board = Board(x,y,winlen, blank= ' ')
        self.players = [Human('#',self.game_board), ToddlerAI('O',self.game_board)]
        for player in self.players:
            player.sort_players(self.players[:])
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

    def sandbox(self):
        oldplayers = self.players
        print oldplayers
        self.players = [Human('#',self.game_board), Human('O',self.game_board)]
        self.play()
        self.players = oldplayers
        print self.players
        

g = Game(7,6,4)
print g.play()

def test(amt):
    counter = {'#':0, 'O':0, ' ':0}
    for i in xrange(amt):
        g.game_board.clear()
        counter[g.play()]+=1
    return counter
