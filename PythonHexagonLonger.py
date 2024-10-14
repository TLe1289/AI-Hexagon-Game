
adj_matrix = [[0 for _ in range(7)] for _ in range(7)]  # Initialize adjacency matrix
history = set()
players = {1: "solid", 2: "dashed"}
winning_move = None


def add_edge(player, edge):
    v1, v2 = edge
    adj_matrix[v1][v2] = player
    adj_matrix[v2][v1] = player
    history.add(edge)

def is_triangle(player):
    for i in range(1, 7):
        for j in range(i + 1, 7):
            for k in range(j + 1, 7):
                if adj_matrix[i][j] == player and adj_matrix[j][k] == player and adj_matrix[k][i] == player:
                    return True
    return False

def remove_edge(edge):
    v1, v2 = edge
    adj_matrix[v1][v2] = 0
    adj_matrix[v2][v1] = 0
    history.remove(edge)

def get_valid_moves():
    vertices = set(range(1, 7))
    valid_moves = set()
    for v1 in vertices:
        for v2 in vertices:
            if v1 < v2 and adj_matrix[v1][v2] == 0:
                valid_moves.add((v1, v2))
    return valid_moves

def minimax(depth, player, alpha, beta):
    if player == 1:
        best_score = float('-inf')
        best_move = None
        for edge in get_valid_moves():
            add_edge(player, edge)
            if is_triangle( player):
                score = -1
            else:
                score, _ = minimax(depth - 1, 2, alpha, beta)
            remove_edge(edge)
            if score > best_score:
                best_score = score
                best_move = edge
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = None
        for edge in get_valid_moves():
            add_edge(player, edge)
            if is_triangle(player):
                score = 1
            else:
                score, _ = minimax(depth - 1, 1, alpha, beta)
            remove_edge(edge)
            if score < best_score:
                best_score = score
                best_move = edge
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score, best_move
        
def check(edge):
    v1, v2 = edge
    if adj_matrix[v1][v2] != 0:
        return True
    if adj_matrix[v2][v1] != 0:
        return True
    return False    # it equals 0 and won't ask player 2 again

def print_board():
    print("Current Board:")
    for edge in history:
        v1, v2 = edge
        print("{} for Player {}".format(edge, adj_matrix[v1][v2]))
        


def play_game():
    print("Player 1 uses solid lines, Player 2 uses dashed lines.")
    player = int(input("Enter player number (1 or 2): "))
    while player not in [1, 2]:
        print("Invalid player number.")
        player = int(input("Enter player number (1 or 2): "))
    while True:
        print_board()
        if player == 1:
            print("Player 1's turn:")
            _, edge = minimax(9, 1, float('-inf'), float('inf'))
            add_edge(player, edge)
            if is_triangle(player):
                print("Player 1 loses! Player 2 wins!")
                print_board(history)
                break
            player = 2
        else:
            print("Player 2's turn:")
            edge = input("Player 2, enter edge (e.g., '1-2'): ").strip()
            edge = tuple(map(int, edge.split('-')))
            if check(edge):
                print("Edge already exists.")
                continue
            add_edge(player, edge)
            if is_triangle(player):
                print("Player 2 loses! Player 1 wins!")
                print_board()
                break
            player = 1

if __name__ == "__main__":
    play_game()
