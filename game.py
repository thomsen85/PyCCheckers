import pygame

from board import Board
from minimax_player import MinimaxPlayer

WIDTH = 800
HEIGHT = 800
RADIUS = 20

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
minmax_player = MinimaxPlayer(Board.PLAYER_2_NR)


class Game:
    PLAYER_1_COLOR = "red"
    PLAYER_2_COLOR = "blue"

    def __init__(self):
        self.board = Board()
        self.cell_coords = {}
        self.selected_piece = None
        self.turn = Board.PLAYER_1_NR

    def draw(self, screen):
        self.cell_coords.clear()
        for top, row in enumerate(self.board.board):
            y = Board.HEIGHT - 1 - top
            for x, cell in enumerate(row):
                if cell == 0:
                    continue
                coords = pygame.Vector2(
                    RADIUS * 1.5 + x * ((WIDTH - RADIUS * 1.5) / self.board.WIDTH),
                    RADIUS * 1.5 + top * ((HEIGHT - RADIUS * 1.5) / self.board.HEIGHT),
                )
                self.cell_coords[(x, y)] = coords
                if (x, y) == self.selected_piece:
                    pygame.draw.circle(screen, "green", coords, RADIUS)
                elif cell == Board.PLAYER_1_NR:
                    pygame.draw.circle(screen, self.PLAYER_1_COLOR, coords, RADIUS)
                elif cell == Board.PLAYER_2_NR:
                    pygame.draw.circle(screen, self.PLAYER_2_COLOR, coords, RADIUS)
                else:
                    pygame.draw.circle(screen, "grey", coords, RADIUS)

    def update(self):
        if self.turn == Board.PLAYER_2_NR:
            move = minmax_player.get_best_move(self.board)
            print("Minimax move:", move)
            self.board.move(*move)
            self.turn = Board.PLAYER_1_NR

    def on_click(self, coord):
        for (x, y), cell_coord in self.cell_coords.items():
            if pygame.Vector2(coord).distance_to(cell_coord) < RADIUS:
                self.on_cell_clicked(x, y)
                print(f"Clicked on cell {x}, {y}")
                break

    def on_cell_clicked(self, x, y):
        if self.selected_piece is None:
            if self.board.get_cell(x, y) == Board.PLAYER_1_NR:
                self.selected_piece = (x, y)
        else:
            if (x, y) in self.board.get_legal_moves(*self.selected_piece):
                self.board.move(*self.selected_piece, x, y)
                self.turn = Board.PLAYER_2_NR
                self.selected_piece = None
            else:
                self.selected_piece = None


game = Game()

clicked_last_frame = False
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    game.update()
    game.draw(screen)

    click = pygame.mouse.get_pressed()
    if click[0] and not clicked_last_frame:
        game.on_click(pygame.mouse.get_pos())
        clicked_last_frame = True
    elif not click[0]:
        clicked_last_frame = False

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
