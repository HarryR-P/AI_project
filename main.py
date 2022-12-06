import numpy as np
import TTT3d as tic
import matplotlib.pyplot as plt

def main():
    # a = np.zeros((4,4,4)).astype('int')
    

    TTT = tic.TTT3d()

    turns, winner, final_board, val_list = tic.rand_bot_game(tic.objective_fc_one, seed=1122333)

    print(final_board)

    plt.plot(val_list)
    plt.xlabel('Objective Function Value')
    plt.show()

    return


if __name__=='__main__':
    main()