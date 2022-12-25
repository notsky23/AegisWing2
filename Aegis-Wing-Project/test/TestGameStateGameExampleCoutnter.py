import unittest

from Model.Agents.Actions import Actions
from Model.Agents.AgentInterface import AgentInterface
from Model.Agents.BasicCounterAgent import BasicCounterAgent
from Model.Agents.PlayerAgent import PlayerAgent
from Model.Agents.SimpleGoLeftAgent import SimpleGoLeftAgent
from Model.Agents.EnemyMoveFireHeuristicAgent import EnemyMoveFireHeuristicAgent
from Model.GameState import GameState
import sys
import codecs


# branch_4

class TestGameStateGameExamples(unittest.TestCase):
    def setUp(self) -> None:
        """
        Sets up variables to use. These variables are
        reset prior to every test
        :return: None
        """
        self.gamestateInit = GameState()

    def test_game_example_1(self):
        """
        For this test
            - 1 simple and 1 counter enemy with a count of 2
            - simple enemy does not hit player
            - Counter Agent moves 2 spaces left then waits 2 turns and leaves
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
        enemy_2 = BasicCounterAgent(4, 4, 4, 2, 4)

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

                # len of current agents may change here, potentiall causing index error
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

        self.assertEqual(1, len(state.current_agents))
        self.assertEqual(1, state.gameBoard.board_array[0][0])

    #TODO: counter heuristic with non counter test
    #TODO: move features to concreate classes
    def test_game_example_2(self):
        """
        For this test
            - 1 heuristic with 5 count and 1 counter enemy with a count of 2
            - Simple Counter agent moves up 2 spaces left 2 spaces then leaves after 2 turns
            - Heuristic agent kills player and leaves after 4 turns
        :return:
        """
        # set to true to print board to terminal/console for visual aid
        print_board = True

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 2
        # set small turns
        state.turns_left = 10
        # make a player and add it
        player = PlayerAgent(1, 1, 9, 0)
        state.addAgent(player)

        enemy_1 = EnemyMoveFireHeuristicAgent(1, 3, count=4)
        # row 1, col = 7
        enemy_2 = BasicCounterAgent(3, 4, 2, 2, 4)

        # add agents
        state.addAgent(enemy_1)
        state.addAgent(enemy_2)

        state.update_board()
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

        self.assertEqual(1, len(state.current_agents))
        self.assertEqual(1, state.gameBoard.board_array[9][0])

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
