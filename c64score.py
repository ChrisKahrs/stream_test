def calculate_score(board, last_row, last_col):
    # Define board dimensions
    WIDTH = 8
    HEIGHT = 16
    
    # Define the scoring values
    score_map = {1: 0, 2: 2, 3: 9, 4: 16, 5: 25, 6: 1000}
    
    # Define the directions to search: right, down, diagonally right-down, diagonally left-down
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    # Initialize score for the last player
    player = board[last_row][last_col]
    score = 0
    
    # Search in all possible directions
    for direction in directions:
        count = 1
        dr, dc = direction
        # Search in the positive direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < HEIGHT and 0 <= c < WIDTH and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        
        # Search in the negative direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < HEIGHT and 0 <= c < WIDTH and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        
        # Update the score if count is in score_map
        if count in score_map:
            score += score_map[count]
    
    return score

def print_board(board):
    for row in reversed(board):
        print(' '.join(map(str, row)))

# Example usage
board = [
    [1, 1, 2, 0, 0, 1, 2, 0],
    [1, 2, 2, 0, 0, 0, 2, 0],
    [1, 1, 1, 0, 0, 1, 2, 0],
    # ... (add more rows as needed)
] + [[0] * 8 for _ in range(13)]  # Adding empty rows for demonstration

# Print board before last piece placed
print("Board before last piece placed:")
print_board(board)

# Assume the last piece was placed at row 2, column 2
last_row, last_col = 3, 0
board[last_row][last_col] = 1  # Simulating the last piece placed by player 1

# Print board after last piece placed
print("\nBoard after last piece placed:")
print_board(board)

# Calculate score for the last piece placed
score = calculate_score(board, last_row, last_col)
print(f"\nScore for the last piece placed: {score}")

# Player scores table
total_scores = {1: 0, 2: 0}
current_scores = {1: 0, 2: 0}

# Update the scores
current_scores[board[last_row][last_col]] = score
total_scores[board[last_row][last_col]] += score

# Print the players' score table
print("\nPlayer Scores:")
print("Player | Symbol | Total Score | Current Score")
print("-------------------------------------------")
for player in [1, 2]:
    print(f"  {player}    |    {player}    |      {total_scores[player]}       |      {current_scores[player]}")