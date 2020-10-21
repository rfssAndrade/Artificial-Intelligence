# ricochet_robots.py: Template para implementação do 1º projeto de Inteligência Artificial 2020/2021.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo al017:
# 93696 Daniel Quintas
# 93750 Ricardo Andrade

from search import Problem, Node, astar_search, breadth_first_tree_search, \
    depth_first_tree_search, greedy_search
import sys
import copy


class RRState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = RRState.state_id
        RRState.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista de abertos nas procuras informadas """
        return self.id < other.id


class Board:
    """ Representacao interna de um tabuleiro de Ricochet Robots. """
    def __init__(self):
        self.walls = {}
        self.robots = {}
        self.target = []

    def create_outside_walls(self, size):
        for i in range(1, size + 1):
            self.set_wall((i, 1), 'l')
            self.set_wall((1, i), 'u')
            self.set_wall((i, size), 'r')
            self.set_wall((size, i), 'd')

    def set_robot(self, colour, position):
        self.robots[colour] = position
        pass

    def set_wall(self, position, side):
        if position in self.walls.keys():
            self.walls[position] += side
        else:
            self.walls[position] = [side]

    def set_target(self, colour, position):
        self.target = [colour, position]

    def robot_position(self, robot: str):
        """ Devolve a posição atual do robô passado como argumento. """
        return self.robots[robot]
        pass
    
    def possible_moves(self):
        moves = []

        for robot in self.robots.keys():
            position = self.robot_position(robot)
            if (position not in self.walls.keys() or 'l' not in self.walls[position]) and (position[0], position[1] - 1) not in self.robots.values():
                moves.append((robot, 'l'))
            if (position not in self.walls.keys() or 'r' not in self.walls[position]) and (position[0], position[1] + 1) not in self.robots.values():
                moves.append((robot, 'r'))
            if (position not in self.walls.keys() or 'd' not in self.walls[position]) and (position[0] + 1, position[1]) not in self.robots.values():
                moves.append((robot, 'd'))
            if (position not in self.walls.keys() or 'u' not in self.walls[position]) and (position[0] - 1, position[1]) not in self.robots.values():
                moves.append((robot, 'u'))
        return moves

    def move_robot(self, action):
        position = self.robots[action[0]]
        direction = action[1]
        del self.robots[action[0]]
        
        while ((position not in self.walls.keys() or direction not in self.walls[position])):
            if direction == 'l' and (position[0], position[1] - 1) not in self.robots.values():
                    position = (position[0], position[1] - 1)
            elif direction == 'r' and (position[0], position[1] + 1) not in self.robots.values():
                position = (position[0], position[1] + 1)
            elif direction == 'd' and (position[0] + 1, position[1]) not in self.robots.values():
                position = (position[0] + 1, position[1])
            elif direction == 'u' and (position[0] - 1, position[1]) not in self.robots.values():
                position = (position[0] - 1, position[1])
            else:
                break

        self.robots[action[0]] = position


def parse_instance(filename: str) -> Board:
    """ Lê o ficheiro cujo caminho é passado como argumento e retorna
    uma instância da classe Board. """
    f = open(filename, 'r')

    board = Board()
    board.create_outside_walls(eval(f.readline()))

    for i in range(4):
        args = f.readline().split(" ")
        colour = args[0]
        position = (eval(args[1]), eval(args[2]))
        board.set_robot(colour, position)

    args = f.readline().split(" ")
    board.set_target(args[0], (eval(args[1]), eval(args[2])))

    for i in range(eval(f.readline())):
        args = f.readline().replace('\n', ' ').split(" ")
        position = (eval(args[0]), eval(args[1]))
        side = args[2]
        board.set_wall(position, side)

        if side == 'r':
            board.set_wall((position[0], position[1] + 1), 'l')
        elif side == 'l':
            board.set_wall((position[0], position[1] - 1), 'r')
        elif side == 'u':
            board.set_wall((position[0] - 1, position[1]), 'd')
        elif side == 'd':
            board.set_wall((position[0] + 1, position[1]), 'u')

    f.close()
        
    return board
    pass


class RicochetRobots(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        # TODO: self.initial = ...
        self.initial = RRState(board)
        pass

    def actions(self, state: RRState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        return state.board.possible_moves()
        pass

    def result(self, state: RRState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação retornada deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """
        new_board = copy.deepcopy(state.board)
        new_board.move_robot(action)
        return RRState(new_board)
        pass

    def goal_test(self, state: RRState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se o alvo e o robô da
        mesma cor ocupam a mesma célula no tabuleiro. """
        return state.board.robots[state.board.target[0]] == state.board.target[1]
        pass

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        colour = node.state.board.target[0]
        target_position = node.state.board.target[1]
        robot_position = node.state.board.robot_position(colour)
        
        dx = abs(target_position[0] - robot_position[0])
        dy = abs(target_position[1] - robot_position[1])
        
        return node.path_cost * (dx + dy)
        pass


if __name__ == "__main__":
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = parse_instance(sys.argv[1])
    problem = RicochetRobots(board)
    node = astar_search(problem)

    print(len(node.solution()))
    for e in node.solution():
        print(e[0], e[1])
    pass
