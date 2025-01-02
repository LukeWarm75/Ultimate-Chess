import math

import pygame


class Board:
    def __init__(self, game, pos, board_size, cell_width, margin, scale):
        self.game = game
        self.pos = list(pos)
        self.board_size = board_size
        self.cell_width = cell_width
        self.margin = margin
        self.scale = scale
        self.image = self.game.assets['2d_board']
        self.pieces = []
        self.moving_pieces = []
        self.markers = []

        self.state = False
        self.white = True
        self.selected_piece = None

        self.moving = False
        self.new_pos = []
        self.distance = []
        self.start_pos = []
        self.swap = 0
        self.velocity = 0.1

        self.board = [
            [-8, -7, -6, -3, -16, -17, -5, -4, -7, -8],
            [-12, -10, -11, -9, -14, -15, -9, -11, -10, -13],
            [-2, -1, -1, -2, -1, -1, -2, -1, -1, -2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 1, 1, 2, 1, 1, 2, 1, 1, 2],
            [13, 10, 11, 9, 15, 14, 9, 11, 10, 12],
            [8, 7, 4, 5, 16, 17, 3, 6, 7, 8]
        ]

        self.display_board()

    def display_board(self):
        for piece in self.pieces.copy():
            self.pieces.remove(piece)

        for i in range(self.board_size):
            for j in range(self.board_size):
                pos = [j * self.cell_width + self.margin + self.scale / 3 + self.cell_width / 2, i * self.cell_width + self.margin + self.scale / 3 + self.cell_width / 2]
                texture = self.get_texture((i, j))

                if texture:
                    piece = [texture, pos]
                    self.pieces.append(piece)

    def get_texture(self, pos):
        texture = None

        match self.board[pos[0]][pos[1]]:
            case -17: texture = self.game.assets['b_king']
            case -16: texture = self.game.assets['b_queen']
            case -15: texture = self.game.assets['b_hydra']
            case -14: texture = self.game.assets['b_antiquarian']
            case -13: texture = self.game.assets['b_necromancer']
            case -12: texture = self.game.assets['b_zoemancer']
            case -11: texture = self.game.assets['b_paladin']
            case -10: texture = self.game.assets['b_dragon']
            case -9: texture = self.game.assets['b_samurai']
            case -8: texture = self.game.assets['b_castle']
            case -7: texture = self.game.assets['b_juggernaut']
            case -6: texture = self.game.assets['b_cryomancer']
            case -5: texture = self.game.assets['b_electromancer']
            case -4: texture = self.game.assets['b_pyromancer']
            case -3: texture = self.game.assets['b_terramancer']
            case -2: texture = self.game.assets['b_custodian']
            case -1: texture = self.game.assets['b_pawn']
            case 0: texture = None
            case 17: texture = self.game.assets['w_king']
            case 16: texture = self.game.assets['w_queen']
            case 15: texture = self.game.assets['w_hydra']
            case 14: texture = self.game.assets['w_antiquarian']
            case 13: texture = self.game.assets['w_necromancer']
            case 12: texture = self.game.assets['w_zoemancer']
            case 11: texture = self.game.assets['w_paladin']
            case 10: texture = self.game.assets['w_dragon']
            case 9: texture = self.game.assets['w_samurai']
            case 8: texture = self.game.assets['w_castle']
            case 7: texture = self.game.assets['w_juggernaut']
            case 6: texture = self.game.assets['w_cryomancer']
            case 5: texture = self.game.assets['w_electromancer']
            case 4: texture = self.game.assets['w_pyromancer']
            case 3: texture = self.game.assets['w_terramancer']
            case 2: texture = self.game.assets['w_custodian']
            case 1: texture = self.game.assets['w_pawn']

        return texture

    def show_options(self):
        moves = self.get_moves(self.selected_piece)
        if not moves:
            self.state = False
            return

    def set_move(self, pos, selected_piece):
        moves = self.get_moves(selected_piece)
        for i in moves:
            if i[0] == pos[0] and i[1] == pos[1]:
                previous = self.board[pos[0]][pos[1]]  # type of piece on marker
                selected = self.board[self.selected_piece[0]][self.selected_piece[1]]  # type of piece moving
                self.swap = self.piece_swap(previous)
                self.new_pos = (pos[1] * self.cell_width + self.margin + self.scale / 3 + self.cell_width / 2, pos[0] * self.cell_width + self.margin + self.scale / 3 + self.cell_width / 2)
                self.pieces.remove([self.get_texture(self.selected_piece), [self.selected_piece[1] * self.cell_width + self.margin + self.scale / 3 + self.cell_width / 2, self.selected_piece[0] * self.cell_width + self.margin + self.scale / 3 + self.cell_width / 2]])
                self.pieces.append([self.get_texture(self.selected_piece), [self.selected_piece[1] * self.cell_width + self.margin + self.scale / 3 + self.cell_width / 2, self.selected_piece[0] * self.cell_width + self.margin + self.scale / 3 + self.cell_width / 2]])
                if self.swap:
                    self.pieces.remove([self.get_texture(pos), [pos[1] * self.cell_width + self.margin + self.scale / 3 + self.cell_width / 2, pos[0] * self.cell_width + self.margin + self.scale / 3 + self.cell_width / 2]])
                    self.pieces.insert(0, [self.get_texture(pos), [pos[1] * self.cell_width + self.margin + self.scale / 3 + self.cell_width / 2, pos[0] * self.cell_width + self.margin + self.scale / 3 + self.cell_width / 2]])

                self.multi_kill(self.selected_piece, pos)
                self.board[pos[0]][pos[1]] = self.board[self.selected_piece[0]][self.selected_piece[1]]  # change marker to selected piece
                self.board[self.selected_piece[0]][self.selected_piece[1]] = self.piece_swap(previous)  # change original position to the piece on the marker

                if self.is_in_check():
                    self.board[self.selected_piece[0]][self.selected_piece[1]] = selected
                    self.board[pos[0]][pos[1]] = previous
                    break

                self.distance = [self.new_pos[0] - self.pieces[-1][1][0], self.new_pos[1] - self.pieces[-1][1][1]]  # same distance for both pieces
                self.start_pos = tuple(self.pieces[-1][1])
                self.moving = True
                self.white = not self.white
                break
        for marker in self.markers.copy():
            self.markers.remove(marker)
        self.state = False

    def visual_move(self):
        piece_pos = self.pieces[-1][1]
        piece_pos[0] += self.velocity * self.distance[0]
        piece_pos[1] += self.velocity * self.distance[1]
        self.pieces[-1][1] = piece_pos
        distance_travelled = math.sqrt((piece_pos[0] - self.start_pos[0])**2 + (piece_pos[1] - self.start_pos[1])**2)
        total_distance = math.sqrt(self.distance[0]**2 + self.distance[1]**2)

        if self.swap:
            piece_pos = self.pieces[0][1]
            piece_pos[0] -= self.velocity * self.distance[0]
            piece_pos[1] -= self.velocity * self.distance[1]

        if total_distance - distance_travelled <= 0:
            self.new_pos = []
            self.distance = []
            self.start_pos = []
            self.moving = False
            self.display_board()

    def piece_swap(self, previous):
        if self.board[self.selected_piece[0]][self.selected_piece[1]] == 14 or self.board[self.selected_piece[0]][self.selected_piece[1]] == -14:
            return previous

        elif previous == 14 and self.white:
            return 14
        elif previous == -14 and not self.white:
            return -14

        elif 3 <= previous <= 6 and self.white:
            return previous
        elif -6 <= previous <= -3 and not self.white:
            return previous

        else:
            return 0

    def get_moves(self, pos):
        moves = []
        match abs(self.board[pos[0]][pos[1]]):
            case 1: moves = self.get_pawn_moves(pos)
            case 2: moves = self.get_custodian_moves(pos)
            case 3: moves = self.get_terramancer_moves(pos)
            case 4: moves = self.get_pyromancer_moves(pos)
            case 5: moves = self.get_electromancer_moves(pos)
            case 6: moves = self.get_cryomancer_moves(pos)
            case 7: moves = self.get_juggernaut_moves(pos)
            case 8: moves = self.get_castle_moves(pos)
            case 9: moves = self.get_samurai_moves(pos)
            case 10: moves = self.get_dragon_moves(pos)
            case 11: moves = self.get_paladin_moves(pos)
            case 12: moves = self.get_zoemancer_moves(pos)
            case 13: moves = self.get_necromancer_moves(pos)
            case 14: moves = self.get_antiquarian_moves(pos)
            case 15: moves = self.get_hydra_moves(pos)
            case 16: moves = self.get_queen_moves(pos)
            case 17: moves = self.get_king_moves(pos)

        return moves

    def draw_markers(self, selected, move, enemy, teleport):
        markers = []
        if move:
            markers.extend(move)
        if teleport:
            markers.extend(teleport)
        if enemy:
            markers.extend(enemy)
        markers.append(selected)
        for i in markers:
            self.markers.append(((i[0][1] * self.cell_width + self.margin + self.scale / 3 + self.cell_width / 2, i[0][0] * self.cell_width + self.margin + self.scale / 3 + self.cell_width / 2), i[1]))

    def get_king_moves(self, selected_piece):
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]

        move_data = self.append_single_directions(directions, selected_piece)
        moves.extend(move_data[0])
        self.draw_markers((tuple(selected_piece), 'selected'), move_data[1], move_data[2], None)

        return moves

    def get_queen_moves(self, selected_piece):
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]

        move_data = self.append_continuous_directions(directions, selected_piece)
        moves.extend(move_data[0])
        antiquarian_data = self.antiquarian_pos()
        moves.extend(antiquarian_data[0])
        self.draw_markers((tuple(selected_piece), 'selected'), move_data[1], move_data[2], antiquarian_data[1])

        return moves

    def get_hydra_moves(self, selected_piece):
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1), (0, 3), (0, -3), (3, 0), (-3, 0), (3, 3), (-3, 3), (3, -3), (-3, -3)]

        move_data = self.append_single_directions(directions, selected_piece)
        moves.extend(move_data[0])
        antiquarian_data = self.antiquarian_pos()
        moves.extend(antiquarian_data[0])
        self.draw_markers((tuple(selected_piece), 'selected'), move_data[1], move_data[2], antiquarian_data[1])

        return moves

    def get_antiquarian_moves(self, selected_piece):
        moves = []
        teleport_markers = []

        for j in range(self.board_size):
            for i in range(self.board_size // 2):
                k = i
                if self.white:
                    k = self.board_size - 1 - i
                if selected_piece != (k, j) and not self.is_enemy((k, j)) and self.board[k][j] != 17 and self.board[k][j] != -17:
                    moves.append([k, j])
                    teleport_markers.append(((k, j), 'teleport'))
            for i in range(self.board_size // 2):
                k = i
                if not self.white:
                    k = self.board_size - 1 - i
                    if self.board[k][j] < 0 and self.board[k][j] != -17 and self.board[k][j] != -14:
                        moves.append((k, j))
                        teleport_markers.append(((k, j), 'teleport'))
                else:
                    if self.board[k][j] > 0 and self.board[k][j] != 17 and self.board[k][j] != 14:
                        moves.append((k, j))
                        teleport_markers.append(((k, j), 'teleport'))

        self.draw_markers((tuple(selected_piece), 'selected'), None, None, teleport_markers)

        return moves

    def get_necromancer_moves(self, selected_piece):
        moves = []
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

        move_data = self.append_continuous_directions(directions, selected_piece)
        moves.extend(move_data[0])
        antiquarian_data = self.antiquarian_pos()
        moves.extend(antiquarian_data[0])
        self.draw_markers((tuple(selected_piece), 'selected'), move_data[1], move_data[2], antiquarian_data[1])

        return moves

    def get_zoemancer_moves(self, selected_piece):
        moves = []
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

        move_data = self.append_continuous_directions(directions, selected_piece)
        moves.extend(move_data[0])
        antiquarian_data = self.antiquarian_pos()
        moves.extend(antiquarian_data[0])
        self.draw_markers((tuple(selected_piece), 'selected'), move_data[1], move_data[2], antiquarian_data[1])

        return moves

    def get_paladin_moves(self, selected_piece):
        moves = []
        directions = [(2, 1), (-2, 1), (2, -1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2), (0, 1), (0, -1), (1, 0), (-1, 0)]

        move_data = self.append_single_directions(directions, selected_piece)
        moves.extend(move_data[0])
        antiquarian_data = self.antiquarian_pos()
        moves.extend(antiquarian_data[0])
        self.draw_markers((tuple(selected_piece), 'selected'), move_data[1], move_data[2], antiquarian_data[1])

        return moves

    def get_dragon_moves(self, selected_piece):
        moves = []
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0), (2, 2), (-2, 2), (2, -2), (-2, -2)]

        move_data = self.append_single_directions(directions, selected_piece)
        moves.extend(move_data[0])
        antiquarian_data = self.antiquarian_pos()
        moves.extend(antiquarian_data[0])
        self.draw_markers((tuple(selected_piece), 'selected'), move_data[1], move_data[2], antiquarian_data[1])

        return moves

    def get_samurai_moves(self, selected_piece):
        moves = []
        directions = [(2, 1), (-2, 1), (2, -1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2), (1, 1), (-1, 1), (1, -1), (-1, -1)]

        move_data = self.append_single_directions(directions, selected_piece)
        moves.extend(move_data[0])
        antiquarian_data = self.antiquarian_pos()
        moves.extend(antiquarian_data[0])
        self.draw_markers((tuple(selected_piece), 'selected'), move_data[1], move_data[2], antiquarian_data[1])

        return moves

    def get_castle_moves(self, selected_piece):
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        move_data = self.append_continuous_directions(directions, selected_piece)
        moves.extend(move_data[0])
        antiquarian_data = self.antiquarian_pos()
        moves.extend(antiquarian_data[0])
        self.draw_markers((tuple(selected_piece), 'selected'), move_data[1], move_data[2], antiquarian_data[1])

        return moves

    def get_juggernaut_moves(self, selected_piece):
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1), (0, 2), (0, -2), (2, 0), (-2, 0), (2, 2), (-2, 2), (2, -2), (-2, -2)]

        move_data = self.append_single_directions(directions, selected_piece)
        moves.extend(move_data[0])
        antiquarian_data = self.antiquarian_pos()
        moves.extend(antiquarian_data[0])
        self.draw_markers((tuple(selected_piece), 'selected'), move_data[1], move_data[2], antiquarian_data[1])

        return moves

    def get_cryomancer_moves(self, selected_piece):
        moves = []
        teleport_markers = []
        directions = [(1, 1), (-1, -1)]

        for i in range(self.board_size):
            for j in range(self.board_size):
                if ((self.board[i][j] == 5 or self.board[i][j] == 4 or self.board[i][j] == 3) and self.white) or ((self.board[i][j] == -5 or self.board[i][j] == -4 or self.board[i][j] == -3) and not self.white):
                    moves.append((i, j))
                    teleport_markers.append(((i, j), 'teleport'))

        move_data = self.append_continuous_directions(directions, selected_piece)
        moves.extend(move_data[0])
        antiquarian_data = self.antiquarian_pos()
        moves.extend(antiquarian_data[0])
        teleport_markers.extend(antiquarian_data[1])
        self.draw_markers((tuple(selected_piece), 'selected'), move_data[1], move_data[2], teleport_markers)

        return moves

    def get_electromancer_moves(self, selected_piece):
        moves = []
        teleport_markers = []
        directions = [(1, 0), (-1, 0)]

        for i in range(self.board_size):
            for j in range(self.board_size):
                if ((self.board[i][j] == 6 or self.board[i][j] == 4 or self.board[i][j] == 3) and self.white) or ((self.board[i][j] == -6 or self.board[i][j] == -4 or self.board[i][j] == -3) and not self.white):
                    moves.append((i, j))
                    teleport_markers.append(((i, j), 'teleport'))

        move_data = self.append_continuous_directions(directions, selected_piece)
        moves.extend(move_data[0])
        antiquarian_data = self.antiquarian_pos()
        moves.extend(antiquarian_data[0])
        teleport_markers.extend(antiquarian_data[1])
        self.draw_markers((tuple(selected_piece), 'selected'), move_data[1], move_data[2], teleport_markers)

        return moves

    def get_pyromancer_moves(self, selected_piece):
        moves = []
        teleport_markers = []
        directions = [(1, -1), (-1, 1)]

        for i in range(self.board_size):
            for j in range(self.board_size):
                if ((self.board[i][j] == 6 or self.board[i][j] == 5 or self.board[i][j] == 3) and self.white) or ((self.board[i][j] == -6 or self.board[i][j] == -5 or self.board[i][j] == -3) and not self.white):
                    moves.append((i, j))
                    teleport_markers.append(((i, j), 'teleport'))

        move_data = self.append_continuous_directions(directions, selected_piece)
        moves.extend(move_data[0])
        antiquarian_data = self.antiquarian_pos()
        moves.extend(antiquarian_data[0])
        teleport_markers.extend(antiquarian_data[1])
        self.draw_markers((tuple(selected_piece), 'selected'), move_data[1], move_data[2], teleport_markers)

        return moves

    def get_terramancer_moves(self, selected_piece):
        moves = []
        teleport_markers = []
        directions = [(0, 1), (0, -1)]

        for i in range(self.board_size):
            for j in range(self.board_size):
                if ((self.board[i][j] == 6 or self.board[i][j] == 5 or self.board[i][j] == 4) and self.white) or ((self.board[i][j] == -6 or self.board[i][j] == -5 or self.board[i][j] == -4) and not self.white):
                    moves.append((i, j))
                    teleport_markers.append(((i, j), 'teleport'))

        move_data = self.append_continuous_directions(directions, selected_piece)
        moves.extend(move_data[0])
        antiquarian_data = self.antiquarian_pos()
        moves.extend(antiquarian_data[0])
        teleport_markers.extend(antiquarian_data[1])
        self.draw_markers((tuple(selected_piece), 'selected'), move_data[1], move_data[2], teleport_markers)

        return moves

    def get_custodian_moves(self, selected_piece):
        moves = []
        move_markers = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]

        for i in directions:
            pos = list(selected_piece)
            pos[0] += i[0]
            pos[1] += i[1]
            if self.is_valid_position(pos):
                if self.is_empty(pos):
                    moves.append(tuple(pos))
                    move_markers.append((tuple(pos), 'move'))

        antiquarian_data = self.antiquarian_pos()
        moves.extend(antiquarian_data[0])
        self.draw_markers((tuple(selected_piece), 'selected'), move_markers, None, antiquarian_data[1])

        return moves

    def get_pawn_moves(self, selected_piece):
        moves = []
        move_markers = []
        enemy_markers = []
        is_first_move = False

        if self.white: direction = (-1, 0)
        else: direction = (1, 0)

        if (self.white and selected_piece[0] == 7) or (not self.white and selected_piece[0] == 2): is_first_move = True

        pos = list(selected_piece)
        pos[0] += direction[0]
        pos[1] += direction[1]
        if self.is_empty(pos):
            moves.append(tuple(pos))
            move_markers.append((tuple(pos), 'move'))

        pos[1] = selected_piece[1] + 1
        if self.is_valid_position(pos):
            if self.is_enemy(pos) and not self.is_custodian(pos):
                moves.append(tuple(pos))
                move_markers.append((tuple(pos), 'enemy'))
        pos[1] = selected_piece[1] - 1
        if self.is_valid_position(pos):
            if self.is_enemy(pos) and not self.is_custodian(pos):
                moves.append(tuple(pos))
                move_markers.append((tuple(pos), 'enemy'))

        pos[0] = selected_piece[0] + direction[0] * 2
        pos[1] = selected_piece[1]
        if is_first_move and self.is_empty(pos) and self.is_empty((selected_piece[0] + direction[0], selected_piece[1])):
            if not self.is_enemy(pos) and not self.is_enemy((selected_piece[0] + direction[0], selected_piece[1])):
                moves.append(tuple(pos))
                move_markers.append((tuple(pos), 'move'))

        antiquarian_data = self.antiquarian_pos()
        moves.extend(antiquarian_data[0])
        self.draw_markers((tuple(selected_piece), 'selected'), move_markers, enemy_markers, antiquarian_data[1])

        return moves

    def multi_kill(self, selected_piece, pos):
        if ((self.board[selected_piece[0]][selected_piece[1]] == 15 or self.board[selected_piece[0]][selected_piece[1]] == 10) and self.board[pos[0]][pos[1]] != 14) or ((self.board[selected_piece[0]][selected_piece[1]] == -15 or self.board[selected_piece[0]][selected_piece[1]] == -10) and self.board[pos[0]][pos[1]] != -14):
            direction = (
                int((pos[0] - selected_piece[0]) / abs(pos[0] - selected_piece[0]) if pos[0] != selected_piece[0] else 0),
                int((pos[1] - selected_piece[1]) / abs(pos[1] - selected_piece[1]) if pos[1] != selected_piece[1] else 0)
            )
            for i in range(1, max(abs(pos[0] - selected_piece[0]), abs(pos[1] - selected_piece[1]))):
                board = self.board[selected_piece[0] + i * direction[0]][selected_piece[1] + i * direction[1]]
                if (board < 0 and self.white and board != -2) or (board > 0 and not self.white and board != 2):
                    self.board[selected_piece[0] + i * direction[0]][selected_piece[1] + i * direction[1]] = 0

    def is_valid_position(self, pos):
        if 0 <= pos[0] < self.board_size and 0 <= pos[1] < self.board_size: return True
        return False

    def is_empty(self, pos):
        if self.board[pos[0]][pos[1]] == 0: return True
        return False

    def is_enemy(self, pos):
        if (self.white and self.board[pos[0]][pos[1]] < 0) or (not self.white and self.board[pos[0]][pos[1]] > 0): return True
        return False

    def is_custodian(self, pos):
        if self.board[pos[0]][pos[1]] == 2 or self.board[pos[0]][pos[1]] == -2: return True
        return False

    def is_mancer(self, pos):
        if (3 <= self.board[pos[0]][pos[1]] <= 6 and self.white) or (-6 <= self.board[pos[0]][pos[1]] <= -3 and not self.white): return True
        return False

    def antiquarian_pos(self):
        moves = []
        teleport_markers = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 14 and self.white or self.board[i][j] == -14 and not self.white:
                    moves.append((i, j))
                    teleport_markers.append(((i, j), 'teleport'))

        return moves, teleport_markers

    def is_in_check(self):
        king_pos = []
        opp_pieces = []
        hydra = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if (self.board[i][j] == 17 and self.white) or (self.board[i][j] == -17 and not self.white):
                    king_pos = (i, j)
                if (self.board[i][j] < 0 and self.white) or (self.board[i][j] > 0 and not self.white):
                    opp_pieces.append(((i, j), self.board[i][j]))
                if (self.board[i][j] == -15 and self.white) or (self.board[i][j] == 15 and not self.white):
                    self.white = not self.white
                    moves = self.get_hydra_moves((i, j))
                    self.white = not self.white
                    for pos in moves:
                        direction = (int((pos[0] - i) / abs(pos[0] - i) if pos[0] != i else 0), int((pos[1] - j) / abs(pos[1] - j) if pos[1] != j else 0))
                        for k in range(1, max(abs(pos[0] - i), abs(pos[1] - j))):
                            hydra.append((i + k * direction[0], j + k * direction[1]))
                if (self.board[i][j] == -10 and self.white) or (self.board[i][j] == 10 and not self.white):
                    self.white = not self.white
                    moves = self.get_dragon_moves((i, j))
                    self.white = not self.white
                    for pos in moves:
                        direction = (int((pos[0] - i) / abs(pos[0] - i) if pos[0] != i else 0), int((pos[1] - j) / abs(pos[1] - j) if pos[1] != j else 0))
                        for k in range(1, max(abs(pos[0] - i), abs(pos[1] - j))):
                            hydra.append((i + k * direction[0], j + k * direction[1]))
        for piece in opp_pieces:
            self.white = not self.white
            moves = self.get_moves(piece[0])
            self.white = not self.white
            for pos in moves:
                if pos == king_pos:
                    return True
            for pos in hydra:
                if pos == king_pos:
                    return True

        return False

    def append_single_directions(self, directions, selected_piece):
        moves = []
        move_markers = []
        enemy_markers = []
        for i in directions:
            pos = list(selected_piece)
            pos[0] += i[0]
            pos[1] += i[1]
            if self.is_valid_position(pos):
                if self.is_empty(pos):
                    moves.append(tuple(pos))
                    move_markers.append((tuple(pos), 'move'))
                elif self.is_enemy(pos) and not self.is_custodian(pos):
                    moves.append(tuple(pos))
                    enemy_markers.append((tuple(pos), 'enemy'))

        return moves, move_markers, enemy_markers

    def append_continuous_directions(self, directions, selected_piece):
        moves = []
        move_markers = []
        enemy_markers = []
        for i in directions:
            pos = list(selected_piece)
            pos[0] += i[0]
            pos[1] += i[1]
            while self.is_valid_position(pos):
                if self.is_empty(pos):
                    moves.append(tuple(pos))
                    move_markers.append((tuple(pos), 'move'))

                elif self.is_enemy(pos) and not self.is_custodian(pos):
                    moves.append(tuple(pos))
                    enemy_markers.append((tuple(pos), 'enemy'))
                    break
                else:
                    break

                pos[0] += i[0]
                pos[1] += i[1]

        return moves, move_markers, enemy_markers

    def append_mancer_directions(self, directions, selected_piece):
        moves = []
        for i in directions:
            pos = list(selected_piece)
            pos[0] += i[0]
            pos[1] += i[1]
            while self.is_valid_position(pos):
                if self.is_empty(pos) or self.is_mancer(pos):
                    moves.append(tuple(pos))

                elif self.is_enemy(pos) and not self.is_custodian(pos):
                    moves.append(tuple(pos))
                    break
                else:
                    break

                pos[0] += i[0]
                pos[1] += i[1]

        return moves

    def render(self, surf):
        surf.blit(pygame.transform.scale_by(self.image, self.scale), self.pos)
        for marker in self.markers:
            img = self.game.assets[marker[1] + '_marker']
            back = self.game.assets[marker[1] + '_back']
            surf.blit(pygame.transform.scale_by(img, self.scale), (marker[0][0] - img.get_width() / 2, marker[0][1] - img.get_height() / 2))
            surf.blit(pygame.transform.scale_by(back, self.scale), (marker[0][0] - back.get_width() / 2, marker[0][1] - back.get_height() / 2))
        for piece in self.pieces:
            surf.blit(pygame.transform.scale_by(piece[0], self.scale), (piece[1][0] - piece[0].get_width() * self.scale / 2, piece[1][1] - piece[0].get_height() * self.scale / 2))
