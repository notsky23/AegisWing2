import unittest

from Model.Agents.Actions import Actions
from Model.Agents.AgentInterface import AgentInterface
from Model.Agents.PlayerAgent import PlayerAgent
from Model.Agents.SimpleGoLeftAgent import SimpleGoLeftAgent
from Model.Agents.EnemyMoveFireHeuristicAgent import EnemyMoveFireHeuristicAgent
from Model.GameState import GameState

from Model.GameBoard import GameBoard
import numpy as np
import sys
import codecs


class TestGameStateGameExamples(unittest.TestCase):
    def get_state(self, game: GameState):
        """
        Possible other inputs:
        - Have to keep tensors the same so I cant include these if im including the grid
            - Danger some Agent 1-3 columns to the right and -1,0,1 rows away
            - Danger some Agent 1-2 columns to the left and -1,0,1 rows away
            - Danger same Agent same column and 1-2 rows up or 1 col right/left 2 up.
            - Danger same Agent same column and 1-2 rows down or 1 col right/left 2 down.
            - Danger enemy bullet at same row and 1-3 columns to right
            - Danger enemy bullet at one row up and 1-2 columns to right
            - Danger enemy bullet at one row down and 1-2 columns to right
            - Possibility --> Change all positions to values [1 , (col*row + 1)]/(col*row + 1)

        """
        """
        Return the state.
        The state is a numpy array of 8 2D Array values, representing:
            - Player Location (in Grid)
            - Heuristic Enemy Locations board col x board row tensor
            - GoLeft Enemy Locations boc col x row tensor
            - BasicFireAndMove Locations
            - Counter Enemy Locations
            - Enemy Bullet Locations
            - Player Bullet Location
            - EnemyOverlapLocations
        """

        player_list_arr = np.array(game.gameBoard.get_board_with_agents_RL(game, 1, 1), dtype="int32")
        left_list_arr = np.array(game.gameBoard.get_board_with_agents_RL(game, 2, 2), dtype="int32")
        fire_move_list_arr = np.array(game.gameBoard.get_board_with_agents_RL(game, 3, 3), dtype="int32")
        heur_list_arr = np.array(game.gameBoard.get_board_with_agents_RL(game, 4, 4), dtype="int32")
        counter_list_arr = np.array(game.gameBoard.get_board_with_agents_RL(game, 5, 5), dtype="int32")

        player_proj_list_arr = np.array(game.gameBoard.get_board_with_proj_RL(game, True), dtype="int32")
        enemy_proj_list_arr = np.array(game.gameBoard.get_board_with_proj_RL(game, False), dtype="int32")

        overlap_list_arr = np.array(game.gameBoard.get_board_with_agents_overlaps_RL(game, 2, 6),
                                    dtype="int32")

        state = np.array([player_list_arr, left_list_arr, fire_move_list_arr, heur_list_arr, counter_list_arr,
                          player_proj_list_arr, enemy_proj_list_arr, overlap_list_arr])

        return state
    def setUp(self) -> None:
        """
        Sets up variables to use. These variables are
        reset prior to every test
        :return: None
        """
        self.gamestateInit = GameState()

    def check_Bullet_Paths(self, game: GameState):
        """
        Creates a negative reward for each enemy bullet in a radius.
        Gives -5 points for each up to a maximum of -45
        Checks 2 columns to the right of player and -1,0,1 row up/down.
        Also checks 3 spaces to the right in the player row.
        Args:
            game: The current gamestate

        Returns: the negative reward

        """
        neg_reward = 0
        # gets the lowest row then the least col
        player_y, player_x = game.getPlayerPos()
        check_y = [player_y - 1, player_y, player_y + 1]
        check_x = [player_x + 1, player_x + 2]
        check_x2 = player_x + 3

        enemy_proj = list(filter(lambda x: x.isPlayerBullet() is False, game.current_projectiles))
        if len(enemy_proj) > 0:
            for proj in enemy_proj:
                proj_y, proj_x = proj.get_position()
                if proj_y in check_y:
                    if proj_x in check_x:
                        neg_reward -= 5
                    if proj_y == player_y and proj_x == check_x2:
                        neg_reward -= 5

        return neg_reward

    def check_enemy_neighbors_left_right(self, game: GameState):
        """
        Creates a negative reward for each enemy agent left or right of player.
        Gives -10 points for each up to a maximum of -50 (max of 5 agents)
        Checks up to columns to the right of player and -1,0,1 row up/down.
        Also check 2 columns left of player and same rows.
        Args:
            game: The current gamestate

        Returns: the negative reward

        """
        neg_reward = 0
        # gets the lowest row then the least col
        player_y, player_x = game.getPlayerPos()
        check_y = [player_y - 1, player_y, player_y + 1]
        # checks the 3 columns to the right of the player and 2 to the left
        check_x = [player_x - 1, player_x - 2, player_x + 1, player_x + 2, player_x + 3]
        check_x2 = player_x + 3

        enemy_agents = list(filter(lambda x: x.isPlayer() is False, game.current_agents))
        if len(enemy_agents) > 0:
            for enemy in enemy_agents:
                proj_y, proj_x = enemy.get_position()
                if proj_y in check_y:
                    if proj_x in check_x:
                        neg_reward -= 10
                    if proj_y == player_y and proj_x == check_x2:
                        neg_reward -= 10

        return neg_reward

    def check_enemy_neighbors_up_down(self, game: GameState):
        """
        Creates a negative reward for each enemy agent above/below/on player
        Gives -10 points for each up to a maximum of -50 (max of 5 agents)
        Checks the player column 2 rows down up to 2 rows above.
        On the max rows also checks the columns 1 left and 1 right of player
        Args:
            game: The current gamestate

        Returns: the negative reward

        """
        neg_reward = 0
        # gets the lowest row then the least col
        player_y, player_x = game.getPlayerPos()
        check_y = [player_y - 2, player_y - 1, player_y, player_y + 1, player_y + 2]
        check_y2 = [player_y - 2, player_y + 2]
        # checks the 3 columns to the right of the player and 2 to the left
        check_x = [player_x - 1, player_x + 1]

        enemy_agents = list(filter(lambda x: x.isPlayer() is False, game.current_agents))
        if len(enemy_agents) > 0:
            for enemy in enemy_agents:
                proj_y, proj_x = enemy.get_position()
                if proj_y in check_y:
                    if proj_x == player_x:
                        neg_reward -= 10
                    elif proj_y in check_y2 and proj_x in check_x:
                        neg_reward -= 10

        return neg_reward

    def test_game_example_1(self):
        """
        For this test
            - 1 player, 1 SimpleGoLeft enemy and 1 heuristic enemy
            - simple enemy does not hit player
            - one enemy exits the game before the other
            - Heuristic agent moves towards the player and kills it
        :return:
        """
        # set to true to print board to terminal/console for visual aid
        print_board = True

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 7
        # set small turns
        state.turns_left = 10
        # make a player and add it
        player = PlayerAgent(1, 1, 2, 2)
        player.set_hp(3)
        state.addAgent(player)

        enemy_1 = SimpleGoLeftAgent(3, 1)
        enemy_2 = SimpleGoLeftAgent(2, 0)
        enemy_3 = SimpleGoLeftAgent(1, 1)
        enemy_4 = SimpleGoLeftAgent(3, 5)
        # row 1, col = 7
        enemy_5 = EnemyMoveFireHeuristicAgent(4, 9)

        enemy_6 = SimpleGoLeftAgent(3, 3)
        enemy_7 = SimpleGoLeftAgent(3, 5)
        enemy_8 = SimpleGoLeftAgent(3, 5)

        # add agents
        state.addAgent(enemy_1)
        state.addAgent(enemy_2)
        state.addAgent(enemy_3)
        state.addAgent(enemy_4)
        state.addAgent(enemy_5)

        state.update_board()
        myarr = self.get_state(state)
        print("ARRAY DIM")
        print(myarr.shape)

        print("OLD DIM")
        print(np.asarray([1,0,0,0,0,0,0,0,0,0,0]).shape)
        print(np.asarray([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]).reshape(1,11).shape)

        cnt = 0

        print("Turn: " + str(state.turns_left))
        print(state.gameBoard)
        print(f"lives left: {state.current_player_lives}")
        print(f"Lost Life?\t{state.lostLife}\n")
        print(f"Last hit: {state.lastHit}")
        print(f"Win?\t{state.isWin()}\nLose?\t{state.isLose()}\n")
        print(f"Bullet Reward: {self.check_Bullet_Paths(state)}")
        print(f"Agent LR Reward: {self.check_enemy_neighbors_left_right(state)}")

        # while game is still going
        while True:
            cnt += 1
            # get enemy agent action,
            for each_index in range(len(state.current_agents)):
                try:
                    each_agent: AgentInterface = state.current_agents[each_index]
                except IndexError:
                    # means list was shortened because agent died or exited board
                    # case 1 agent in middle of list disappeared
                    each_agent: AgentInterface = state.current_agents[each_index - 1]
                    # case 2 agent at end of list died/disappeared
                    # no more agents to move
                    if each_agent.hasMoved():
                        break
                    else:
                        each_index -= 1
                    # continue otherwise

                # making player action just stop for this example
                if each_agent.isPlayer():
                    if cnt % 2 == 0:
                        agent_action = Actions.FIRE
                    elif(state.lostLife):
                        agent_action = Actions.UP
                    else:
                        agent_action = Actions.STOP
                elif each_agent.isHeuristicAgent():
                    agent_action = each_agent.autoPickAction(state)
                else:
                    agent_action = each_agent.autoPickAction()

                # len of current agents may change here, potentiall causing index error
                state = state.generateSuccessorState(each_index, agent_action)

                if (state.current_agents[len(state.current_agents) - 1].hasMoved() == True):
                    state.decrement_turn()

                    if print_board:
                        print("Turn: " + str(state.turns_left))
                        print(state.gameBoard)
                        print(f"lives left: {state.current_player_lives}")
                        print(f"Lost Life?\t{state.lostLife}\n")
                        print(f"Last hit: {state.lastHit}")
                        print(f"Win?\t{state.isWin()}\nLose?\t{state.isLose()}\n")
                        print(f"Bullet Reward: {self.check_Bullet_Paths(state)}")
                        print(f"Agent LR Reward: {self.check_enemy_neighbors_left_right(state)}")

            state.reset_agents_move_status()

            if state.isWin() or state.isLose():
                break

        self.assertEqual(1, state.gameBoard.board_array[1][0])
        self.assertEqual('X', state.gameBoard.board_array[1][1])

    def test_game_example_2(self):
        """
        For this test
            - 1 heuristic enemy
            - heuristic agent starts behind player
            - Heuristic agent should move right then go up/down around the player
            - Once it gets 2 spaces past the player it should move to the correct row
            - Then it shoots and kills player as it moves down
        :return:
        """
        # set to true to print board to terminal/console for visual aid
        print_board = True

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 2
        # set small turns
        state.turns_left = 10
        # make a player and add it
        player = PlayerAgent(1, 1, 5, 5)
        state.addAgent(player)

        enemy_2 = EnemyMoveFireHeuristicAgent(5, 0)

        state.addAgent(enemy_2)

        state.update_board()

        # while game is still going
        while True:
            # get enemy agent action,
            for each_index in range(len(state.current_agents)):
                try:
                    each_agent: AgentInterface = state.current_agents[each_index]
                except IndexError:
                    # means list was shortened because enemy agent died or exited board
                    # 3 cases
                    # case 1 agent in middle of list disappeared
                    each_agent: AgentInterface = state.current_agents[each_index - 1]
                    # case agent at end of list died/disappeared
                    # no more agents to move
                    if each_agent.hasMoved():
                        state.decrement_turn()
                        break
                    else:
                        each_index -= 1
                    # continue otherwise

                # making player action just stop for this example
                if each_agent.isPlayer():
                    agent_action = Actions.STOP
                elif each_agent.isHeuristicAgent():
                    agent_action = each_agent.autoPickAction(state)
                else:
                    agent_action = each_agent.autoPickAction()

                # len of current agents may change here, potentially causing index error
                state = state.generateSuccessorState(each_index, agent_action)

                if (state.current_agents[len(state.current_agents) - 1].hasMoved() == True):
                    state.decrement_turn()

                    if print_board:
                        print("Turn: " + str(state.turns_left))
                        print(state.gameBoard)
                        print(f"lives left: {state.current_player_lives}")
                        print(f"Win?\t{state.isWin()}\nLose?\t{state.isLose()}\n")
            state.reset_agents_move_status()

            if state.isWin() or state.isLose():
                break

        self.assertEqual(2, state.gameBoard.board_array[5][7])
        # Check that player was killed
        self.assertEqual(0, state.gameBoard.board_array[5][6])

    # TODO: What happens if 2 bullets are fired from the same spot?

    def test_game_example_3(self):

        """
        For this test
            - 2 Heuristic Enemies
            - 1 at top, 1 at bottom
            - player in back middle
            - Check that both move towards player
            - Check that they kill player
            - If you run this test multiple times you can
                    see that agents have a chance of not following
                    the preset pattern if there is another agent overlapping
        :return:
        """
        # set to true to print board to terminal/console for visual aid
        print_board = True

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 2
        # set small turns
        state.turns_left = 10
        # make a player and add it
        player = PlayerAgent(1, 1, 4, 4)
        state.addAgent(player)

        enemy_1 = EnemyMoveFireHeuristicAgent(9, 9)

        enemy_2 = EnemyMoveFireHeuristicAgent(0, 9)

        # add agents
        state.addAgent(enemy_1)
        state.addAgent(enemy_2)

        state.update_board()

        # while game is still going
        while True:
            # get enemy agent action,
            for each_index in range(len(state.current_agents)):
                try:
                    each_agent: AgentInterface = state.current_agents[each_index]
                except IndexError:
                    # means list was shortened because enemy agent died or exited board
                    # 3 cases
                    # case 1 agent in middle of list disappeared
                    each_agent: AgentInterface = state.current_agents[each_index - 1]
                    # case agent at end of list died/disappeared
                    # no more agents to move
                    if each_agent.hasMoved():
                        state.decrement_turn()
                        break
                    else:
                        each_index -= 1
                    # continue otherwise

                # making player action just stop for this example
                if each_agent.isPlayer():
                    agent_action = Actions.STOP
                elif each_agent.isHeuristicAgent():
                    agent_action = each_agent.autoPickAction(state)
                else:
                    agent_action = each_agent.autoPickAction()

                # len of current agents may change here, potentially causing index error
                state = state.generateSuccessorState(each_index, agent_action)

                if (state.current_agents[len(state.current_agents) - 1].hasMoved() == True):
                    state.decrement_turn()

                    if print_board:
                        print("Turn: " + str(state.turns_left))
                        print(state.gameBoard)
                        print(f"lives left: {state.current_player_lives}")
                        print(f"Win?\t{state.isWin()}\nLose?\t{state.isLose()}\n")
            state.reset_agents_move_status()

            if state.isWin() or state.isLose():
                break

            # checking that the player is dead
        self.assertEqual(0, state.gameBoard.board_array[4][4])
        self.assertEqual(2, len(state.current_agents))


    def test_game_example_4(self):

        """
        For this test
            - 2 Heuristic Enemies
            - 1 at top, 1 at bottom
            - player in back middle
            - Check that both move towards player
            - Player moves up as much as possible --> Check that agents will follow
            - Check that they kill player
        :return:
        """
        # set to true to print board to terminal/console for visual aid
        print_board = True

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 2
        # set small turns
        state.turns_left = 10
        # make a player and add it
        player = PlayerAgent(1, 1, 4, 4)
        state.addAgent(player)

        enemy_1 = EnemyMoveFireHeuristicAgent(9, 9)

        enemy_2 = EnemyMoveFireHeuristicAgent(0, 9)

        # add agents
        state.addAgent(enemy_1)
        state.addAgent(enemy_2)

        state.update_board()

        # while game is still going
        while True:
            # get enemy agent action,
            for each_index in range(len(state.current_agents)):
                try:
                    each_agent: AgentInterface = state.current_agents[each_index]
                except IndexError:
                    # means list was shortened because enemy agent died or exited board
                    # 3 cases
                    # case 1 agent in middle of list disappeared
                    each_agent: AgentInterface = state.current_agents[each_index - 1]
                    # case agent at end of list died/disappeared
                    # no more agents to move
                    if each_agent.hasMoved():
                        state.decrement_turn()
                        break
                    else:
                        each_index -= 1
                    # continue otherwise

                # making player action just stop for this example
                if each_agent.isPlayer():
                    agent_copy = each_agent.deepcopy()
                    agent_copy.performAction(Actions.UP)
                    print("Can the player move up?")
                    print(state.isValidAgent(agent_copy))
                    if state.isValidAgent(agent_copy):
                        agent_action = Actions.UP
                    else:
                        agent_action = Actions.STOP

                elif each_agent.isHeuristicAgent():
                    agent_action = each_agent.autoPickAction(state)
                else:
                    agent_action = each_agent.autoPickAction()

                # len of current agents may change here, potentially causing index error
                state = state.generateSuccessorState(each_index, agent_action)

                if (state.current_agents[len(state.current_agents) - 1].hasMoved() == True):
                    state.decrement_turn()

                    if print_board:
                        print("Turn: " + str(state.turns_left))
                        print(state.gameBoard)
                        print(f"lives left: {state.current_player_lives}")
                        print(f"Win?\t{state.isWin()}\nLose?\t{state.isLose()}\n")
            state.reset_agents_move_status()

            if state.isWin() or state.isLose():
                break

            # checking that the player is dead
        self.assertEqual(2, state.gameBoard.board_array[9][7])
        self.assertEqual(2, state.gameBoard.board_array[6][9])

        self.assertEqual(2, len(state.current_agents))


# ramzi merged
def main():
    unittest.main(verbosity=3)


if __name__ == '__main__':
    main()
