import arcade
from board import Board
from ai import AI
import random

TITLE = "Kinasjakk"
WIDTH = 800
HEIGHT = 800


class Grid:
    COLOR = arcade.color.BLACK 
    def __init__(self, board, width, height):
        self.width = width
        self.height = height 

        self.shapes = arcade.ShapeElementList()
        self.radius = 1.1 * min(width, height) / (len(board)+1) 
        self.rows = len(board)
        self.cols = len(board[0])
        
        self.x_dist = width / (self.cols+1) 
        self.y_dist = height / (self.rows+1)


        for row in range(self.rows):
            for col in range(self.cols):
                if board[row][col] != 0:
                    x, y = self.row_col_to_x_y(row, col)
                    shape = arcade.create_ellipse(x, y, self.radius, self.radius,
                            Grid.COLOR)
                    self.shapes.append(shape)
    
    def draw(self): 
        self.shapes.draw()

    def row_col_to_x_y(self, row, col):
        return (col + 1) * self.x_dist, (self.rows - row) * self.y_dist 
    def x_y_to_coord_x_y(self, x, y):
        return (x+1) * self.x_dist, (y+1) * self.y_dist

    def coord_x_y_to_x_y(self, x, y):
        x_coord = x * self.cols // self.width 
        y_coord = y * self.rows // self.height 
        return x_coord, y_coord

class GUI:
    PLAYER_1_COLOR = arcade.color.BLUE
    PLAYER_2_COLOR = arcade.color.YELLOW

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.board = Board()
        self.grid = Grid(self.board.board, width, height)
        self.ai1 = AI(1, self.board)
        self.ai2 = AI(2, self.board) 

        self.ai_play = False
        self.player = 1

        self.selected_piece = None

    def draw(self):
        self.grid.draw()
        self.draw_players()

        if self.board.is_won():
            arcade.draw_text(str(self.board.is_won()), self.width/2,
                    self.height/2,arcade.color.BLUE, 100)
        
        if not self.selected_piece is None:
            sel_x, sel_y = self.selected_piece
            move_coords = [self.grid.x_y_to_coord_x_y(m[0], m[1]) for m in
                self.board.get_legal_moves(sel_x, sel_y)]
            if len(move_coords) > 0:
                arcade.draw_points(move_coords, arcade.color.WHITE, 10)

            sel_x, sel_y = self.grid.x_y_to_coord_x_y(sel_x, sel_y)
            arcade.draw_circle_filled(sel_x, sel_y, self.grid.radius/2,
                    arcade.color.WHITE)

    
    def start_ai_play(self):
        p_r = 0.5

        if random.random() > p_r:
            self.ai1.make_random_move()
        else:
            self.ai1.make_closer_move((12,26))
        
        if random.random() > p_r:
            self.ai2.make_random_move()
        else:
           self.ai2.make_closer_move((12,0))
        
        if self.ai_play:
            self.ai_play = False
        else:
            self.ai_play = True


    def draw_players(self):
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                if self.board.board[row][col] > 1:
                    x, y = self.grid.row_col_to_x_y(row, col)
                    arcade.draw_circle_filled(x, y, self.grid.radius/2,
                    getattr(GUI, f"PLAYER_{self.board.board[row][col]-1}_COLOR"))

    def mouse_press(self, x, y):
        x_coord, y_coord = self.grid.coord_x_y_to_x_y(x,y)
        if self.selected_piece is None:
            if self.board.get_board_value(x_coord, y_coord) == 1 + self.player:
                self.selected_piece = (x_coord, y_coord)
        else:
            curr_x, curr_y = self.selected_piece
            legal_moves = self.board.get_legal_moves(curr_x, curr_y) 
            print(legal_moves)
            if (self.board.get_board_value(x_coord, y_coord) == 1 and
            (x_coord,y_coord) in legal_moves):
                self.board.move(curr_x, curr_y, x_coord, y_coord)
                self.ai2.make_random_move()
                self.selected_piece = None
            else:
                self.selected_piece = None

class Window(arcade.Window):
    def __init__(self, title, width, height):
        super().__init__(width, height, title)
        self.gui = GUI(width, height)
        arcade.set_background_color(arcade.color.APRICOT)

    def on_draw(self):
        arcade.start_render()
        self.gui.draw()

    def on_mouse_press(self, x, y, modifier, symbol):
        self.gui.mouse_press(x, y)

    def on_key_press(self, key, modifier):
        if key == arcade.key.G:
            print("AI STARTING")
            self.gui.start_ai_play()


if __name__=="__main__":
    win = Window(TITLE, WIDTH, HEIGHT)
    arcade.run()

