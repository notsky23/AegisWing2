import random
import unittest

from Model.Agents.Actions import Actions
from Model.Agents.AgentInterface import AgentInterface
from Model.Agents.EnemyAgentBasicFireAndMove import EnemyAgentBasicFireAndMove
from Model.Agents.EnemyMoveFireHeuristicAgent import EnemyMoveFireHeuristicAgent
from Model.Agents.PlayerAgent import PlayerAgent
from Model.Agents.SimpleGoLeftAgent import SimpleGoLeftAgent
from Model.EnemyPicker import EnemyPicker
from Model.GameState import GameState

"""
This class tests game loops with varying game conditions
to ensure successive gamestates are being generated correctly (generateSuccessorState method)
as the game progresses.
"""
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
        Game Conditions:
            - 2 SimpleGoLeft Agents, they move at the same rate
            - They do not hit the player agent
            - They both exit the board simultaneously
            - The game lasts for 10 turns
        Tests:
        - Enemy agents get removed from state (agents list) upon exiting board space
        - Update board renders positions correctly
        :return:
        """
        # set to true to print board to terminal/console for visual aid
        print_board = False

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 2
        # set small turns
        state.turns_left = 10
        # make a player and add it
        player = PlayerAgent(1, 1, 0, 0)
        state.addAgent(player)

        enemy_1 = SimpleGoLeftAgent(9, 9)
        enemy_2 = SimpleGoLeftAgent(1, 9)

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
#TODO check if agent is heuristic if so pass state intp autopickaction, have autopick action take null param by default
                # making player action just stop for this example
                if each_agent.isPlayer():
                    agent_action = Actions.STOP
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

        self.assertEquals(1, state.gameBoard.board_array[0][0])
        self.assertEquals(1, len(state.current_agents))

    def test_game_example_2(self):
        """
        Ramzi Branch 2
        Game Conditions
            - Player does not move
            - 2 enemies (SimpleGoLeft)
            - neither enemy hits player
            - one enemy exits the game before the other
        Tests:
            - Check that one enemy removed from state
            - Check board renders correctly
        :return:
        """
        # set to true to print board to terminal/console for visual aid
        print_board = False

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 2
        # set small turns
        state.turns_left = 9
        # make a player and add it
        player = PlayerAgent(1, 1, 0, 0)
        state.addAgent(player)


        enemy_1 = SimpleGoLeftAgent(9, 9)
        #row 1, col = 7
        enemy_2 = SimpleGoLeftAgent(1, 7)

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

        self.assertEquals(1, state.gameBoard.board_array[0][0])
        self.assertEquals(2, len(state.current_agents))

    def test_game_example_3(self):
        """
        Ramzi Branch 2
        Game Conditions:
            - 2 SimpleGoLeft enemy Agents
            - Player does not move
            - One SimpleGoLeft hits player, causes player to lose
        Tests:
            - board rendered correctly
            - isWin and isLose methods
            - player and colliding enemy removed from state
            - Game ended after 5 turns
        :return:
        """

        # set to true to print board to terminal/console for visual aid
        print_board = False

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 2
        # set small turns
        state.turns_left = 10
        # make a player and add it
        player = PlayerAgent(1, 1, 0, 0)
        state.addAgent(player)

        enemy_1 = SimpleGoLeftAgent(9, 9)
        # row 1, col = 7
        enemy_2 = SimpleGoLeftAgent(0, 5)

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
                else:
                    agent_action = each_agent.autoPickAction()

                # len of current agents may change here, potentiall causing index error
                state = state.generateSuccessorState(each_index, agent_action)

                if (state.current_agents[len(state.current_agents) - 1].hasMoved() == True):
                    state.decrement_turn()

                    if print_board:
                        state.update_board()
                        print("Turn: " + str(state.turns_left))
                        print(state.gameBoard)
                        print(f"lives left: {state.current_player_lives}")
                        print(f"Win?\t{state.isWin()}\nLose?\t{state.isLose()}\n")

            state.reset_agents_move_status()

            if state.isWin() or state.isLose():
                break

        self.assertTrue(state.isLose())
        self.assertFalse(state.isWin())
        self.assertEquals(5, state.turns_left)
        self.assertEquals(1, len(state.current_agents))

    def test_game_example_head_on_collision(self):
        """
        Game Conditions:
            - 1 SimpleGoLeft enemy Agents
            - Player moves only to the right
            - SimpleGoLeft hits player, causes player to lose
        Tests:
            - board rendered correctly
            - isWin and isLose methods
            - player and colliding enemy removed from state
            - Game ended after 2 turns
        :return:
        """

        # set to true to print board to terminal/console for visual aid
        print_board = True

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 2
        # set small turns
        state.turns_left = 10
        # make a player and add it
        player = PlayerAgent(1, 1, 5, 4)
        state.addAgent(player)

        enemy_1 = SimpleGoLeftAgent(5, 7)

        # add agents
        state.addAgent(enemy_1)

        state.update_board()
        if print_board:
            print("initial state")
            print(state.gameBoard)

        inner_loop_flag = False
        # while game is still going
        while True:
            if inner_loop_flag == True:
                break
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
                    agent_action = Actions.RIGHT
                else:
                    agent_action = each_agent.autoPickAction()

                # len of current agents may change here, potentiall causing index error
                state = state.generateSuccessorState(each_index, agent_action)

                if len(state.current_agents) > 0: #TODO Ramzi: Needs to implement this in final game loop
                    if (state.current_agents[len(state.current_agents) - 1].hasMoved() == True):
                        state.decrement_turn()

                        if print_board:
                            state.update_board()
                            print("Turn: " + str(state.turns_left))
                            print(state.gameBoard)
                            print(f"lives left: {state.current_player_lives}")
                            print(f"Win?\t{state.isWin()}\nLose?\t{state.isLose()}\n")
                else:
                    inner_loop_flag = True
                    state.turns_left -= 1

                    if print_board:
                        state.update_board()
                        print("Turn: " + str(state.turns_left))
                        print(state.gameBoard)
                        print(f"lives left: {state.current_player_lives}")
                        print(f"Win?\t{state.isWin()}\nLose?\t{state.isLose()}\n")

                    break

            state.reset_agents_move_status()

            if state.isWin() or state.isLose():
                break

        self.assertTrue(state.isLose())
        self.assertFalse(state.isWin())
        self.assertEquals(8, state.turns_left)


    def test_game_example_4(self):
        """
        Ramzi Branch 3
        Game Conditions:
            - 10 turns player spawn in middle of board on furthest left col
            - Spawn rate is 100%
            - max enemies is 5
            - Only enemy type is SimpleGoLeft
            - 1 enemy should spawn per turn up until turn 5, total 5 enemies
            - player does not move
        Test:
            - amount of enemies by the end is 5
            - one enemy added per turn until 5 is reached
            - board renders correctly
        :return:
        """

        # set to true to print board to terminal/console for visual aid
        print_board = False

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 5
        # set small turns
        state.turns_left = 10
        # make a player size 1 X 1 at row=5,col=0 and add it
        player = PlayerAgent(1, 1, 5, 0)
        state.addAgent(player)

        #pass in gameboard to get spawn boundaries, 2nd param is spawn rate
        enemy_spawner = EnemyPicker(state.gameBoard, 100)
        enemy_spawner.add_enemy_to_spawn_list(SimpleGoLeftAgent(1,1),15) #weight doesn't mattter if only one enemy type to spawn
        enemy_spawner.initialize_spawn_behavior()
        state.update_board()

        PLAYER_ACTION = Actions.STOP #placeholder action

        enemies_added = 0

        #Main game loop
        while state.turns_left > 4:
            # move each agents
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
                    agent_action = PLAYER_ACTION
                else:
                    agent_action = each_agent.autoPickAction()

                # len of current agents may change here, potentiall causing index error
                state = state.generateSuccessorState(each_index, agent_action)

                if (state.current_agents[len(state.current_agents) - 1].hasMoved() == True):
                    state.decrement_turn()
                    # spawn enemy based on spawn rate
                    #pick random number
                    probability_to_spawn = random.randint(0,100)
                    if probability_to_spawn <= enemy_spawner.spawn_rate:
                        #pick an enemy
                        enemy_to_spawn = enemy_spawner.choose_enemy()
                        state.addAgent(enemy_to_spawn)

                    if print_board:
                        print("Turn: " + str(state.turns_left))
                        print(state.gameBoard)
                        print(f"lives left: {state.current_player_lives}")
                        print(f"Win?\t{state.isWin()}\nLose?\t{state.isLose()}\n")

                    enemies_added += 1
                    if enemies_added > 5:
                        enemies_added = 5
                    self.assertEquals(enemies_added, len(state.current_agents) - 1)
            state.reset_agents_move_status()

        self.assertEquals(6, len(state.current_agents))

    def test_game_example_5(self):
        """
        Ramzi Branch 3
        Game Conditions:
            - 10 turns
            - player spawn in middle of board on furthest left col
            - Spawn rate is 100%
            - max enemies is 5
            - 2 enemy types SimpleGoLeft and EnemyAgentBasicFireAndMove
            - 1 enemy should spawn per turn up until turn 5, total 5 enemies
            - player will not move the whole time
        Tests:
             - amount of enemies by the end is 5
            - one enemy added per turn until 5 is reached
            - board renders correctly
        :return:
        """

        # set to true to print board to terminal/console for visual aid
        print_board = True

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 5
        # set small turns
        state.turns_left = 10
        # make a player size 1 X 1 at row=5,col=0 and add it
        player = PlayerAgent(1, 1, 5, 0)
        state.addAgent(player)

        # pass in gameboard to get spawn boundaries, 2nd param is spawn rate
        enemy_spawner = EnemyPicker(state.gameBoard, 100)
        enemy_spawner.add_enemy_to_spawn_list(SimpleGoLeftAgent(1, 1),
                                              50)  # pos doesn't matter it will be changed by spawner
        enemy_spawner.add_enemy_to_spawn_list(EnemyAgentBasicFireAndMove(1,1),
                                              50)
        #now 50/50 chance that enemy will be a Simple Go Left or an EnemyAgentBasicFireAndMove
        enemy_spawner.initialize_spawn_behavior()
        state.update_board()

        PLAYER_ACTION = Actions.STOP  # placeholder action

        enemies_added = 0

        # Main game loop
        while state.turns_left > 4:
            # move each agents
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
                    agent_action = PLAYER_ACTION
                else:
                    agent_action = each_agent.autoPickAction()

                # len of current agents may change here, potentiall causing index error
                state = state.generateSuccessorState(each_index, agent_action)

                if (state.current_agents[len(state.current_agents) - 1].hasMoved() == True):
                    state.decrement_turn()
                    if len(state.current_agents) - 1 < state.max_enemies_at_any_given_time:
                        # spawn enemy based on spawn rate
                        # pick random number
                        probability_to_spawn = random.randint(0, 100)
                        if probability_to_spawn <= enemy_spawner.spawn_rate:
                            # pick an enemy
                            enemy_to_spawn = enemy_spawner.choose_enemy()
                            state.addAgent(enemy_to_spawn)

                    if print_board:
                        state.update_board()
                        print("Turn: " + str(state.turns_left))
                        print("# Enemies on board: ", len(state.current_agents) - 1)
                        print("enemy positions: ")
                        for each in state.current_agents:
                            each_agent : AgentInterface = each
                            if each_agent.isPlayer() == False:
                                print(f"x = {each_agent.get_min_col_boundary()}, y = {each_agent.get_min_row_boundary()}, type: {type(each_agent)}")
                        print("# Projectiles on board: ", len(state.current_projectiles))
                        print(state.gameBoard)
                        print(f"lives left: {state.current_player_lives}")
                        print(f"Win?\t{state.isWin()}\nLose?\t{state.isLose()}\n")

                    enemies_added += 1
                    if enemies_added > 5:
                        enemies_added = 5

            state.reset_agents_move_status()

        self.assertEquals(6, len(state.current_agents))

    def test_gain_one_point_per_turn_survival(self):
        """
        Game Conditions:
            - Gain one point while Game Loop continues
            - Game loop will forcibly be broken early after 6 turns
        Tests:
            - Score should be 5 at the end
        :return:
        """

        # set to true to print board to terminal/console for visual aid
        print_board = False

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 5
        # set small turns
        state.turns_left = 10
        # make a player size 1 X 1 at row=5,col=0 and add it
        player = PlayerAgent(1, 1, 5, 0)
        state.addAgent(player)

        PLAYER_ACTION = Actions.STOP  # placeholder action

        # Main game loop
        while state.turns_left > 4:
            # move each agents
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
                    agent_action = PLAYER_ACTION
                else:
                    agent_action = each_agent.autoPickAction()

                # len of current agents may change here, potentiall causing index error
                state = state.generateSuccessorState(each_index, agent_action)

                if (state.current_agents[len(state.current_agents) - 1].hasMoved() == True):
                    state.decrement_turn()

                    if print_board:
                        print("Current Score: ", state.score)
                        print("Turns left: ", state.turns_left)
                        state.update_board()


            state.reset_agents_move_status()

        self.assertEquals(6, state.score)


    #TODO need to test head on collision

    def test_score_1(self):
        """
        Game Conditions:
            - Game lasts 1 turn
            - Only player on board
        Tests:
            - Final score should be score for winning + survival for one turn
                > 10000 + 1 = 10001
            - isWin should return True
        :return:
        """

        # set to true to print board to terminal/console for visual aid
        print_board = False

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 5
        # set small turns
        state.turns_left = 1
        # make a player size 1 X 1 at row=5,col=0 and add it
        player = PlayerAgent(1, 1, 5, 0)
        state.addAgent(player)

        PLAYER_ACTION = Actions.STOP  # placeholder action

        # Main game loop
        while state.isWin() == False:
            # move each agents
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
                    agent_action = PLAYER_ACTION
                else:
                    agent_action = each_agent.autoPickAction()

                # len of current agents may change here, potentiall causing index error
                state = state.generateSuccessorState(each_index, agent_action)

                if (state.current_agents[len(state.current_agents) - 1].hasMoved() == True):
                    state.decrement_turn()

                    if print_board:
                        print("Current Score: ", state.score)
                        print("Turns left: ", state.turns_left)
                        state.update_board()

            state.reset_agents_move_status()

        self.assertEquals(10_001, state.score)
        self.assertTrue(state.isWin())

    def test_score_2(self):
        """
        Game Conditions:
            - Game has 10 turns left until over
            - Player and BasicFireAndMove Agent on board
            - enemy will create a bullet on the first turn
                > At next turn the bullet should reduce hp of player,
                    but player has 3 hp so player not destroyed
            - Score reduced due to decrease in player hp
            - Game plays out until win due to survival
            - No Enemies destroyed
        Tests:
            - Final score should be score for loss of health + turns survived + points for winning
            - -100 + 10 + 10000 = 9910
            - isWin = True and isLose = False
            :return:
        """

        # set to true to print board to terminal/console for visual aid
        print_board = True

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 5
        # set small turns
        state.turns_left = 10
        # make a player size 1 X 1 at row=5,col=0 and add it
        player = PlayerAgent(1, 1, 5, 0)
        player.set_hp(3)
        e1 = EnemyAgentBasicFireAndMove(5,2)
        state.addAgent(player)
        state.addAgent(e1)
        state.update_board()

        PLAYER_ACTION = Actions.STOP  # placeholder action

        # Main game loop
        while True:
            # move each agents
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
                    agent_action = PLAYER_ACTION
                else:
                    if state.turns_left == 10:
                        agent_action = Actions.FIRE
                    else:
                        agent_action = Actions.STOP

                # len of current agents may change here, potentiall causing index error
                state = state.generateSuccessorState(each_index, agent_action)

                if (state.current_agents[len(state.current_agents) - 1].hasMoved() == True):
                    state.decrement_turn()

                    if print_board:
                        print("Current Score: ", state.score)
                        print("Turns left: ", state.turns_left)
                        print(f"Player hp: {state.current_agents[0].get_hp()}")
                        print(state.gameBoard)
                        state.update_board()

            state.reset_agents_move_status()
            if state.isWin() == True or state.isLose() == True:
                break

        self.assertEquals(9910, state.score)
        self.assertTrue(state.isWin())
        self.assertFalse(state.isLose())

    def test_score_3(self):
        """
        Game Conditions:
            - Game has 10 turns left until over
            - Player and BasicFireAndMove Agent on board
            - enemy will create a bullet on the first turn and second turn
                > At next turn the bullet should reduce hp of player,
                    but player has 3 hp so player not destroyed, and be left with 1 hp
            - Score reduced due to decrease in player hp
            - Game plays out until win due to survival
            - No Enemies destroyed
        Tests:
            - Final score should be score for (loss of health * 2) + turns survived + points for winning
            - (-100 * 2) + 10 + 10000 = 9810
            - isWin = True and isLose = False
            :return:
        """

        # set to true to print board to terminal/console for visual aid
        print_board = True

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 5
        # set small turns
        state.turns_left = 10
        # make a player size 1 X 1 at row=5,col=0 and add it
        player = PlayerAgent(1, 1, 5, 0)
        player.set_hp(3)
        e1 = EnemyAgentBasicFireAndMove(5, 2)
        state.addAgent(player)
        state.addAgent(e1)
        state.update_board()

        PLAYER_ACTION = Actions.STOP  # placeholder action

        # Main game loop
        while True:
            # move each agents
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
                    agent_action = PLAYER_ACTION
                else:
                    if state.turns_left > 8:
                        agent_action = Actions.FIRE
                    else:
                        agent_action = Actions.STOP

                # len of current agents may change here, potentiall causing index error
                state = state.generateSuccessorState(each_index, agent_action)

                if (state.current_agents[len(state.current_agents) - 1].hasMoved() == True):
                    state.decrement_turn()

                    if print_board:
                        print("Current Score: ", state.score)
                        print("Turns left: ", state.turns_left)
                        print(f"Player hp: {state.current_agents[0].get_hp()}")
                        print(state.gameBoard)
                        state.update_board()

            state.reset_agents_move_status()
            if state.isWin() == True or state.isLose() == True:
                break

        self.assertEquals(9810, state.score)
        self.assertTrue(state.isWin())
        self.assertFalse(state.isLose())

    def test_score_4(self):
        """
        Game Conditions:
            - Game has 10 turns left until over
            - Only player on board
            - enemy will create a bullet on the first turn
                > At next turn the bullet should reduce hp of player
            - Since player only has 1 life, this should end the game
        Tests:
            - Final score should be score for loss of health + loss of life + loss of game + 2 turn survive
                > -100 + -500 + -1000 + 2 = -1598
            - isLose should return True since only 1 life
            :return:
        """

        # set to true to print board to terminal/console for visual aid
        print_board = True

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 5
        # set small turns
        state.turns_left = 10
        # make a player size 1 X 1 at row=5,col=0 and add it
        player = PlayerAgent(1, 1, 5, 0)
        player.set_hp(1)
        e1 = EnemyAgentBasicFireAndMove(5, 3)
        state.addAgent(player)
        state.addAgent(e1)

        PLAYER_ACTION = Actions.STOP  # placeholder action

        if print_board: # print initial board
            print("Current Score: ", state.score)
            print("Turns left: ", state.turns_left)
            print(f"Player hp: {player.get_hp()}")
            state.update_board()
            print(state.gameBoard)

        # Main game loop
        while state.isWin() == False or state.isLose() == False:
            # move each agents
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

                agent_action = None # initialize var

                # making player action just stop for this example
                if each_agent.isPlayer():
                    agent_action = PLAYER_ACTION
                else:
                    if state.turns_left == 10: #Force enemy to fire on first turn
                        agent_action = Actions.FIRE
                    else:
                        # enemy moves randomly up or down after first turn
                        agent_action = random.choice([Actions.UP, Actions.DOWN])

                # len of current agents may change here, potentiall causing index error

                state = state.generateSuccessorState(each_index, agent_action)

                if (state.current_agents[len(state.current_agents) - 1].hasMoved() == True):
                    state.decrement_turn()

            if print_board:
                print("Current Score: ", state.score)
                print("Turns left: ", state.turns_left)
                print(f"Player hp: {player.get_hp()}")
                state.update_board()
                print(state.gameBoard)


            state.reset_agents_move_status()

            if state.isWin() == True or state.isLose() == True:

                if print_board:
                    print("Current Score: ", state.score)
                    print("Turns left: ", state.turns_left)
                    print(f"Player hp: {player.get_hp()}")
                    state.update_board()
                    print(state.gameBoard)

                break

        self.assertEquals(-1598, state.score)

    def test_score_player_destroys_simple_go_left_near(self):
        """
            Game Conditions:
                - Game has 10 turns left until over
                - Only player and 1 SimpleGoLeftAgent on board
                - Player will create a bullet on the first turn
                    > At next turn the bullet should reduce hp of SimpleGoLeft and destroy it
                - Player will gain points
            Tests:
                - Final score should be score for points for destroyed enemy + 10 turns survived + points for winning
                    > 10 + 10 + 10000 = 10020
                - isLose should return False
                - isWin should return True
            :return:
        """

        # set to true to print board to terminal/console for visual aid
        print_board = True

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 5
        # set small turns
        state.turns_left = 10
        # make a player size 1 X 1 at row=5,col=0 and add it
        player = PlayerAgent(1, 1, 5, 0)
        player.set_hp(1)
        e1 = SimpleGoLeftAgent(5, 2)
        state.addAgent(player)
        state.addAgent(e1)

        PLAYER_ACTION = Actions.STOP  # placeholder action

        if print_board:  # print initial board
            print("Current Score: ", state.score)
            print("Turns left: ", state.turns_left)
            print(f"Player hp: {player.get_hp()}")
            state.update_board()
            print(state.gameBoard)

        # Main game loop
        while state.isWin() == False or state.isLose() == False:
            # move each agents
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

                agent_action = None  # initialize var

                # making player action just stop for this example
                if each_agent.isPlayer():
                    if state.turns_left == 10:
                        agent_action = Actions.FIRE
                    else:
                        agent_action = PLAYER_ACTION
                else:
                    agent_action = each_agent.autoPickAction()

                # len of current agents may change here, potentiall causing index error

                state = state.generateSuccessorState(each_index, agent_action)

                if (state.current_agents[len(state.current_agents) - 1].hasMoved() == True):
                    state.decrement_turn()

            if print_board:
                print("Current Score: ", state.score)
                print("Turns left: ", state.turns_left)
                print(f"Player hp: {player.get_hp()}")
                state.update_board()
                print(state.gameBoard)

            state.reset_agents_move_status()

            if state.isWin() == True or state.isLose() == True:

                if print_board:
                    print("Current Score: ", state.score)
                    print("Turns left: ", state.turns_left)
                    print(f"Player hp: {player.get_hp()}")
                    state.update_board()
                    print(state.gameBoard)

                break

        self.assertEquals(10_020, state.score)

    def test_score_player_destroys_basic_fire_and_move(self):
        """
            Game Conditions:
                - Game has 10 turns left until over
                - Only player and 1 BasicFireAndMove on board
                - Player will create a bullet on the first turn
                    > At next turn:
                     -> the bullet will move one unit to the right
                     -> the enemy will move one unit to the left
                     -> the bullet should reduce hp of BasicFireAndMOve and destroy it
                - Player will gain points
            Tests:
                - Final score should be score for points for destroyed enemy + 10 turns survived + points for winning
                    > 25 + 10 + 10000 = 10035
                - isLose should return False
                - isWin should return True
                :return:
        """

        # set to true to print board to terminal/console for visual aid
        print_board = True

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 5
        # set small turns
        state.turns_left = 10
        # make a player size 1 X 1 at row=5,col=0 and add it
        player = PlayerAgent(1, 1, 5, 0)
        player.set_hp(1)
        e1 = EnemyAgentBasicFireAndMove(5, 2)
        state.addAgent(player)
        state.addAgent(e1)

        PLAYER_ACTION = Actions.STOP  # placeholder action

        if print_board:  # print initial board
            print("Current Score: ", state.score)
            print("Turns left: ", state.turns_left)
            print(f"Player hp: {player.get_hp()}")
            state.update_board()
            print(state.gameBoard)

        # Main game loop
        while state.isWin() == False or state.isLose() == False:
            # move each agents
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

                agent_action = None  # initialize var

                # making player action just stop for this example
                if each_agent.isPlayer():
                    if state.turns_left == 10:
                        agent_action = Actions.FIRE
                    else:
                        agent_action = PLAYER_ACTION
                else:
                    agent_action = Actions.LEFT

                # len of current agents may change here, potentiall causing index error

                state = state.generateSuccessorState(each_index, agent_action)

                if (state.current_agents[len(state.current_agents) - 1].hasMoved() == True):
                    state.decrement_turn()

            if print_board:
                print("Current Score: ", state.score)
                print("Turns left: ", state.turns_left)
                print(f"Player hp: {player.get_hp()}")
                state.update_board()
                print(state.gameBoard)

            state.reset_agents_move_status()

            if state.isWin() == True or state.isLose() == True:

                if print_board:
                    print("Current Score: ", state.score)
                    print("Turns left: ", state.turns_left)
                    print(f"Player hp: {player.get_hp()}")
                    state.update_board()
                    print(state.gameBoard)

                break

        self.assertEquals(10_035, state.score)

    def test_score_player_destroys_basic_heuristic_enemy(self):
        """
            Game Conditions:
                - Game has 10 turns left until over
                - Only player and 1 MoveFireHueristicAgent on board
                - Player will create a bullet on the first turn
                    > At next turn:
                     -> the bullet will move one unit to the right
                     -> the enemy will move one unit to the left
                     -> the bullet should reduce hp of MoveFireHueristicAgent and destroy it
                - Player will gain points
            Tests:
                - Final score should be score for points for destroyed enemy + 10 turns survived + points for winning
                    > 50 + 10 + 10000 = 10060
                - isLose should return False
                - isWin should return True
                :return:
        """

        # set to true to print board to terminal/console for visual aid
        print_board = True

        state = self.gamestateInit
        state.max_enemies_at_any_given_time = 5
        # set small turns
        state.turns_left = 10
        # make a player size 1 X 1 at row=5,col=0 and add it
        player = PlayerAgent(1, 1, 5, 0)
        player.set_hp(1)
        e1 = EnemyMoveFireHeuristicAgent(5, 2)
        state.addAgent(player)
        state.addAgent(e1)

        PLAYER_ACTION = Actions.STOP  # placeholder action

        if print_board:  # print initial board
            print("Current Score: ", state.score)
            print("Turns left: ", state.turns_left)
            print(f"Player hp: {player.get_hp()}")
            state.update_board()
            print(state.gameBoard)

        # Main game loop
        while state.isWin() == False or state.isLose() == False:
            # move each agents
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

                agent_action = None  # initialize var

                # making player action just stop for this example
                if each_agent.isPlayer():
                    if state.turns_left == 10:
                        agent_action = Actions.FIRE
                    else:
                        agent_action = PLAYER_ACTION
                else:
                    agent_action = Actions.LEFT

                # len of current agents may change here, potentiall causing index error

                state = state.generateSuccessorState(each_index, agent_action)

                if (state.current_agents[len(state.current_agents) - 1].hasMoved() == True):
                    state.decrement_turn()

            if print_board:
                print("Current Score: ", state.score)
                print("Turns left: ", state.turns_left)
                print(f"Player hp: {player.get_hp()}")
                state.update_board()
                print(state.gameBoard)

            state.reset_agents_move_status()

            if state.isWin() == True or state.isLose() == True:

                if print_board:
                    print("Current Score: ", state.score)
                    print("Turns left: ", state.turns_left)
                    print(f"Player hp: {player.get_hp()}")
                    state.update_board()
                    print(state.gameBoard)

                break

        self.assertEquals(10_060, state.score)



#ramzi merged
def main():
    unittest.main(verbosity=3)

if __name__ == '__main__':
    main()