import copy, sys

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
        self.weigh_stones = []
        self.map_matrix = []
        self.current_position = None
        self.position_stones = []


    # 1, 2, 3...: index of stone
    # 0: empty space
    # -1: user
    # -2: destination
    # self.weigh_stones[self.map_matrix[y][x]] 
    def set_map_matrix(self, raw_map_data: list, weigh_stones: list):
        self.map_matrix = copy.deepcopy(raw_map_data)
        self.weigh_stones = [None] + copy.deepcopy(weigh_stones) # 0 is empty space, 1 is the first stone
        self.position_stones = [None] * (len(weigh_stones) + 1)
        num_weigh_stones = 0

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
                    num_weigh_stones += 1
                    self.map_matrix[i][j] = num_weigh_stones
                    self.position_stones[num_weigh_stones] = (i, j)

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
    
    def get_weigh_stones(self):
        return self.weigh_stones
    
    def copy(self) -> 'MapData':
        new_map = MapData()
        new_map.set_map_matrix(self.map_matrix, self.weigh_stones)
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
        
        if self.map_matrix[next_x][next_y] > 0: # stone
            if self.map_matrix[next_next_x][next_next_y] > 0 \
                or self.map_matrix[next_next_x][next_next_y] == self.BLOCKER \
                or self.map_matrix[next_next_x][next_next_y] == self.DONE_SWITCH:
                return False
            
            if self.map_matrix[next_next_x][next_next_y] == self.SPACE:
                if self.map_matrix[next_x][next_y] > 0:
                    self.map_matrix[next_next_x][next_next_y] = self.map_matrix[next_x][next_y]
                elif self.map_matrix[next_x][next_y] == self.DONE_SWITCH:
                    # find stone at (next_x, next_y) using find function
                    index = self.position_stones.index((next_x, next_y))
                    self.map_matrix[next_next_x][next_next_y] = index

            elif self.map_matrix[next_next_x][next_next_y] == self.SWITCH:
                self.map_matrix[next_next_x][next_next_y] = self.DONE_SWITCH

            # update the position of the stone
            stone = self.map_matrix[next_x][next_y]
            if stone > 0:
                self.position_stones[stone] = (next_next_x, next_next_y)
            elif stone == self.DONE_SWITCH:
                # find the stone that was on the switch by looking at the position of the switch
                for i in range(1, len(self.position_stones)):
                    if self.position_stones[i] == (next_x, next_y):
                        self.position_stones[i] = (next_next_x, next_next_y)
            else:
                print("Invalid stone position")
                sys.exit(1)
                

        if self.map_matrix[next_x][next_y] == self.DONE_SWITCH or self.map_matrix[next_x][next_y] == self.SWITCH:
            self.map_matrix[next_x][next_y] = self.ARES_ON_SWITCH
        elif self.map_matrix[next_x][next_y] > 0 or self.map_matrix[next_x][next_y] == self.SPACE:
            self.map_matrix[next_x][next_y] = self.map_matrix[x][y]

        if self.map_matrix[x][y] == self.ARES_ON_SWITCH:
            self.map_matrix[x][y] = self.SWITCH
        elif self.map_matrix[x][y] == self.USER:
            self.map_matrix[x][y] = self.SPACE
            
        self.current_position = (next_x, next_y)

        return True