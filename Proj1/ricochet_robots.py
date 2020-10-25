# ricochet_robots.py: Template para implementação do 1º projeto de Inteligência Artificial 2020/2021.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo al017:
# 93696 Daniel Quintas
# 93750 Ricardo Andrade

from search import Problem, Node, astar_search, breadth_first_tree_search, \
    depth_first_tree_search, greedy_search, recursive_best_first_search, InstrumentedProblem
import sys
import copy
import numpy as np
import math
import time



class RRState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = RRState.state_id
        RRState.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista de abertos nas procuras informadas """
        return self.id < other.id

    def __eq__(self, other):
        return self.board.robots == other.board.robots

    def __hash__(self):
        sorted_keys = self.board.robots.keys()
        values = self.board.robots.values()

        return hash(str(sorted_keys) + str(values))



class Board:
    """ Representacao interna de um tabuleiro de Ricochet Robots. """

    def __init__(self):
        self.size = 0
        self.robots = {}
        self.target = []
        self.walls = {}
        self.cost_board = []
    

    def parsed_to_board(self, size, robots, target, walls):
        """ Recebe os atributos do board parsed e converte para a representacao interna """
        self.size = size
        self.set_walls(walls)
        self.set_target(target[0], target[1])
        self.set_cost_board()
        self.set_robots(robots)
    

    def set_all(self, size, robots, target, walls, cost_board):
        """ Mete os atributos a apontar para os pointers passados como argumentos """
        self.size = size
        self.robots = robots
        self.target = target
        self.walls = walls
        self.cost_board = cost_board


    def set_robots(self, robots):
        """ Adiciona os robots """
        for robot in robots:
            self.set_robot(robot[0], robot[1])


    def set_robot(self, colour, position):
        """ Adiciona um robot """
        self.robots[colour] = position
        pass


    def set_cost_board(self):
        """ Cria o tabuleiro de custos """
        def expand(position):
            """ Expande uma posicao que teve o seu custo alterado e altera o custo de todas as posicoes a que tem acesso """
            cost = self.cost_board[position[0]-1, position[1]-1] + 1

            directions = []
            for e in self.possible_moves_robot(self.target[0], position):
                directions += e[1]
            
            result = []
            original_position = position
            for direction in directions:
                position = original_position
                while ((self.target[0], direction) in self.possible_moves_robot(self.target[0], position)):
                    if direction == 'l' and self.cost_board[position[0]-1, position[1]-2] == -1:
                        position = (position[0], position[1] - 1)
                    elif direction == 'r' and self.cost_board[position[0]-1, position[1]] == -1:
                        position = (position[0], position[1] + 1)
                    elif direction == 'd' and self.cost_board[position[0], position[1]-1] == -1:
                        position = (position[0] + 1, position[1])
                    elif direction == 'u'and self.cost_board[position[0]-2, position[1]-1] == -1:
                        position = (position[0] - 1, position[1])
                    else:
                        break
                    result += [position]
                    self.cost_board[position[0]-1, position[1]-1] = cost
            return result

        self.cost_board = np.full((self.size, self.size), -1, dtype=int)
        self.cost_board[self.target[1][0]-1,self.target[1][1]-1] = 0

        to_expand = [(self.target[1][0], self.target[1][1])]

        while(to_expand):
            next_position = to_expand.pop(0)
            to_expand += expand(next_position)


    def set_walls(self, walls):
        """ Adiciona as walls """
        self.set_outside_walls()

        for wall in walls:
            self.set_wall(wall[0], wall[1])
            if wall[1] == 'r':
                self.set_wall((wall[0][0], wall[0][1] + 1), 'l')
            elif wall[1] == 'l':
                self.set_wall((wall[0][0], wall[0][1] - 1), 'r')
            elif wall[1] == 'u':
                self.set_wall((wall[0][0] - 1, wall[0][1]), 'd')
            elif wall[1] == 'd':
                self.set_wall((wall[0][0] + 1, wall[0][1]), 'u')
        

    def set_outside_walls(self):
        """ Adiciona as walls exteriores """
        for i in range(1, self.size + 1):
            self.set_wall((i, 1), 'l')
            self.set_wall((1, i), 'u')
            self.set_wall((i, self.size), 'r')
            self.set_wall((self.size, i), 'd')


    def set_wall(self, position, side):
        """ Adiciona uma parede """
        if position in self.walls.keys():
            self.walls[position] += side
        else:
            self.walls[position] = [side]


    def set_target(self, colour, position):
        """ Adiciona o target """
        self.target = [colour, position]


    def robot_position(self, robot: str):
        """ Devolve a posição atual do robô passado como argumento. """
        return self.robots[robot]
        pass
    

    def possible_moves(self):
        """ Devolve os movimentos possiveis """
        moves = []
        for robot in self.robots.keys():
            moves += self.possible_moves_robot(robot, self.robot_position(robot))
        
        return moves
    

    def possible_moves_robot(self, robot, position):
        """ Devolve os movimentos possiveis de um dado robot """
        moves = []

        if (position not in self.walls.keys() or 'l' not in self.walls[position]) and (position[0], position[1] - 1) not in self.robots.values():
            moves.append((robot, 'l'))
        if (position not in self.walls.keys() or 'r' not in self.walls[position]) and (position[0], position[1] + 1) not in self.robots.values():
            moves.append((robot, 'r'))
        if (position not in self.walls.keys() or 'u' not in self.walls[position]) and (position[0] - 1, position[1]) not in self.robots.values():
            moves.append((robot, 'u'))
        if (position not in self.walls.keys() or 'd' not in self.walls[position]) and (position[0] + 1, position[1]) not in self.robots.values():
            moves.append((robot, 'd'))
        return moves


    def move_robot(self, action):
        """ Move um robot segundo uma dada direcao """

        robot = action[0]
        position = self.robots[robot]
        direction = action[1]
        
        while ((robot, direction) in self.possible_moves_robot(robot, position)):
            if direction == 'l':
                position = (position[0], position[1] - 1)
            elif direction == 'r':
                position = (position[0], position[1] + 1)
            elif direction == 'd':
                position = (position[0] + 1, position[1])
            elif direction == 'u':
                position = (position[0] - 1, position[1])
            else:
                break

        self.robots[action[0]] = position



def parse_instance(filename: str) -> Board:
    """ Lê o ficheiro cujo caminho é passado como argumento e retorna
    uma instância da classe Board. """
    f = open(filename, 'r')

    board_size = eval(f.readline())

    board_robots = []
    for i in range(4):
        args = f.readline().split(" ")
        board_robots += [[args[0], (eval(args[1]), eval(args[2]))]]

    args = f.readline().split(" ")
    board_target = [args[0], (eval(args[1]), eval(args[2]))]

    board_walls = [] 
    for i in range(eval(f.readline())):
        args = f.readline().replace('\n', ' ').split(" ")
        board_walls += [[(eval(args[0]), eval(args[1])), args[2]]]

    f.close()
        
    board = Board()
    board.parsed_to_board(board_size, board_robots, board_target, board_walls)
    return board



class RicochetRobots(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
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
        robots = copy.deepcopy(state.board.robots)

        board = Board()
        board.set_all(state.board.size, robots, state.board.target, state.board.walls, state.board.cost_board)

        board.move_robot(action)

        return RRState(board)
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

        dx = abs(target_position[0] - robot_position[0])**2
        dy = abs(target_position[1] - robot_position[1])**2
        
        return math.sqrt(dx + dy) + node.state.board.cost_board[robot_position[0]-1][robot_position[1]-1]



if __name__ == "__main__":
    start_time = time.time()
    board = parse_instance(sys.argv[1])
    problem = InstrumentedProblem(RicochetRobots(board))
    # node = breadth_first_tree_search(problem)
    # node = depth_first_tree_search(problem)
    # node = greedy_search(problem)
    # node = astar_search(problem)
    node = recursive_best_first_search(problem)

    print(len(node.solution()))
    for e in node.solution():
        print(e[0], e[1])
    
    print("Time = ",time.time() - start_time)
    print(problem)
    pass