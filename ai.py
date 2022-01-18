import random


class AI:
    def __init__(self, player, board):
        self.player = player
        self.board = board
        self.near_score = 0

    def update_board(self):
        self.board = board

    def calc_near_score(self, point):
        score = 0
        p_x, p_y = point
        for x, y in self.board.get_player_positions(self.player):
            score += (p_x-x)**2 + (p_y-y)**2
        
        return score
    
    def calc_near_score_move_diff(self,point, c_x, c_y, t_x, t_y):
        x, y = point
        curr_dist = (x-c_x)**2 + (y-c_y)**2
        future_dist = (x-t_x)**2 + (y-t_y)**2
    
        return future_dist - curr_dist 



    def make_random_move(self):
        moves = []
        for x, y in self.board.get_player_positions(self.player):
            for t_x, t_y in self.board.get_legal_moves(x,y):
                moves.append((x, y, t_x, t_y))

        x, y, t_x, t_y = random.choice(moves)
        #print(f"AI moved: ({x}, {y}), to ({t_x}, {t_y})")
        self.board.move(x, y, t_x, t_y)
        return (x, y, t_x, t_y)
                
    def make_closer_move(self, point):

        moves = []
        min_move = None
        min_value = 999999
        #print(f"Player: {self.player} possible moves:")
        for x, y in self.board.get_player_positions(self.player):
            #print(x,y)
            for t_x, t_y in self.board.get_legal_moves(x,y, False, []):
                score = self.calc_near_score_move_diff(point,x,y,t_x,t_y) 
                #print(f"\t-Diff: {score}, ({x}, {y}) -> ({t_x}, {t_y})")
                if score < min_value:
                    min_move = (x,y,t_x,t_y)
                    min_value = score 

        x,y,t_x,t_y = min_move 
        #print(f"Chose: Diff: {min_value}, ({x}, {y}) -> ({t_x}, {t_y})")
        self.board.move(x, y, t_x, t_y)

        return (x,y,t_x,t_y)
