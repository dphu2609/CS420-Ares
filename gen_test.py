import random
import os

def generate_weights(num_stones):
    # Generate random weights between 1 and 10
    weights = [random.randint(1, 99) for _ in range(num_stones)]
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
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)

    invalid_cases = [8]
    
    for i in invalid_cases:
        n = random.randint(6, 8)
        m = random.randint(8, 10)
        num_stones = random.randint(2, 3)
        num_blockers = random.randint(0, 10)
        
        weights = generate_weights(num_stones)
        board = generate_board(n, m, num_stones, num_blockers)
        
        with open(f'data/input{i}.txt', 'w') as f:
            f.write(' '.join(map(str, weights)) + '\n')
            for row in board:
                f.write(''.join(row) + '\n')

if __name__ == "__main__":
    main()