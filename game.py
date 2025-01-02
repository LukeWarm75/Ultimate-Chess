import sys
import math
import random

import pygame

from scripts.board import Board
from scripts.utils import load_image

SCALE = 1
MARGIN = SCALE * 28
CELL_WIDTH = SCALE * 32
BOARD_SIZE = 10



class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Ultimate Chess")
        self.screen = pygame.display.set_mode((750, 750))
        self.display_1 = pygame.Surface((375, 375), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((750, 147 * SCALE), pygame.SRCALPHA)

        self.clock = pygame.time.Clock()

        self.assets = {
            'b_king': load_image('2d_pieces/b_king.png'),
            'b_queen': load_image('2d_pieces/b_queen.png'),
            'b_castle': load_image('2d_pieces/b_castle.png'),
            'b_juggernaut': load_image('2d_pieces/b_juggernaut.png'),
            'b_pawn': load_image('2d_pieces/b_pawn.png'),
            'b_antiquarian': load_image('2d_pieces/b_antiquarian.png'),
            'b_cryomancer': load_image('2d_pieces/b_cryomancer.png'),
            'b_electromancer': load_image('2d_pieces/b_electromancer.png'),
            'b_pyromancer': load_image('2d_pieces/b_pyromancer.png'),
            'b_terramancer': load_image('2d_pieces/b_terramancer.png'),
            'b_paladin': load_image('2d_pieces/b_paladin.png'),
            'b_dragon': load_image('2d_pieces/b_dragon.png'),
            'b_hydra': load_image('2d_pieces/b_hydra.png'),
            'b_custodian': load_image('2d_pieces/b_custodian.png'),
            'b_samurai': load_image('2d_pieces/b_samurai.png'),
            'b_necromancer': load_image('2d_pieces/b_necromancer.png'),
            'b_zoemancer': load_image('2d_pieces/b_zoemancer.png'),
            'w_king': load_image('2d_pieces/w_king.png'),
            'w_queen': load_image('2d_pieces/w_queen.png'),
            'w_castle': load_image('2d_pieces/w_castle.png'),
            'w_juggernaut': load_image('2d_pieces/w_juggernaut.png'),
            'w_pawn': load_image('2d_pieces/w_pawn.png'),
            'w_antiquarian': load_image('2d_pieces/w_antiquarian.png'),
            'w_cryomancer': load_image('2d_pieces/w_cryomancer.png'),
            'w_electromancer': load_image('2d_pieces/w_electromancer.png'),
            'w_pyromancer': load_image('2d_pieces/w_pyromancer.png'),
            'w_terramancer': load_image('2d_pieces/w_terramancer.png'),
            'w_paladin': load_image('2d_pieces/w_paladin.png'),
            'w_dragon': load_image('2d_pieces/w_dragon.png'),
            'w_hydra': load_image('2d_pieces/w_hydra.png'),
            'w_custodian': load_image('2d_pieces/w_custodian.png'),
            'w_samurai': load_image('2d_pieces/w_samurai.png'),
            'w_necromancer': load_image('2d_pieces/w_necromancer.png'),
            'w_zoemancer': load_image('2d_pieces/w_zoemancer.png'),
            '2d_board': load_image('boards/2D_board.png'),
            'selected_marker': load_image('markers/selected_marker.png'),
            'enemy_marker': load_image('markers/enemy_marker.png'),
            'move_marker': load_image('markers/move_marker.png'),
            'teleport_marker': load_image('markers/teleport_marker.png'),
            'selected_back': load_image('markers/selected_back.png'),
            'enemy_back': load_image('markers/enemy_back.png'),
            'move_back': load_image('markers/move_back.png'),
            'teleport_back': load_image('markers/teleport_back.png')
        }

        self.board = Board(self, (0, 0), BOARD_SIZE, CELL_WIDTH, MARGIN, SCALE)

        self.counter = 0

    def run(self):

        while True:

            self.board.render(self.display_1)
            if self.board.moving:
                self.board.visual_move()

            if not self.board.white:
                kill_moves = []
                for i in range(BOARD_SIZE):
                    for j in range(BOARD_SIZE):
                        piece = self.board.board[i][j]
                        if piece < 0:
                            self.board.selected_piece = (i, j)
                            moves = self.board.get_moves(self.board.selected_piece)
                            print(self.board.markers)
                            for marker in self.board.markers:
                                if marker[1] == 'enemy':
                                    move = ((int((marker[0][1] - MARGIN - SCALE / 3 - CELL_WIDTH / 2) / CELL_WIDTH), int((marker[0][0] - MARGIN - SCALE / 3 - CELL_WIDTH / 2) / CELL_WIDTH)), self.board.selected_piece)
                                    kill_moves.append(move)
                if kill_moves:
                    move = random.choice(kill_moves)
                    self.board.set_move(move[0], move[1])
                else:
                    while True:
                        pos = (random.randint(0, 9), random.randint(0, 9))
                        piece = self.board.board[pos[0]][pos[1]]
                        if piece < 0:
                            self.board.selected_piece = pos
                            moves = self.board.get_moves(self.board.selected_piece)
                            if moves:
                                move = random.choice(moves)
                                self.board.set_move(move, self.board.selected_piece)
                                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if pos[0] < MARGIN*2 or pos[0] > self.screen.get_width() - MARGIN*2 or pos[1] < MARGIN*2 or pos[1] > self.screen.get_height() - MARGIN*2: continue
                    xpos = (pos[0] - MARGIN * 2) // (CELL_WIDTH * 2)  # factor of 2 is because the screen is 2x bigger than the display
                    ypos = (pos[1] - MARGIN * 2) // (CELL_WIDTH * 2)  # don't hard code the 2 in
                    if not self.board.state and (self.board.white and self.board.board[ypos][xpos] > 0):
                        self.board.selected_piece = (ypos, xpos)
                        self.board.show_options()
                        self.board.state = True
                    elif self.board.state:
                        self.board.set_move((ypos, xpos), self.board.selected_piece)

            self.screen.blit(pygame.transform.scale(self.display_1, self.screen.get_size()), (0, 0))

            pygame.display.update()
            self.clock.tick(60)


Game().run()
