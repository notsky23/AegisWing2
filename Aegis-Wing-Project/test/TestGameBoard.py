import unittest

from Model.Agents.PlayerAgent import PlayerAgent
from Model.Agents.SimpleGoLeftAgent import SimpleGoLeftAgent
from Model.GameBoard import GameBoard


gameBoard = GameBoard(10,10)

class TestGameBoard(unittest.TestCase):

    def setUp(self) -> None:
        self.board = GameBoard(10,8) #10 columns, 8 rows
        self.board_2 = GameBoard(8,4,12,10) #8 columns, 10 rows, min row = 12, max_col = 10

    # test default constructor values
    def test_default_constructor(self):
        self.assertEqual(10, self.board.board_length)
        self.assertEqual(8,self.board.board_height)
        self.assertEqual(0, self.board.min_col)
        self.assertEqual(0, self.board.min_row)
        self.assertEqual(9, self.board.board_max_x_boundary) # column boundary
        self.assertEqual(7, self.board.board_max_y_boundary) # row boundary

    # test valid values, non-default
    def test_valid_constructor_values(self):
        self.assertEqual(8, self.board_2.board_length)
        self.assertEqual(4, self.board_2.board_height)
        self.assertEqual(12, self.board_2.min_col)
        self.assertEqual(10, self.board_2.min_row)
        self.assertEqual(19, self.board_2.board_max_x_boundary)  # column boundary
        self.assertEqual(13, self.board_2.board_max_y_boundary)  # row boundary

    def test_initial_board_vals_equal_zero(self):
        all_zeroes_default = True
        hit = False
        board = self.board.board_array

        for eachRow in board:
            if hit == True:
                break
            for eachCol in eachRow:
                if eachCol > 0 or eachCol < 0:
                    all_zeroes_default = False
                    hit = True
                    break

        all_zeroes_non_default = True
        hit_2 = False
        board_2 = self.board_2.board_array

        for eachRow in board_2:
            if hit_2 == True:
                break
            for eachCol in eachRow:
                if eachCol > 0 or eachCol < 0:
                    all_zeroes_non_default = False
                    hit_2 = True
                    break

        self.assertEqual(True, all_zeroes_default)
        self.assertEqual(True,all_zeroes_non_default)

    def testRaiseValueErrorConstructor(self):
        '''
        Testing if invalid inputs passed into constructor
        :return: void
        '''
        error_counter = 0

        try:
            GameBoard(0,1) # edge case: board length = 0
        except ValueError:
            error_counter += 1

        try:
            GameBoard(1,0) # edge case: board height = 0
        except ValueError:
            error_counter += 1

        try:
            GameBoard(-1,2) # board length < 0
        except ValueError:
            error_counter += 1

        try:
            GameBoard(2,-1) # board height < 0
        except ValueError:
            error_counter += 1

        self.assertEqual(4, error_counter)

    def test_populate_board(self):
        # set to true to print board to terminal/console for visual aid
        print_board = True

        # default position is bottom left corner
        player = PlayerAgent()

        #self.board has #8 rows, 10 columns,
        #min row = 0, max_row = 9, min col = 0, max_col = 9
        #Place enemy on top left corner
        enemy_1 = SimpleGoLeftAgent(7, 9)

        #another enemy agent maybe like somewhere in the middle of the board
        enemy_2 = SimpleGoLeftAgent(3, 4)

        #key is AgentInterface obj, value is what its agentIndex+1 value would be
        dict_agents = {player: 1}
        dict_agents[enemy_1] = 2
        dict_agents[enemy_2] = 3

        # add them to the board_array
        self.board.populate_board_with_agents(dict_agents[player], player)
        self.board.populate_board_with_agents(dict_agents[enemy_1], enemy_1)
        self.board.populate_board_with_agents(dict_agents[enemy_2], enemy_2)

        if print_board:
            print("Board from test_populate_board ")
            print(self.board)

        #check positions
        self.assertEqual(1, self.board.board_array[0][0])
        self.assertEqual(2, self.board.board_array[7][9])
        self.assertEqual(3, self.board.board_array[3][4])


        #Merged Dan_DQN_branch
        #TODO write test with enemies with largers lengths, heights
        #TODO write test where enemy is beyond col boundaries, should be allowed
        #TODO: ask team where are the other tests





def main():
    unittest.main(verbosity=3)

if __name__ == '__main__':
    main()