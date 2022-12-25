import unittest

from Model.Agents.Actions import Actions
from Model.Agents.AgentInterface import AgentInterface
from Model.Agents.AgentSuperClass import AgentSuperClass
from Model.Agents.EnemyAgentBasicFireAndMove import EnemyAgentBasicFireAndMove
from Model.Agents.PlayerAgent import PlayerAgent
from Model.Agents.SimpleGoLeftAgent import SimpleGoLeftAgent
from Model.GameState import GameState
from Model.Projectiles.ProjectileInterface import ProjectileInterface

UP = Actions.UP
DOWN = Actions.DOWN
LEFT = Actions.LEFT
RIGHT = Actions.RIGHT
STOP = Actions.STOP
FIRE = Actions.FIRE

"""
This class tests the methods in the 
GameState class.
"""
class TestGameState(unittest.TestCase):
    def setUp(self) -> None:
        """
        Sets up variables to use. These variables are
        reset prior to every test
        :return: None
        """
        self.gamestateInit = GameState()
        self.gameState_2 = GameState()

    # test default values
    def test_default_values(self) -> None:
        """
        Test default GameState constructor values
        :return: None
        """
        g = self.gamestateInit
        self.assertEquals(0,len(g.current_agents))
        self.assertFalse(g.isPlayerAdded)
        self.assertEquals(100, g.turns_left)
        self.assertEquals(1, g.max_enemies_at_any_given_time)

    #testing trying to add player agent in valid position
    def test_is_valid_agent_player(self) -> None:
        """
        Testing isValidAgent method with a player with a
        valid location (i.e. inside the GameBoard)
        :return:
        """
        temp_p = PlayerAgent(1,1,4,5)
        isValid = self.gamestateInit.isValidAgent(temp_p)
        self.assertTrue(isValid)

    def test_is_valid_enemy_agents(self):
        """
        Testing Valid and InValid enemy agent locations via isValidAgent method.
        Valid:
        - Beyond col minimum boundary of board (represent exiting board)
        - Beyond col maximum of board (represent spawning into board)
        Invalid:
        - Beyond row maximum (should not be able to go "above" the board)
        - Beyond row minimum (should not be able to go "below" the board)
        :return: None
        """
        board_min_col_boundary = self.gamestateInit.gameBoard.min_col
        board_max_x_boundary = self.gamestateInit.gameBoard.board_max_x_boundary
        board_min_row_boundary = self.gamestateInit.gameBoard.min_row
        board_max_y_boundary = self.gamestateInit.gameBoard.board_max_y_boundary

        invalidCount = 0
        agentsList = []

        invalid_tuples = [
            # go one row lower than minimum board min
            (board_min_row_boundary - 1, board_min_col_boundary),
            # go one col lower than board min, enemy is allowed to do this
            # enemy agents allowed to go beyond board_min_bounds
            (board_min_row_boundary, board_min_col_boundary - 1),
            # go one higher than max row of board
            (board_max_y_boundary + 1, board_max_x_boundary),
            # go one higher than max col of board, enemy is allowed to do this
            # enemy agents allowed to come in from col > board_col_max bounds
            (board_max_y_boundary, board_max_x_boundary + 1)]

        for each in invalid_tuples:
            enemy_agent = AgentSuperClass(lowest_row=each[0], least_col=each[1])
            agentsList.append(enemy_agent)

        for eachAgent in agentsList:
            isValid = self.gamestateInit.isValidAgent(eachAgent)
            if isValid == False:
                invalidCount += 1

        self.assertEqual(2, invalidCount)

    #testing trying to add player agent who is out of bounds
    def test_not_valid_agent_player(self):
        """
        Testing invalid player agent locations via isValidAgent method.
        Invalid cases:
        - Above board
        - Below Board
        - To the right of board (beyond max col)
        - To the left of board (beyond min col)
        :return:
        """
        board_min_col_boundary = self.gamestateInit.gameBoard.min_col
        board_max_x_boundary = self.gamestateInit.gameBoard.board_max_x_boundary
        board_min_row_boundary = self.gamestateInit.gameBoard.min_row
        board_max_y_boundary = self.gamestateInit.gameBoard.board_max_y_boundary

        invalidCount = 0
        agentsList = []

        invalid_tuples = [
            # go one row lower than minimum board min
            (board_min_row_boundary-1, board_min_col_boundary),
            #go one col lower than board min
            (board_min_row_boundary,board_min_col_boundary - 1),
            #go one higher than max row of board
            (board_max_y_boundary + 1, board_max_x_boundary),
            # go one higher than max col of board
            (board_max_y_boundary, board_max_x_boundary + 1)]

        for each in invalid_tuples:
            temp_p = PlayerAgent(lowest_row=each[0],least_col=each[1])
            agentsList.append(temp_p)

        for eachAgent in agentsList:
            isValid = self.gamestateInit.isValidAgent(eachAgent)
            if isValid == False:
                invalidCount += 1

        self.assertEqual(4,invalidCount)


    def test_add_valid_player(self) -> None:
        """
        Testing adding valid player agent to gamestate via
        addAgent method
        :return: None
        """
        p1 = PlayerAgent()
        self.gameState_2.addAgent(p1)
        self.assertTrue(self.gameState_2.isPlayerAdded)
        self.assertEquals(1, len(self.gameState_2.current_agents))

    def test_adding_2_players(self):
        """
        Testing trying to add 2 players to gamestate.
        This is not allowed.
        :return:
        """
        p1 = PlayerAgent()
        self.gameState_2.addAgent(p1)
        player_2 = PlayerAgent()
        self.assertFalse(self.gameState_2.addAgent(player_2))
        self.assertEquals(1,len(self.gameState_2.current_agents) )

    def testGetAllLegalActionsPlayer(self):
        """
        Testing getting all legal actions of a player agent via
        getAllLegalActions method.
        :return: None
        """
        valid_p1 = PlayerAgent()
        self.gamestateInit.addAgent(valid_p1)
        p1_legal_actions = self.gamestateInit.getAllLegalActions(0)
        # from 0,0 (bottom left corner) player can move up, right, stop or fire = 4 actions
        self.assertEquals(4, len(p1_legal_actions))
        self.assertEquals(
            [Actions.UP, Actions.RIGHT, Actions.STOP, Actions.FIRE],
            p1_legal_actions)

        gameState3 = GameState()
        # from (9,9) top right corner player can move left, down, stop , or fire
        valid_p2 = PlayerAgent(1,1,9,9)
        gameState3.addAgent(valid_p2)
        p2_legal_actions = gameState3.getAllLegalActions(0)
        gameState3.getAllLegalActions(0)
        print(p2_legal_actions)
        self.assertEquals(4,len(p2_legal_actions))
        self.assertEquals([Actions.LEFT, Actions.DOWN, Actions.STOP,Actions.FIRE],
                          p2_legal_actions)

        #from center of board move anywhere
        gameState4 = GameState()
        valid_p3 = PlayerAgent(1, 1, 5, 5)
        gameState4.addAgent(valid_p3)
        p3_legal_actions = gameState4.getAllLegalActions(0)
        gameState4.getAllLegalActions(0)
        self.assertEquals(6, len(p3_legal_actions))
        self.assertEquals([Actions.UP, Actions.LEFT, Actions.RIGHT, Actions.DOWN, Actions.STOP, Actions.FIRE],
                          p3_legal_actions)



    def test_player_enemy_legal_actions_together_far_away(self):
        """
        Testing getting all legal actions of a player and a SimpleGoLeftAgent
        Default heights and lengths for player.
        Enemy and player far apart.
        :return: None
        """
        #TODO Ramzi_iter_1 show team

        #set to true to see board
        print_board = False

        valid_p1 = PlayerAgent()
        valid_enemy_1 = SimpleGoLeftAgent(9,9)
        self.gamestateInit.addAgent(valid_p1)
        self.gamestateInit.addAgent(valid_enemy_1)
        self.assertEquals(2,len(self.gamestateInit.current_agents))

        p1_legal_actions = self.gamestateInit.getAllLegalActions(0)
        # from 0,0 (bottom left corner) player can move up, right, stop or fire = 4 actions
        self.assertEquals(4, len(p1_legal_actions))
        self.assertEquals(
            [Actions.UP, Actions.RIGHT, Actions.STOP, Actions.FIRE],
            p1_legal_actions)

        enemy_1_legal_actions = self.gamestateInit.getAllLegalActions(1)
        self.assertEquals(1,len(enemy_1_legal_actions))
        self.assertEquals([Actions.LEFT], enemy_1_legal_actions)

        if print_board:
            self.gamestateInit.update_board()
            print(self.gamestateInit.gameBoard)

        gameState3 = GameState()
        valid_p2 = PlayerAgent(1, 1, 5, 5)
        gameState3.addAgent(valid_p2)
        valid_e2 = SimpleGoLeftAgent(9,9)
        gameState3.addAgent(valid_e2)
        p2_legal_actions = gameState3.getAllLegalActions(0)
        e2_legal_actions = self.gamestateInit.getAllLegalActions(1)

        self.assertEquals(1, len(e2_legal_actions))
        self.assertEquals([Actions.LEFT], e2_legal_actions)

        self.assertEquals(6, len(p2_legal_actions))
        self.assertEquals([Actions.UP, Actions.LEFT, Actions.RIGHT, Actions.DOWN, Actions.STOP, Actions.FIRE],
                          p2_legal_actions)

        if print_board:
            gameState3.update_board()
            print(gameState3.gameBoard)

    def test_player_enemy_legal_actions_together_close_to_each_other(self):
        """
        Testing getting all legal actions of a player and a SimpleGoLeftAgent
        Default heights and lengths for player.
        Enemy and player next to each other
        :return: None
        """
        # TODO Ramzi_iter_1 show team

        # set to true to see board
        print_board = False

        valid_p1 = PlayerAgent(1,1,5,5)
        valid_enemy_1 = SimpleGoLeftAgent(5, 6)
        self.gamestateInit.addAgent(valid_p1)
        self.gamestateInit.addAgent(valid_enemy_1)
        self.assertEquals(2, len(self.gamestateInit.current_agents))

        p1_legal_actions = self.gamestateInit.getAllLegalActions(0)
        # from 0,0 (bottom left corner) player can move up, right, stop or fire = 4 actions
        self.assertEquals(6, len(p1_legal_actions))
        self.assertEquals(
            [Actions.UP, Actions.LEFT, Actions.RIGHT, Actions.DOWN, Actions.STOP, Actions.FIRE],
            p1_legal_actions)

        enemy_1_legal_actions = self.gamestateInit.getAllLegalActions(1)
        self.assertEquals(1, len(enemy_1_legal_actions))
        self.assertEquals([Actions.LEFT], enemy_1_legal_actions)

        if print_board:
            self.gamestateInit.update_board()
            print(self.gamestateInit.gameBoard)



        #TODO test player and enemy getLegalActions together

    def testGetAllLegalActionsPlayerLargerHeight(self):
        """
        Testing getting all legal actions of a player agent via
        getAllLegalActions method. Player has height = 2
        :return: None
        """
        #TODO Ramzi_iter_1 show team

        # set to true to print board
        print_board = False

        valid_p1 = PlayerAgent(1,2,8,0)
        self.gamestateInit.addAgent(valid_p1)
        p1_legal_actions = self.gamestateInit.getAllLegalActions(0)
        # from 8,0 (top left corner) player can move right, down, stop or fire = 4 actions
        self.assertEquals(4, len(p1_legal_actions))
        self.assertEquals(
            [Actions.RIGHT, Actions.DOWN, Actions.STOP, Actions.FIRE],
            p1_legal_actions)

        if (print_board):
            self.gamestateInit.update_board()
            print(self.gamestateInit.gameBoard)

        gameState3 = GameState()
        # player at row = 8 with height = 2
        # should not be able to move up
        # from (8,9) top right corner player can move left, down, stop , or fire
        valid_p2 = PlayerAgent(1, 2, 8, 9)
        gameState3.addAgent(valid_p2)
        p2_legal_actions = gameState3.getAllLegalActions(0)
        gameState3.getAllLegalActions(0)
        self.assertEquals(4, len(p2_legal_actions))
        self.assertEquals([Actions.LEFT, Actions.DOWN, Actions.STOP, Actions.FIRE],
                          p2_legal_actions)

        if (print_board):
            gameState3.update_board()
            print(gameState3.gameBoard)

        gameState4 = GameState()
        # player at row = 8 with height = 2
        # should not be able to move up
        # from (8,9) top right corner player can move left, down, stop , or fire
        valid_p3 = PlayerAgent(1, 2, 5, 5)
        gameState4.addAgent(valid_p3)
        p3_legal_actions = gameState4.getAllLegalActions(0)
        gameState4.getAllLegalActions(0)
        self.assertEquals(6, len(p3_legal_actions))
        self.assertEquals([Actions.UP, Actions.LEFT, Actions.RIGHT, Actions.DOWN, Actions.STOP, Actions.FIRE],
                          p3_legal_actions)

        if (print_board):
            gameState4.update_board()
            print(gameState4.gameBoard)

    def testGetAllLegalActionsPlayerLargerLength(self):
        """
        Testing getting all legal actions of a player agent via
        getAllLegalActions method. Player has height = 2
        :return: None
        """
        #TODO RAmzi_iter_1 show team
        # set to true to print board
        print_board = True

        valid_p1 = PlayerAgent(2, 1, 9, 0)
        self.gamestateInit.addAgent(valid_p1)
        p1_legal_actions = self.gamestateInit.getAllLegalActions(0)
        # from 8,0 (top left corner) player can move right, down, stop or fire = 4 actions
        self.assertEquals(4, len(p1_legal_actions))
        self.assertEquals(
            [Actions.RIGHT, Actions.DOWN, Actions.STOP, Actions.FIRE],
            p1_legal_actions)

        if (print_board):
            self.gamestateInit.update_board()
            print(self.gamestateInit.gameBoard)

        gameState3 = GameState()
        # player at row = 8 with height = 2
        # should not be able to move up
        # from (8,9) top right corner player can move left, down, stop , or fire
        valid_p2 = PlayerAgent(2, 1, 9, 8)
        gameState3.addAgent(valid_p2)
        p2_legal_actions = gameState3.getAllLegalActions(0)
        gameState3.getAllLegalActions(0)
        self.assertEquals(4, len(p2_legal_actions))
        self.assertEquals([Actions.LEFT, Actions.DOWN, Actions.STOP, Actions.FIRE],
                          p2_legal_actions)
        # set to true to print board
        if (print_board):
            gameState3.update_board()
            print(gameState3.gameBoard)

        gameState4 = GameState()
        # player at row = 8 with height = 2
        # should not be able to move up
        # from (8,9) top right corner player can move left, down, stop , or fire
        valid_p3 = PlayerAgent(2, 1, 5, 5)
        gameState4.addAgent(valid_p3)
        p3_legal_actions = gameState4.getAllLegalActions(0)
        gameState4.getAllLegalActions(0)
        self.assertEquals(6, len(p3_legal_actions))
        self.assertEquals([Actions.UP, Actions.LEFT, Actions.RIGHT, Actions.DOWN, Actions.STOP, Actions.FIRE],
                          p3_legal_actions)

        if (print_board):
            gameState4.update_board()
            print(gameState4.gameBoard)

    def testCheckPlayerAgentClashes_no_clash_simple(self):
        """
        Testing to see if player clashes with enemy agent via
        checkPlayerAgentClashes.
        In this case player and agent are near each other but
        do not overlap. There should be no clash and
        amount of agents should remain the same.

        Set print_board variable to True for visual aid
        :return: None
        """
        # set to true to print board to terminal/console for visual aid
        print_board = False

        player = PlayerAgent(1,1,3,3)
        enemy_1 = SimpleGoLeftAgent(3,4)
        state = self.gamestateInit

        state.addAgent(player)
        state.addAgent(enemy_1)

        #no clashes agents should be right next to each other
        state.checkPlayerAgentClashes()
        state.update_board()

        self.assertEquals(1,state.gameBoard.board_array[3][3])
        self.assertEquals(2, state.gameBoard.board_array[3][4])
        self.assertEquals(2,len(state.current_agents))

        if print_board:
            print(state.gameBoard)
            print("/****** END OF testCheckPlayerAgentClashes_no_clash_simple *****/\n")


    def test_check_clash_player_vs_simple(self):
        """
        Testing to see if player clashes with enemy agent via
        checkPlayerAgentClashes.
        In this case player and enemy agent are in the same
        position. Both should lose 1 hp. Since both only
        have 1 hp, both should be removed from current agents.

        Set print_board variable to True for visual aid
        :return:
        """
        #This also tests updateAgentsList
        # set to true to print board to terminal/console for visual aid
        print_board = False

        #player and agent on same space, should both lose 1 hp and die
        player = PlayerAgent(1, 1, 4, 4)
        enemy_1 = SimpleGoLeftAgent(4, 4)

        state = self.gamestateInit

        state.addAgent(player)
        state.addAgent(enemy_1)

        # agents should clash and both die
        state.checkPlayerAgentClashes()
        state.updateAgentsList()
        state.update_board()

        # agents should have been removed since both lost 1 hp and died
        self.assertEqual(0, len(state.current_agents))
        self.assertEqual(0, state.gameBoard.board_array[4][4])

        if print_board:
            print("KEY:\n0 = Empty Space\n1 = Player\n> 1 = Enemy Agent")
            print(state.gameBoard)
            print("/***** END OF test_check_clash_player_vs_simple *****/\n")

    def test_agent_clash_with_enemy_index_2(self):
        """
        Testing to see if player clashes with enemy agent via
        checkPlayerAgentClashes.
        In this case there are 3 agents -> 1 player and 2 enemies
        Player (agent index=0) and Enemy 2 (agent index=2)
        are in the same position so both should
        lose 1 hp. Since both only have 1 hp, both should be
        removed from current agents.
        However, Enemy 1 (agent index = 1) should still exist.

        Set print_board variable to True for visual aid
        :return:

        """
        # This also tests updateAgentsList
        # set to true to print board to terminal/console for visual aid
        print_board = False

        # player and agent on same space, should both lose 1 hp and die
        player = PlayerAgent(1, 1, 4, 4)
        enemy_1 = SimpleGoLeftAgent(5,6)
        enemy_2 = SimpleGoLeftAgent(4,4)

        # need to allow more than 1 enemy at a time
        state = GameState(max_enemies_at_one_time=2)

        state.addAgent(player)
        state.addAgent(enemy_1)
        state.addAgent(enemy_2)

        # player and enemy 2 clash and both die
        state.checkPlayerAgentClashes()
        state.updateAgentsList()
        state.update_board()

        #enemy 1 still exists though
        self.assertEqual(1, len(state.current_agents))
        self.assertEquals(2,state.gameBoard.board_array[5][6])
        #neither enemy_2 or player should occupy this position
        self.assertEqual(0, state.gameBoard.board_array[4][4])

        if print_board:
            print("KEY:\n0 = Empty Space\n1 = Player\n> 1 = Enemy Agent")
            print(state.gameBoard)
            print("/***** END OF test_check_clash_player_vs_simple *****/\n")

    def test_generate_successor_state_player_moves_valid(self):
        """
        Testing generateSuccessorState method.
        This case only uses player agent in agent list
        and uses valid actions. So player should be able to
        move to new location.
        This new state should contain an updated agent list
        (i.e. agents in new position / any changes to agent hp)

        Set print_board variable to True for visual aid
        :return: None
        """
        # set to true to print board to terminal/console for visual aid
        print_board = False

        state = self.gamestateInit
        player = PlayerAgent(1, 1, 4, 4)
        state.addAgent(player)

        newState = state.generateSuccessorState(0,LEFT)
        #check previous position now empty
        self.assertEquals(0, newState.gameBoard.board_array[4][4])
        #check new position NOT empty
        self.assertEquals(1,newState.gameBoard.board_array[4][3])


        if (print_board):
            print("Player initial position:\n\tx= 4, y = 4")
            print("Player moves left (col - 1), so new position:\n\tx = 3, y = 4")
            print(newState.gameBoard)
            print("-" * 40 + "\n")

        newState = newState.generateSuccessorState(0,UP)
        #check old position is empty
        self.assertEquals(0, newState.gameBoard.board_array[4][3])
        #check new position NOT empty on board
        self.assertEquals(1,newState.gameBoard.board_array[5][3])

        if (print_board):
            print("Player initial position:\n\tx= 3, y = 4")
            print("Player moves up (row + 1), so new position:\n\tx = 3, y = 5")
            print(newState.gameBoard)
            print("-" * 40 + "\n")


        newState = newState.generateSuccessorState(0, DOWN)
        # check previous position now empty
        self.assertEquals(0, newState.gameBoard.board_array[5][3])
        # check new position NOT empty on board
        self.assertEquals(1, newState.gameBoard.board_array[4][3])

        if (print_board):
            print("Player initial position:\n\tx= 3, y = 5")
            print("Player moves down (row - 1), so new position:\n\tx = 3, y = 4")
            print(newState.gameBoard)
            print("-" * 40 + "\n")

        newState = newState.generateSuccessorState(0,RIGHT)
        # check previous position now empty
        self.assertEquals(0, newState.gameBoard.board_array[4][3])
        # check new position NOT empty on board
        self.assertEquals(1, newState.gameBoard.board_array[4][4])

        if (print_board):
            print("Player initial position:\n\tx= 3, y = 4")
            print("Player moves down (row - 1), so new position:\n\tx = 4, y = 4")
            print(newState.gameBoard)
            print("-" * 40 + "\n")
            print("/****** END OF test_generate_successor_state_player_moves_valid *****/\n")

        #TODO repeat test but with larger player length and height


    def test_generate_successor_state_player_invalid_moves(self):
        """
        Testing generateSuccessorState method.
        This case only uses player agent in agent list
        and uses invalid actions. So player should just
        end up in the same position as initial.

        This new state should contain an updated agent list
        (i.e. agents in new position / any changes to agent hp)

        Set print_board variable to True for visual aid
        :return:
        """
        # set to true to print board to terminal/console for visual aid
        print_board = True

        state = self.gamestateInit
        #agent in bottom corner, should not be able to move down or left
        player = PlayerAgent(1, 1, 0, 0)
        state.addAgent(player)

        newState = state.generateSuccessorState(0,LEFT)
        #check current position is 1
        self.assertEquals(1, newState.gameBoard.board_array[0][0])
        #check surrounding position = 0
        self.assertEquals(0, newState.gameBoard.board_array[1][0])
        self.assertEquals(0, newState.gameBoard.board_array[0][1])

        if (print_board):
            print("Player initial position:\n\tx= 0, y = 0")
            print("Player can NOT move left (i.e cannot col - 1), so new position:\n\tx = 0, y = 0")
            print(newState.gameBoard)
            print("-" * 40 + "\n")

        newState = state.generateSuccessorState(0, DOWN)
        # check current position is 1
        self.assertEquals(1, newState.gameBoard.board_array[0][0])
        # check surrounding position = 0
        self.assertEquals(0, newState.gameBoard.board_array[1][0])
        self.assertEquals(0, newState.gameBoard.board_array[0][1])

        if (print_board):
            print("Player initial position:\n\tx= 0, y = 0")
            print("Player can NOT move down (i.e cannot row - 1), so new position:\n\tx = 0, y = 0")
            print(newState.gameBoard)
            print("-" * 40 + "\n")

        #manually move player to top right corner to perform tests there
        player_agent: AgentInterface = newState.current_agents[0]
        player_agent.set_position(9,9)

        newState = newState.generateSuccessorState(0, UP)
        # check current position is 1
        self.assertEquals(1, newState.gameBoard.board_array[9][9])
        # check surrounding position = 0
        self.assertEquals(0, newState.gameBoard.board_array[8][9])
        self.assertEquals(0, newState.gameBoard.board_array[9][8])

        if (print_board):
            print("Player initial position:\n\tx= 9, y = 9")
            print("Player can NOT move down (i.e cannot row + 1), so new position:\n\tx = 9, y = 9")
            print(newState.gameBoard)
            print("-" * 40 + "\n")

        newState = newState.generateSuccessorState(0, RIGHT)
        # check curret position is 1
        self.assertEquals(1, newState.gameBoard.board_array[9][9])
        # check surrounding position = 0
        self.assertEquals(0, newState.gameBoard.board_array[8][9])
        self.assertEquals(0, newState.gameBoard.board_array[9][8])

        if (print_board):
            print("Player initial position:\n\tx= 9, y = 9")
            print("Player can NOT move down (i.e cannot col + 1), so new position:\n\tx = 9, y = 9")
            print(newState.gameBoard)
            print("-" * 40 + "\n")
            print("/****** END OF test_generate_successor_state_player_invalid_moves *****/\n")

        #TODO maybe make test with diff board_height and lenght too?

    def test_gen_successor_state_enemy_incoming_and_outbound(self):
        """
        Testing generateSuccessorState method.
        This case has a single player agent
        and a singe enemy agent (SimpleGoLeftAgent)
        in current agents list.
        This case is testing valid enemy agent action,
        namely spawning in to the board (beyond board col/x max boundary)
        and exiting board (beyond board col/x min boundary)
        Enemy agent should be able to transition to new position.

        This new state should contain an updated agent list
        (i.e. agents in new position / any changes to agent hp,
        any removed agents gone as well)

        Set print_board variable to True for visual aid
        :return:
        """
        # set to true to print board to terminal/console for visual aid
        print_board = False

        state = self.gamestateInit

        #make a player and add it
        player = PlayerAgent(1, 1, 0, 0)
        state.addAgent(player)

        #enemy start off by being off screen, so coming in from the right
        enemy_1 = SimpleGoLeftAgent(7,10)
        #this should be allowed
        state.addAgent(enemy_1)
        #initial state so need to update board to reflect added agents
        state.update_board()

        #check agent list
        self.assertEquals(2,len(state.current_agents))

        if (print_board):
            print("Enemy initially coming in from right side off screen, only player can be seen at 0,0")
            print(state.gameBoard)
            print("-" * 40 + "\n")

        # simple left agent only goes left
        newState = state.generateSuccessorState(1,LEFT)
        self.assertEquals(2, newState.gameBoard.board_array[7][9])

        if (print_board):
            print("Enemy coming from offscreen should now be able to be seen at x=9,y=7")
            print(newState.gameBoard)
            print("-" * 40 + "\n")


        # move enemy agent to min col boundary of board
        for i in range(9):
            newState = newState.generateSuccessorState(1,LEFT)

        if print_board:
            print("Manually moving enemy to near min col boundary\nx=0,y=7")
            print(newState.gameBoard)
            print("-" * 40 + "\n")

        #now have enemy exit board
        newState = newState.generateSuccessorState(1,LEFT)
        self.assertEquals(1,len(newState.current_agents))
        #check that where enemy was is empty again
        self.assertEquals(0, newState.gameBoard.board_array[7][1])

        if print_board:
            print("Enemy has moved off board after LEFT action, \nshould no longer be visible at x=0,y=7")
            print(newState.gameBoard)
            print("-" * 40 + "\n")
            print("/****** END OF test_gen_successor_state_enemy_incoming_and_outbound *****/\n")

    def test_generateSuccessorState_edge_case_player_enemy_next_to_each_other(self):
        # set to true to print board to terminal/console for visual aid
        print_board = False

        state = self.gamestateInit

        # make a player and add it
        player = PlayerAgent(1, 1, 5, 5)
        state.addAgent(player)

        enemy_1 = SimpleGoLeftAgent(5, 6)
        # this should be allowed
        state.addAgent(enemy_1)
        # initial state so need to update board to reflect added agents
        state.update_board()

        newState = state.generateSuccessorState(0, Actions.RIGHT)
        self.assertEquals(True, newState.isLose())
        #newState = newState.generateSuccessorState(1,Actions.LEFT)
        #newState.update_board()
        #print(newState.gameBoard)



    def test_generateSuccessorState_player_fires_SimpleAgentBullet_diff_speeds(self):
        """
        Test that a player taking the action Actions.Fire will add
        a player bullet to the self.curent_projectiles list.
        Speed of SimpleBulletAgent = 1
        :return:
        """
        #set to true to see game board visualization

        print_board = True
        state = self.gamestateInit

        # make a player and add it
        player = PlayerAgent(1, 1, 0, 0)
        state.addAgent(player)

        newState = state.generateSuccessorState(0,Actions.FIRE)
        newState.update_board()
        self.assertEquals(1,len(newState.current_projectiles))

        if print_board:
            print("Key:\nPlayer = 1\nPlayer Bullet = X")
            print(newState.gameBoard)

    def test_generateSuccessorState_enemy_fires_SimpleAgentBullet_s1(self):
        """
        Test that an enemy taking the action Actions.Fire will add
        a enemy bullet to the self.current_projectiles list.
        Speed of SimpleBulletAgent = 1
        :return:
        """
        #set to true to see game board visualization

        print_board = True
        state = self.gamestateInit

        # make a player and add it
        player = PlayerAgent(1, 1, 0, 0)
        state.addAgent(player)
        enemy = EnemyAgentBasicFireAndMove(5,9)
        state.addAgent(enemy)

        newState = state.generateSuccessorState(1,Actions.FIRE)
        newState.update_board()
        self.assertEquals(1,len(newState.current_projectiles))

        if print_board:
            print("Key:\nPlayer = 1\nEnemy > 1\nPlayer Bullet = X, Enemy Bullet = B")
            print(newState.gameBoard)

    def test_moveAllProjectiles(self):
        """
        Testing moving simple projectiles
        :return:
        """
        print_board = True
        state = self.gamestateInit

        # make a player and add it
        player = PlayerAgent(1, 1, 0, 0)
        state.addAgent(player)
        enemy = EnemyAgentBasicFireAndMove(5, 9)
        state.addAgent(enemy)
        state.update_board()

        print(state.gameBoard)

        #TODO RAMZI what if both enemy and player fire at the same "time"
        newState = state.generateSuccessorState(0, Actions.FIRE)
        print(newState.gameBoard)
        newState = newState.generateSuccessorState(1,Actions.FIRE)
        newState = newState.moveAllProjectiles()
        newState.update_board()

        self.assertEquals(2, len(newState.current_projectiles))
        self.assertEquals((0,2), newState.current_projectiles[0].get_position())
        self.assertEquals((5,7), newState.current_projectiles[1].get_position())

        if print_board:
            print(newState.gameBoard)

    def test_moveProjectiles_in_gamestate(self):
        print_board = True
        state = self.gamestateInit

        # make a player and add it
        player = PlayerAgent(1, 1, 0, 0)
        state.addAgent(player)
        enemy = EnemyAgentBasicFireAndMove(5, 9)
        state.addAgent(enemy)
        state.update_board()

        if print_board:
            print("initial state")
            print(state.gameBoard)

        #player fires
        newState = state.generateSuccessorState(0, Actions.FIRE)
        # enemy fires
        newState = newState.generateSuccessorState(1, Actions.FIRE)
        self.assertEquals((0, 1), newState.current_projectiles[0].get_position())
        self.assertEquals((5, 8), newState.current_projectiles[1].get_position())

        if print_board:
            print("Player bullet should be at pos row=0, col=1")
            print("Enemy bullet should be at pos row = 5, col=8")
            print(newState.gameBoard)

        newState.reset_agents_move_status()
        # the projectiles should have moved
        newState = newState.generateSuccessorState(0,Actions.STOP)
        newState = newState.generateSuccessorState(1, Actions.LEFT)
        self.assertEquals((0, 2), newState.current_projectiles[0].get_position())
        self.assertEquals((5, 7), newState.current_projectiles[1].get_position())


        if print_board:
            print("Player bullet should be at row=0, col=2")
            print("Enemy bullet should be at row=5, col=5")
            print(newState.gameBoard)

    def test_checkBulletAgentClashes(self):
        """
        1 player fires bullet, 1 enemy approaches bullet
        bullet hits enemy
        :return:
        """
        print_board = True
        state = self.gamestateInit

        # make a player and add it
        player = PlayerAgent(1, 1, 5, 0)
        state.addAgent(player)
        enemy = SimpleGoLeftAgent(5, 9)
        state.addAgent(enemy)
        newState = state.generateSuccessorState(0,Actions.FIRE)
        newState.reset_agents_move_status()

        for i in range(4):
            newState = newState.generateSuccessorState(0, Actions.STOP)
            newState = newState.generateSuccessorState(1, Actions.LEFT)
            newState.reset_agents_move_status()

        if print_board:
            print(newState.gameBoard)

        self.assertEquals(1, len(newState.current_agents))
        self.assertEquals(0,len(newState.current_projectiles))

    def test_checkBulletAgentClashesFlyBy(self):
        """
        1 enemy fires bullet
        bullet hits player
        :return:
        """
        #TODO Ramzi fix test
        print_board = True
        state = self.gamestateInit
        state.turns_left = 10

        # make a player and add it
        player = PlayerAgent(1, 1, 5, 0)
        state.addAgent(player)
        enemy = EnemyAgentBasicFireAndMove(5, 8)
        state.addAgent(enemy)
        newState = state.generateSuccessorState(0, Actions.STOP)
        #bullet originates at row=5, col=7
        newState = newState.generateSuccessorState(1, Actions.FIRE)


        while newState.isWin() == False and newState.isLose() == False:
            if print_board:
                print(f"Turns left {newState.turns_left}")
                print(newState.gameBoard)

            # for j in range(len(newState.current_projectiles)):
            #     current_bullet : ProjectileInterface = newState.current_projectiles[j]
            #     moved_bullet = current_bullet.take_action(current_bullet.autoPickAction())
            #     newState.current_projectiles[j] = moved_bullet

            if newState.turns_left == 4:
                print("hello")

            for k in range(len(newState.current_agents)):
                newState = newState.generateSuccessorState(k, Actions.STOP)

            newState.decrement_turn()
            newState.reset_agents_move_status()
            newState.update_board()


        self.assertEquals(1, len(newState.current_agents))
        agent_left : AgentInterface = newState.current_agents[0]
        self.assertFalse(agent_left.isPlayer())
        self.assertEquals(0,len(newState.current_projectiles))



def main():
    unittest.main(verbosity=3)

if __name__ == '__main__':
    main()