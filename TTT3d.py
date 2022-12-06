import numpy as np

class TTT3d():

    def __init__(self, state=None):
        if state is None:
            state = np.zeros((4,4,4)).astype('int')
        hh, ww, dd  = state.shape
        if hh != 4 or ww != 4 or dd != 4:
            raise Exception('Please input 4x4x4 array')
        self.state = np.array(state)


    def __str__(self):
        state = self.state
        hh, ww, dd  = state.shape
        print_state = state.copy().tolist()
        for i in range(hh):
            for j in range(ww):
                for k in range(dd):
                    if state[i][j][k] == 1:
                        print_state[i][j][k] = 'X'
                    elif state[i][j][k] == 2:
                        print_state[i][j][k] = 'O'
                    else:
                        print_state[i][j][k] = ' '

        printstr = '\n'
        for i in range(hh):
            printstr += f'[{print_state[i][0][0]}][{print_state[i][1][0]}][{print_state[i][2][0]}][{print_state[i][3][0]}] '
            printstr += f'[{print_state[i][0][1]}][{print_state[i][1][1]}][{print_state[i][2][1]}][{print_state[i][3][1]}] '
            printstr += f'[{print_state[i][0][2]}][{print_state[i][1][2]}][{print_state[i][2][2]}][{print_state[i][3][2]}] '
            printstr += f'[{print_state[i][0][3]}][{print_state[i][1][3]}][{print_state[i][2][3]}][{print_state[i][3][3]}]\n'
        
        return printstr


    def detect_row_state(self, player):
        state = self.state
        hh, ww, dd  = state.shape
        r_one = 0
        r_two = 0
        r_three = 0
        r_four = 0
        draw_list = []

        # check layers on each axis
        for l in range(dd):
            r_found = self.__detect_face(player, axis=0, layer=l)
            r_one += r_found[0]
            r_two += r_found[1]
            r_three += r_found[2]
            r_four += r_found[3]
            draw_list.append(r_found[4])
        
        for l in range(ww):
            r_found = self.__detect_face(player, axis=1, layer=l)
            r_one += r_found[0]
            r_two += r_found[1]
            r_three += r_found[2]
            r_four += r_found[3]
            draw_list.append(r_found[4])

        for l in range(hh):
            r_found = self.__detect_face(player, axis=2, layer=l)
            r_one += r_found[0]
            r_two += r_found[1]
            r_three += r_found[2]
            r_four += r_found[3]
            draw_list.append(r_found[4])

        #check digonals
        r_found = self.__check_row(ind=np.array([0,0,0]), ittr_hor=np.array([0,1,0]), ittr_vert=np.array([1,0,0]), ittr_depth=np.array([0,0,1]), player=player)
        r_one += r_found[0]
        r_two += r_found[1]
        r_three += r_found[2]
        r_four += r_found[3]
        draw_list.append(r_found[4])

        r_found = self.__check_row(ind=np.array([3,0,0]), ittr_hor=np.array([0,1,0]), ittr_vert=np.array([-1,0,0]), ittr_depth=np.array([0,0,1]), player=player)
        r_one += r_found[0]
        r_two += r_found[1]
        r_three += r_found[2]
        r_four += r_found[3]
        draw_list.append(r_found[4])

        r_found = self.__check_row(ind=np.array([0,3,0]), ittr_hor=np.array([0,-1,0]), ittr_vert=np.array([1,0,0]), ittr_depth=np.array([0,0,1]), player=player)
        r_one += r_found[0]
        r_two += r_found[1]
        r_three += r_found[2]
        r_four += r_found[3]
        draw_list.append(r_found[4])

        r_found = self.__check_row(ind=np.array([3,3,0]), ittr_hor=np.array([0,-1,0]), ittr_vert=np.array([-1,0,0]), ittr_depth=np.array([0,0,1]), player=player)
        r_one += r_found[0]
        r_two += r_found[1]
        r_three += r_found[2]
        r_four += r_found[3]
        draw_list.append(r_found[4])

        draw = all(draw_list)

        return r_one, r_two, r_three, r_four, draw
        


    def __detect_face(self, player, axis, layer):
        ind = np.zeros(3).astype('int')
        if axis == 0:
            itr_right = np.array([0,1, 0])
            itr_down = np.array([1, 0, 0])
            ind[1] = 3
            ind[2] = layer
        elif axis == 1:
            itr_right = np.array([0, 0, 1])
            itr_down = np.array([1, 0, 0])
            ind[2] = 3
            ind[1] = layer
        else:
            itr_right = np.array([0, 1, 0])
            itr_down = np.array([0, 0, 1])
            ind[1] = 3
            ind[0] = layer
        
        r_one = 0
        r_two = 0
        r_three = 0
        r_four = 0
        draw_list = []

        if axis == 0:
            # check virtical rows
            while self.__is_in_bounds(ind[0], ind[1], ind[2]):
                r_found = self.__check_row(ind, None, itr_down, None, player)
                r_one += r_found[0]
                r_two += r_found[1]
                r_three += r_found[2]
                r_four += r_found[3]
                draw_list.append(r_found[4])
                ind += -itr_right
            ind += itr_right
        else:
            ind += -itr_right
            ind += -itr_right
            ind += -itr_right
        
        # check digonal
        r_found = self.__check_row(ind, itr_right, itr_down, None, player)
        r_one += r_found[0]
        r_two += r_found[1]
        r_three += r_found[2]
        r_four += r_found[3]
        draw_list.append(r_found[4])

        if axis != 2:
            # check horizontal
            while self.__is_in_bounds(ind[0], ind[1], ind[2]):
                r_found = self.__check_row(ind, itr_right, None, None, player)
                r_one += r_found[0]
                r_two += r_found[1]
                r_three += r_found[2]
                r_four += r_found[3]
                draw_list.append(r_found[4])
                ind += itr_down
            ind += -itr_down
        else:
            ind += itr_down
            ind += itr_down
            ind += itr_down

        # check digonal
        r_found = self.__check_row(ind, itr_right, -itr_down, None, player)
        r_one += r_found[0]
        r_two += r_found[1]
        r_three += r_found[2]
        r_four += r_found[3]
        draw_list.append(r_found[4])

        draw = all(draw_list)

        return r_one, r_two, r_three, r_four, draw


    def __check_row(self, ind, ittr_hor, ittr_vert, ittr_depth, player):
        if ittr_hor is None:
            ittr_hor = np.zeros(3).astype('int')
        if ittr_vert is None:
            ittr_vert = np.zeros(3).astype('int')
        if ittr_depth is None:
            ittr_depth = np.zeros(3).astype('int')

        state = self.state

        not_player = (player % 2) + 1
        
        r_one = 0
        r_two = 0
        r_three = 0
        r_four = 0

        found = 0
        ind_temp = ind.copy()
        not_row = False
        draw = False
        found_rows = np.zeros(4).astype('int')
        while self.__is_in_bounds(ind_temp[0], ind_temp[1], ind_temp[2]):
            if state[ind_temp[0], ind_temp[1], ind_temp[2]] == not_player:
                not_row = True
                found = 0
            elif state[ind_temp[0], ind_temp[1], ind_temp[2]] == player:
                found += 1
                found_rows[found-1] += 1
                if found > 1:
                    found_rows[found-2] -= 1
            else:
                found = 0
            ind_temp += ittr_hor
            ind_temp += ittr_vert
            ind_temp += ittr_depth
        if not not_row:
            r_one = found_rows[0]
            r_two = found_rows[1]
            r_three = found_rows[2]
            r_four = found_rows[3]

        if not_row and any(row > 0 for row in found_rows):
            draw = True

        return r_one, r_two, r_three, r_four, draw

    def __is_in_bounds(self, i, j, k, l_bound=0, r_bound=4):
        return (i >= l_bound and j >= l_bound and k >= l_bound) and (i < r_bound and j < r_bound and k < r_bound)

    def turn(self, player, ind):
        """
        player can be 1 or 2, ind must be a tuple in format (h,w,d)
        """
        if self.state[ind[0],ind[1],ind[2]] != 0:
            print('space is already occupied')
            return
        self.state[ind[0],ind[1],ind[2]] = player

        return

    def revert_turn(self, ind):
        self.state[ind[0],ind[1],ind[2]] = 0

    def is_game_over(self):
        r1 = self.detect_row_state(player=1)
        r2 = self.detect_row_state(player=2)
        if r1[4] == True:
            return 3
        if r2[3] > 0:
            return 2
        if r1[3] > 0:
            return 1
        return 0

    def possible_moves(self):
        moves = []
        state = self.state
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    if state[i,j,k] == 0:
                        moves.append((i,j,k))
        return moves

    def copy(self):
        state = self.state
        newTTT = TTT3d(state.copy())
        return newTTT


def minimax_step(board, objective_fn, player):
    sim_board = board.copy()
    action_value, move = minimax(True, sim_board, objective_fn, player, alpha=-1000000, beta=1000000, max_layer=4,cur_layer=0)
    return move, action_value


def random_step(board, rng):
    moves = board.possible_moves()
    move_ind = rng.integers(0,len(moves))
    return moves[move_ind]


def minimax(maxim, board, objective_fn, player, alpha, beta, max_layer, cur_layer):
    val = board.is_game_over()
    if val != 0:
        # draw
        if val == 3:
            return 0, None
        # loss/win
        else:
            return objective_fn(board), None
    if max_layer <= cur_layer:
        return objective_fn(board), None
    scores = []
    moves = board.possible_moves()
    for move in moves:
        if alpha >= beta:
            break
        board.turn(player, move)
        score, _ = minimax(not maxim, board, objective_fn, (player % 2) + 1, alpha, beta, max_layer, cur_layer + 1)
        scores.append(score)
        board.revert_turn(move)
        if maxim:
            if score > alpha:
                alpha = score
        else:
            if score < beta:
                beta = score
    
    if maxim:
        max_ind = np.argmax(scores)
        return scores[max_ind], moves[max_ind]
    else:
        min_ind = np.argmin(scores)
        return scores[min_ind], moves[min_ind]


def objective_fc_one(board):
    player1_data = board.detect_row_state(player=1)
    player2_data = board.detect_row_state(player=2)
    if player2_data[3] > 0:
        return -1
    p1_sum = player1_data[0] + 2 * player1_data[1] + 5 * player1_data[2] + 10 * player1_data[3]
    return p1_sum


def objective_fc_two(board):
    player1_data = board.detect_row_state(player=1)
    player2_data = board.detect_row_state(player=2)
    if player2_data[3] > 0:
        return -1
    p1_sum = player1_data[1] + 5 * player1_data[2] + 50 * player1_data[3]
    return p1_sum


def objective_fc_three(board):
    player1_data = board.detect_row_state(player=1)
    player2_data = board.detect_row_state(player=2)
    p1_sum = player1_data[1] + 5 * player1_data[2] + 50 * player1_data[3]
    p2_sum = player2_data[1] + 5 * player2_data[2] + 50 * player2_data[3]
    return p1_sum - p2_sum


def rand_bot_game(objective_fn, seed):
    minimax_player = 1
    rand_player = 2
    player1_turn = True
    board = TTT3d()
    rng = np.random.default_rng(seed)
    turn_count = 0
    obj_value_list = []
    while(not board.is_game_over()):
        if player1_turn:
            turn_count += 1
            move, obj_value = minimax_step(board, objective_fn, minimax_player)
            obj_value_list.append(obj_value)
            board.turn(minimax_player, move)
            print(f'Turn {turn_count}: X to {move}')
            player1_turn = not player1_turn
        else:
            move = random_step(board, rng)
            board.turn(rand_player, move)
            print(f'Turn {turn_count}: O to {move}')
            player1_turn = not player1_turn
    end_val = board.is_game_over()
    if end_val == 1:
        winner = 'Minimax'
        print('Minimax wins!')
    elif end_val == 2:
        winner = 'Random'
        print('Random Wins!')
    else:
        winner = 'Draw'
        print('Draw.')
    return turn_count, winner, board, obj_value_list


def mini_bot_game(objective_fn_test, objective_fn_base):
    player1 = 1
    player2 = 2
    player1_turn = True
    board = TTT3d()
    turn_count = 1
    while(not board.is_game_over()):
        if player1_turn:
            move, _ = minimax_step(board, objective_fn_test, player1)
            board.turn(player1, move)
            print(f'Turn {turn_count}: X to {move}')
            turn_count += 1
            player1_turn = not player1_turn
        else:
            move, _ = minimax_step(board, objective_fn_base, player2)
            board.turn(player2, move)
            print(f'Turn {turn_count}: O to {move}')
            player1_turn = not player1_turn
    end_val = board.is_game_over()
    if end_val == 1:
        winner = 'Test'
        print('Player 1 wins!')
    elif end_val == 2:
        winner = 'Base'
        print('Player 2 Wins!')
    else:
        winner = 'Draw'
        print('Draw.')
    return turn_count, winner, board.state