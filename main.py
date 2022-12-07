import numpy as np
import TTT3d as tic
import matplotlib.pyplot as plt

def main():

    turns, winner, final_board, val_list = tic.rand_bot_game(tic.objective_fc_four, seed=1122333)

    print(final_board)

    plt.plot(val_list)
    plt.title('Objective Function Value per turn')
    plt.xlabel('Turns')
    plt.ylabel('Value')
    plt.show()

    return


if __name__=='__main__':
    main()