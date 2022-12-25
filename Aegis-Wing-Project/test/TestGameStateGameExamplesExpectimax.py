import unittest

from Model.Agents.Actions import Actions
from Model.Agents.AgentInterface import AgentInterface
from Model.Agents.EnemyAgentBasicFireAndMove import EnemyAgentBasicFireAndMove
from Model.Agents.EnemyMoveFireHeuristicAgent import EnemyMoveFireHeuristicAgent
from Model.Agents.ExpectimaxAgent import ExpectimaxAgent
from Model.Agents.PlayerAgent import PlayerAgent
from Model.Agents.SimpleGoLeftAgent import SimpleGoLeftAgent
from Model.GameState import GameState

#TODO Nosky fix tests
class TestGameStateGameExamples(unittest.TestCase):
    def setUp(self) -> None:
        """
        Notsky Branch 4
        Sets up variables to use. These variables are
        reset prior to every test
        :return: None
        """
        self.gamestateInit = GameState()

    def test_game_example_1(self):
        """
        Notsky Branch 4
        For this test
            - 1 simple and 1 expectimax enemy
            - simple enemy does not hit player
            - one enemy exits the game before the other
            - Heuristic agent moves towards the player and kills it
        :return:
        """
        # set to true to print board to terminal/console for visual aid
        print_board = True

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 2
        # set small turns
        state.turns_left = 10
        # make a player and add it
        player = PlayerAgent(1, 1, 0, 0)
        state.addAgent(player)

        enemy_1 = SimpleGoLeftAgent(3, 3)
        # row 1, col = 7
        enemy_2 = ExpectimaxAgent(9, 9)

        # add agents
        state.addAgent(enemy_1)
        state.addAgent(enemy_2)

        state.update_board()

        if print_board:
            print("Turn: " + str(state.turns_left))
            print(state.gameBoard)
            print(f"lives left: {state.current_player_lives}")
            print(f"Win?\t{state.isWin()}\nLose?\t{state.isLose()}\n")

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
                elif each_agent.isExpectimaxAgent():
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
                        print(f"Win?\t{state.isWin()}\nLose?\t{state.isLose()}\n")

            # once for loop is done reset move status
            state.reset_agents_move_status()

            if state.isWin() or state.isLose():
                break

        # self.assertEquals(1, state.gameBoard.board_array[0][0])

        # checking that the player is dead
        # self.assertEqual(2, state.gameBoard.board_array[0][3])
        # self.assertEqual('B', state.gameBoard.board_array[0][1])