import matplotlib.pyplot as plt
import numpy as np



def get_rule(idx):
    input_patterns = [
                (1,1,1),
                (1,1,0),
                (1,0,1),
                (1,0,0),
                (0,1,1),
                (0,1,0),
                (0,0,1),
                (0,0,0)
            ]

    output = list(map(int, format(idx, "#010b")[2:]))
    mapping = dict(zip(input_patterns, output))
    mapping["name"] = "rule %d" % (idx)
    return(mapping)

def iterate(board, rule):
    board = np.pad(board, (1, 1), 'constant', constant_values=(0,0))
    new_board = np.zeros_like(board)
    for i in range(1, board.shape[0] - 1):
        new_board[i] = rule[tuple(board[i-1:i+2])]
    return new_board[1:-1]


def generate_map(initial_board, rule, num_iterations=1000):

    if isinstance(initial_board, list):
        board = np.array(initial_board)
    else:
        board = initial_board

    board = np.pad(board, (num_iterations, num_iterations), 'constant', constant_values=(0,0))

    rows = [board]
    for i in range(num_iterations):
        board = iterate(board, rule)
        rows.append(board)

    rows = np.array(rows)
    return rows


def visualize_board(board, title=None):
    plt.figure(figsize=(16,16))
    plt.imshow(board, cmap="bone")
    plt.axis("off")
    if title is not None:
        plt.title(title, fontsize=14)
    plt.show()
    plt.close()



rule = get_rule(30)
board = generate_map([0,1,0], rule, num_iterations=1000)
visualize_board(board, rule["name"])