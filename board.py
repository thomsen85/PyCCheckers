class Board:
    '''
    Class for managing a chinese checkers board. 
    
    The class deals with x,y coordinates, where 0,0 is unplayable bottom left,
    and 16,24 is upper right. 12,0 is the lower-most playable field.

    Moves happen through the move(current_x, current_y, to_x, to_y) method
    illigal moves are not controlled but the is_legal_move(current_x,
    current_y, to_x, to_y) method will check.

    Legal moves will be able to be found with the get_legal_moves() method.

    '''
    WIDTH = 25
    HEIGHT = 17

    
    PLAYER_1_POS = [(12,0), (11,1), (13, 1), (10, 2), (12, 2), (14,2), (9, 3),
            (11, 3), (13, 3), (15, 3)]
    PLAYER_2_POS = [(12,16), (11, 15), (13, 15), (10, 14), (12, 14), (14, 14),
            (9, 13), (11, 13), (13, 13), (15, 13)]
    PLAYER_3_POS = []
    PLAYER_4_POS = []
    PLAYER_5_POS = []
    PLAYER_6_POS = [] 


    def __init__(self, players=2):
        self.board = Board.get_empty_board()
        self.players = players
        
        if players == 2:
            self.fill_coordinates(Board.PLAYER_1_POS, 2)
            self.fill_coordinates(Board.PLAYER_2_POS, 3)
        

    def reset(self):
        self.board = Board.get_empty_board()
        if self.players == 2:
            self.fill_coordinates(Board.PLAYER_1_POS, 2)
            self.fill_coordinates(Board.PLAYER_2_POS, 3)

    def fill_coordinates(self, coordinates, value):
        for x, y in coordinates:
            self.set_board_value(x, y, value)
        
    
    def get_board_value(self,  x,   y):
        '''Method for getting the value at given x and y location'''
        return self.board[Board.HEIGHT-1-y][x]

    def set_board_value(self,  x,   y,   value) :
        '''Method for setting a value at given x and y location'''
        self.board[Board.HEIGHT-1-y][x] = value

    def get_player_positions(self, player):
        position = []
        for x in range(Board.WIDTH):
            for y in range(Board.HEIGHT):
                if self.get_board_value(x,y) == player + 1:
                    position.append((x,y))

        return position

    def move(self,  current_x,   current_y,   to_x,   to_y) :
        '''Method for moveing a pisce from one place to another'''
        self.set_board_value(to_x, to_y,
                self.get_board_value(current_x, current_y))

        self.set_board_value(current_x, current_y, 1)
    
    def player_in_territory(self, player, territory):
        for p_x, p_y in getattr(Board, f"PLAYER_{territory}_POS"):
            if self.get_board_value(p_x, p_y) != player+1:
                return False

        return True

    def is_won(self):
        '''
        Returns 0 if nobody has won, 1 if player one and 2 if player two has
        won and so on
        '''
        if self.players == 2:
            if self.player_in_territory(1, 2):
                return 1
            elif self.player_in_territory(2, 1):
                return 2

        return 0
            

    def get_graphical_representation(self):
        string = ""
        for row in self.board:
            for col in row:
                if col == 0:
                    string += " "
    
                elif col == 1:
                    string += "O"

                else:
                    string +=str(col-1)
            string += "\n"

        return string

    def get_legal_moves(self, x, y, jump=False, prev=[]):
        '''
        Method for listing all the legal moves
        '''
        
        # Check that a player is being moved.
        if self.get_board_value(x, y) <= 1 and not jump:
            return []

        
        
        moves = []
        player = self.get_board_value(x, y)
        
        if jump:
            moves.append((x,y))
        else:
            prev = []
        
        for surr_x, surr_y in self.get_surrounding(x,y):
            if self.get_board_value(surr_x, surr_y) == 1 and not jump:
                moves.append((surr_x, surr_y))
            
            elif self.get_board_value(surr_x, surr_y) > 1:
                if not self.get_coord_over_piece(x, y, surr_x, surr_y) is None: 

                    over_x, over_y = self.get_coord_over_piece(x,y,surr_x,surr_y)
                    # print(f"At: {x}, {y}, {prev=}, {over_x}, {over_y}")
                    if self.get_board_value(over_x, over_y) == 1 and not (over_x,
                            over_y) in prev:
                        # print(f"Checking {over_x},{over_y}, {prev=}")
                        prev.append((x,y))
                        moves.extend(self.get_legal_moves(over_x, over_y,
                            True, prev))
        prev = []
        # print("Done: ", moves)
        return moves

    def get_coord_over_piece(self, current_x, current_y, surr_x, surr_y):
        '''
        Method for getting the coordinate over a surrounding piece.
        '''
        
        v_x = surr_x - current_x
        v_y = surr_y - current_y

        x, y = (surr_x + v_x, surr_y + v_y)
 
        if x < 0 or x >= Board.WIDTH or y < 0 or y >= Board.HEIGHT:
            return None
        
        return (x,y)
    

    def get_surrounding(self, x, y):
        '''
        Method for getting all surrounding coordinates, they will not 
        exceed the coordinates of the board, but they may contain zeros (out of
        bounds)
        '''

        points = []
        
        # Left
        if x - 2 >= 0:
            points.append((x-2, y))

        # Up Left
        if x - 1 >= 0 and y + 1 < Board.HEIGHT:
            points.append((x-1, y+1))

        # Up Right
        if x + 1 < Board.WIDTH and y + 1 < Board.HEIGHT:
            points.append((x+1, y+1))

        # Right
        if x + 2 < Board.WIDTH:
            points.append((x+2, y))

        # Down Right
        if x + 1 < Board.WIDTH and y - 1 >= 0:
            points.append((x+1, y-1))

        # Down Left
        if x - 1 >= 0 and y - 1 >= 0:
            points.append((x-1, y-1))
        
        return points

    @staticmethod
    def get_empty_board():
        '''Creates an empty chinese checkers board'''

        star_pattern = [1,2,3,4,13,12,11,10,9,10,11,12,13,4,3,2,1]
        board = []
        for line in star_pattern:
            line_pattern = []
            if line % 2 == 0:
                line_pattern.append(1)
                for _ in range(line//2 - 1):
                    line_pattern.extend([0,1])

                line_pattern.extend([0 for _ in range(Board.WIDTH//2 -
                    (line//2)*2+1)])   
                line_pattern = line_pattern[::-1] + [0] + line_pattern

            else:
                for _ in range(line//2):
                    line_pattern.extend([0,1])

                line_pattern.extend([0 for _ in range(Board.WIDTH//2 -
                    (line//2)*2)])
                line_pattern = line_pattern[::-1] + [1] + line_pattern
        
            board.append(line_pattern)

        return board


if __name__=="__main__":
    board = Board()
    print(board.get_graphical_representation())

    print("(9,3):", board.get_legal_moves(9,3))
    
    board.move(11,3, 10, 4)

    print(board.get_graphical_representation())
    
    print("(9,3):", board.get_legal_moves(9,3))


