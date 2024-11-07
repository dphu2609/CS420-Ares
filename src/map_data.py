import copy

class MapData:
    SPACE = 0
    BLOCKER = -1
    USER = -2
    SWITCH = -3
    DONE_SWITCH = -4
    ARES_ON_SWITCH = -5

    def __init__(self):
        self.stones = []
        self.map_matrix = []


    # 1, 2, 3...: index of stone
    # 0: empty space
    # -1: user
    # -2: destination
    # self.stones[self.map_matrix[y][x]] 
    def set_map_matrix(self, raw_map_data: list, stones: list):
        self.map_matrix = copy.deepcopy(raw_map_data)
        self.stones = [None] + copy.deepcopy(stones)
        num_stones = 0

        for i in range(len(raw_map_data)):
            for j in range(len(raw_map_data[i])):
                if raw_map_data[i][j] == ' ':
                    self.map_matrix[i][j] = self.SPACE
                elif raw_map_data[i][j] == '#':
                    self.map_matrix[i][j] = self.BLOCKER
                elif raw_map_data[i][j] == '@':
                    self.map_matrix[i][j] = self.USER
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
    def convert_display_map(self):
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