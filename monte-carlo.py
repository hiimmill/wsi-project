import math
import random
from itertools import cycle

import game
from game import GameState, Player

c = math.sqrt(2)


def create_random_move(state: GameState) -> GameState:
    player_order = cycle(GameState.PLAYER_ORDER)
    if state.is_finished():
        return state
    current_player = next(player_order)
    possible_moves = state.possible_moves(current_player)
    moves_number = len(possible_moves)
    if moves_number > 0:
        move_x, move_y = possible_moves[random.randint(0, moves_number - 1)]
        state = state.make_move(current_player, move_x, move_y)
    else:
        state = state.pass_move(current_player)
    return state


class Node:
    children: list
    wins: (int, int, int)
    simuls: int
    parent = None
    activePlayer: GameState.PLAYER_ORDER
    state: GameState

    def __init__(self, state=GameState()):
        wins = {0, 0, 0}
        simuls = 0
        game.state = state
        children = []

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def add_win(self, winner):
        if winner == Player.BLACK:
            self.wins[0] += 1
        if winner == Player.WHITE:
            self.wins[1] += 1
        if winner == Player.RED:
            self.wins[2] += 1
        self.simuls += 1

    def add_child(self):
        node = Node(create_random_move(self.state))
        node.parent = self
        self.children.append(node)

    def calc_usb(self) -> float:
        return self.wins / self.simuls + c * math.sqrt(math.log(self.parent.simuls) / self.simuls)

    def simulate(self) -> Player:
        player_order = cycle(GameState.PLAYER_ORDER)
        state = self.state
        for _ in range(4000):
            state = create_random_move(state)
        ret = Player.BLACK
        if state.evaluate_end_game(Player.WHITE) > state.evaluate_end_game(ret):
            ret = Player.WHITE
        if state.evaluate_end_game(Player.RED) > state.evaluate_end_game(ret):
            ret = Player.RED
        return ret


def choose_node(node) -> Node:
    if node.is_leaf():
        return node
    max_node = None
    for nod in node.children:
        if node.is_leaf():
            return nod
        if max_node is None or nod.calc_usb() > max_node.calc_usb():
            max_node = nod
    return choose_node(max_node)


def make_turn(root, n):  # n - number of simulations
    parent = choose_node(root)
    parent.add_child()
    child = parent.children[0]
    for ind in (0, n):
        winner_id = child.simulate()
    p = child
    while p is not None:
        p.add_win(winner_id)
        p = p.parent
    pass


if __name__ == '__main__':
    root = Node()
    print('Hello')
    for _ in (0, 1000):
        make_turn(root, 10)
    print(root.wins)
