import random

def generate_weights(num_stones):
    # Generate random weights between 1 and 10
    weights = [random.randint(1, 10) for _ in range(num_stones)]
    return weights

def generate_board(n, m, num_stones, num_blockers):
    # Initialize board with spaces
    board = [[' ' for _ in range(m)] for _ in range(n)]
    
    # Add blockers '#' around the border
    for i in range(n):
        board[i][0] = '#'
        board[i][m - 1] = '#'
    for j in range(m):
        board[0][j] = '#'
        board[n - 1][j] = '#'
    
    # Randomly place internal blockers
    blockers_placed = 0
    while blockers_placed < num_blockers:
        x = random.randint(1, n - 2)
        y = random.randint(1, m - 2)
        if board[x][y] == ' ':
            board[x][y] = '#'
            blockers_placed += 1
    
    # Place the user '@'
    while True:
        user_x = random.randint(1, n - 2)
        user_y = random.randint(1, m - 2)
        if board[user_x][user_y] == ' ':
            board[user_x][user_y] = '@'
            break

    # Place stones '$' (not next to any border line)
    stones_placed = 0
    while stones_placed < num_stones:
        x = random.randint(2, n - 3)
        y = random.randint(2, m - 3)
        if board[x][y] == ' ':
            board[x][y] = '$'
            stones_placed += 1

    # Place goals '.' (also not next to any border line)
    goals_placed = 0
    while goals_placed < num_stones:
        x = random.randint(2, n - 3)
        y = random.randint(2, m - 3)
        if board[x][y] == ' ':
            board[x][y] = '.'
            goals_placed += 1

    return board

def print_board(weights, board):
    # First line: weights of stones
    print(' '.join(map(str, weights)))

    # Board
    for row in board:
        print(''.join(row))

def main():
    # Board dimensions
    n = 10  # Number of rows
    m = 10  # Number of columns
    num_stones = 5  # Number of stones and goals
    num_blockers = 10  # Number of internal blockers

    # Generate weights and board
    weights = generate_weights(num_stones)
    board = generate_board(n, m, num_stones, num_blockers)

    # Output the test case
    print_board(weights, board)

if __name__ == "__main__":
    main()