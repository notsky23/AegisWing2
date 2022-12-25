import unittest

import numpy as np

from Model.Agents.Actions import Actions
from Model.Agents.AgentInterface import AgentInterface
from Model.Agents.PlayerAgent import PlayerAgent
from Model.Agents.SimpleGoLeftAgent import SimpleGoLeftAgent
from Model.Agents.EnemyMoveFireHeuristicAgent import EnemyMoveFireHeuristicAgent
from Model.GameState import GameState
import sys
import codecs


class TestRLGameFunc(unittest.TestCase):

    def setUp(self) -> None:
        """
        Sets up variables to use. These variables are
        reset prior to every test
        :return: None
        """
        self.gamestateInit = GameState(7, 8)


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

    def get_state(self, game: GameState):
        """
        Return the state.
        The state is a numpy array of (8*7*7) x 1 , representing:
            - Player Location (in Grid)
            - Heuristic Enemy Locations
            - GoLeft Enemy Locations
            - BasicFireAndMove Locations
            - Counter Enemy Locations
            - Enemy Bullet Locations
            - Player Bullet Location

            Each position in list corresponds to a location and enemy type. The locations go in
            groups of 7 with a 1 representing that this agent is in that location. For example the
            first seven elements represent the top row fdr left state, the next seven one space to
            the rights, and so on with wrapping.
        """

        player_list_arr = game.gameBoard.get_board_with_agents_RL(game, 1, 1)
        left_list_arr = game.gameBoard.get_board_with_agents_RL(game, 2, 2)
        fire_move_list_arr = game.gameBoard.get_board_with_agents_RL(game, 3, 3)
        heur_list_arr = game.gameBoard.get_board_with_agents_RL(game, 4, 4)
        counter_list_arr = game.gameBoard.get_board_with_agents_RL(game, 5, 5)

        player_proj_list_arr = game.gameBoard.get_board_with_proj_RL(game, True)
        enemy_proj_list_arr = game.gameBoard.get_board_with_proj_RL(game, False)

        state = []
        for eachRowIndex in range(len(player_list_arr)):
            for eachColIndex in range(len(player_list_arr[eachRowIndex])):
                if player_list_arr[eachRowIndex][eachColIndex] == 1:
                    state.append(1)
                else:
                    state.append(0)

                if left_list_arr[eachRowIndex][eachColIndex] == 1:
                    state.append(1)
                else:
                    state.append(0)

                if fire_move_list_arr[eachRowIndex][eachColIndex] == 1:
                    state.append(1)
                else:
                    state.append(0)

                if heur_list_arr[eachRowIndex][eachColIndex] == 1:
                    state.append(1)
                else:
                    state.append(0)

                if counter_list_arr[eachRowIndex][eachColIndex] == 1:
                    state.append(1)
                else:
                    state.append(0)

                if player_proj_list_arr[eachRowIndex][eachColIndex] == 1:
                    state.append(1)
                else:
                    state.append(0)

                if enemy_proj_list_arr[eachRowIndex][eachColIndex] == 1:
                    state.append(1)
                else:
                    state.append(0)

        return state


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
        state.max_enemies_at_any_given_time = 5
        # set small turns
        state.turns_left = 10
        # make a player and add it
        player = PlayerAgent(1, 1, 2, 2)
        player.set_hp(3)
        state.addAgent(player)

        enemy_1 = SimpleGoLeftAgent(7,6)
        enemy_2 = SimpleGoLeftAgent(2, 0)
        enemy_3 = SimpleGoLeftAgent(1, 1)
        enemy_4 = SimpleGoLeftAgent(3, 5)
        # row 1, col = 7
        enemy_5 = EnemyMoveFireHeuristicAgent(4, 9)

        enemy_6 = SimpleGoLeftAgent(3, 3)
        enemy_7 = SimpleGoLeftAgent(4, 1)
        enemy_8 = SimpleGoLeftAgent(0, 3)

        # add agents
        state.addAgent(enemy_1)
        #state.addAgent(enemy_2)
        #state.addAgent(enemy_3)
        #state.addAgent(enemy_4)
        #state.addAgent(enemy_5)
        #state.addAgent(enemy_6)
        #state.addAgent(enemy_7)
        #state.addAgent(enemy_8)


        state.update_board()
        cnt = 0

        print("Turn: " + str(state.turns_left))
        print(state.gameBoard)
        print(f"lives left: {state.current_player_lives}")
        print(f"Lost Life?\t{state.lostLife}\n")
        print(f"Last hit: {state.lastHit}")
        print(f"Win?\t{state.isWin()}\nLose?\t{state.isLose()}\n")
        print(f"Bullet Reward: {self.check_Bullet_Paths(state)}")
        print(f"Agent LR Reward: {self.check_enemy_neighbors_left_right(state)}")
        print(f"Agent UD Reward: {self.check_enemy_neighbors_up_down(state)}")

        mystate = state
        state_arr = self.get_state(mystate)
        print(len(state_arr))
        print(str(state_arr))
        print(max(state_arr))


        # while game is still going
        while True:
            cnt += 1
            # get enemy agent action,
            for each_index in range(len(state.current_agents)):
                try:
                    print("Current Agent moving try block")
                    print(str(each_index))
                    each_agent: AgentInterface = state.current_agents[each_index]
                except IndexError:
                    print("Current Agent moving catch block")
                    print(str(each_index))
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
                    agent_action = Actions.FIRE
                    if(state.lostLife):
                        agent_action = Actions.UP
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
                        print(f"Agent UD Reward: {self.check_enemy_neighbors_up_down(state)}")
                        state_arr = self.get_state(state)
                        print(len(state_arr))
                        print(str(state_arr))
                        print(max(state_arr))

            state.reset_agents_move_status()

            if state.isWin() or state.isLose():
                break

        self.assertEqual(1, state.gameBoard.board_array[1][0])
        self.assertEqual('X', state.gameBoard.board_array[1][1])

"""
enemy_1 = SimpleGoLeftAgent(3, 1)
        enemy_2 = SimpleGoLeftAgent(2, 0)
        enemy_3 = SimpleGoLeftAgent(1, 1)
        enemy_4 = SimpleGoLeftAgent(3, 5)
        # row 1, col = 7
        #enemy_5 = EnemyMoveFireHeuristicAgent(4, 9)

        enemy_6 = SimpleGoLeftAgent(3, 3)
        enemy_7 = SimpleGoLeftAgent(4, 1)
        enemy_8 = SimpleGoLeftAgent(0, 3)

        # add agents
        state.addAgent(enemy_1)
        state.addAgent(enemy_2)
        state.addAgent(enemy_3)
        state.addAgent(enemy_4)
        #state.addAgent(enemy_5)
        state.addAgent(enemy_6)
        state.addAgent(enemy_7)
        state.addAgent(enemy_8)
if print_board:
    print("Turn: " + str(state.turns_left))
    print(state.gameBoard)
    print(f"lives left: {state.current_player_lives}")
    print(f"Lost Life?\t{state.lostLife}\n")
    print(f"Last hit: {state.lastHit}")
    print(f"Win?\t{state.isWin()}\nLose?\t{state.isLose()}\n")
    print(f"Bullet Reward: {self.check_Bullet_Paths(state)}")
    print(f"Agent LR Reward: {self.check_enemy_neighbors_left_right(state)}")
    print(f"Agent UD Reward: {self.check_enemy_neighbors_up_down(state)}")
"""