import copy

class MapData:
    SPACE = 0
    BLOCKER = -1
    USER = -2
    SWITCH = -3
    DONE_SWITCH = -4
    ARES_ON_SWITCH = -5

    DIRECTIONS = {
        'u': (-1, 0),
        'd': (1, 0),
        'l': (0, -1),
        'r': (0, 1)
    }

    def __init__(self):
        self.stones = []
        self.map_matrix = []
        self.current_position = None


    # 1, 2, 3...: index of stone
    # 0: empty space
    # -1: user
    # -2: destination
    # self.stones[self.map_matrix[y][x]] 
    def set_map_matrix(self, raw_map_data: list, stones: list):
        self.map_matrix = copy.deepcopy(raw_map_data)
        self.stones = copy.deepcopy(stones)
        num_stones = 0

        for i in range(len(raw_map_data)):
            for j in range(len(raw_map_data[i])):
                if raw_map_data[i][j] == ' ':
                    self.map_matrix[i][j] = self.SPACE
                elif raw_map_data[i][j] == '#':
                    self.map_matrix[i][j] = self.BLOCKER
                elif raw_map_data[i][j] == '@':
                    self.map_matrix[i][j] = self.USER
                    self.current_position = (i, j)
                elif raw_map_data[i][j] == '.':
                    self.map_matrix[i][j] = self.SWITCH
                elif raw_map_data[i][j] == '*':
                    self.map_matrix[i][j] = self.DONE_SWITCH
                elif raw_map_data[i][j] == '+':
                    self.map_matrix[i][j] = self.ARES_ON_SWITCH
                else:
                    num_stones += 1
                    self.map_matrix[i][j] = num_stones

    # convert to #, @, ., and $
    def get_display_map(self):
        display_map = []
        for i in range(len(self.map_matrix)):
            row = []
            for j in range(len(self.map_matrix[i])):
                if self.map_matrix[i][j] == self.SPACE:
                    row.append(' ')
                elif self.map_matrix[i][j] == self.BLOCKER:
                    row.append('#')
                elif self.map_matrix[i][j] == self.USER:
                    row.append('@')
                elif self.map_matrix[i][j] == self.SWITCH:
                    row.append('.')
                elif self.map_matrix[i][j] == self.DONE_SWITCH:
                    row.append('*')
                elif self.map_matrix[i][j] == self.ARES_ON_SWITCH:
                    row.append('+')
                else:
                    row.append('$')
            display_map.append(row)
        return display_map

    def get_map_matrix(self):
        return self.map_matrix
    
    def get_stones(self):
        return self.stones
    
    def copy(self) -> 'MapData':
        new_map = MapData()
        new_map.set_map_matrix(self.map_matrix, self.stones)
        return new_map

    def calculate_heuristic(self) -> int:
        return 0
    
    def move(self, direction: str) -> bool:
        # can move if the next position is not a blocker and not out of bounds
        # can push a stone if the next position is a stone and the position after that is not a blocker or another stone
        # can only push one stone at a time
        x, y = self.current_position
        dx, dy = self.DIRECTIONS[direction]
        next_x, next_y = x + dx, y + dy
        next_next_x, next_next_y = next_x + dx, next_y + dy

        if self.map_matrix[next_x][next_y] == self.BLOCKER:
            return False
        
        if self.map_matrix[next_x][next_y] in self.stones:
            if self.map_matrix[next_next_x][next_next_y] in self.stones or self.map_matrix[next_next_x][next_next_y] == self.BLOCKER:
                return False
            self.stones[self.stones.index(self.map_matrix[next_x][next_y])] = self.map_matrix[next_next_x][next_next_y]

        self.map_matrix[next_x][next_y] = self.map_matrix[x][y]
        self.map_matrix[x][y] = self.SPACE
        self.current_position = (next_x, next_y)

        return True