from Model.Agents.AgentInterface import AgentInterface
from Model.Projectiles.ProjectileInterface import ProjectileInterface



class GameBoard:
    '''
    This class represents a GameBoard, which is the environment the agents
    will be traversing through.
    '''

    def __init__(self, board_length: int,
                 board_height: int, minimum_x: int = 0,
                 minimum_y: int = 0):
        '''
        This represents the GameBoard for AegisWing
        It will be used to render a visual representation
        of agents and their positions
        :param board_length: {int} the length of the board
        :param board_height: {int} the height of the board
        :param minimum_x: {int} the lowest x/column value for the board, by default it is 0
        :param minimum_y: {int} the lowest y/row value for the board, by default it is 0
        '''

        if (board_length <= 2):
            raise ValueError("board length cannot be less than 2")
        if (board_height <= 2):
            raise ValueError("board height cannot be less than 2")

        self.board_length = board_length  # amount of col
        self.board_height = board_height  # amount of rows
        self.min_col = minimum_x  # least column value
        self.min_row = minimum_y  # least row value

        # storing board as a 2D array, each row starts at x = 0
        # so if board is 10 units long, then x = {0,1,2...9}
        self.board_max_x_boundary = self.min_col + board_length - 1
        self.board_max_y_boundary = self.min_row + board_height - 1
        self.setUpBlankBoard()

    def getBoardBoundaries(self):
        """
        Get the board's inclusive boundaries
        :return: {quadruple} (min x, max_x, min_y,max_y)
        """
        return (self.min_col, self.board_max_x_boundary, self.min_row, self.board_max_y_boundary)

    def populate_board_with_agents(self, agentIndex: int, agent: AgentInterface):
        """
        Add numbers that represent agents on board. Does not check
        if agents are beyond board or if agents clash. This is done by gameState class.
        :param agentIndex: {int} index value of agent
        :return: {None}
        """
        if agentIndex == 0:
            raise ValueError("0 represents empty space, agentIndex passed cannot be 0, must be 1 for player for ex.")

        agent_row_min, agent_row_max = agent.get_row_boundaries()
        agent_col_min, agent_col_max = agent.get_col_boundaries()

        for eachRowIndex in range(len(self.board_array)):
            if eachRowIndex >= agent_row_min and eachRowIndex <= agent_row_max:
                for eachColIndex in range(len(self.board_array[eachRowIndex])):
                    if eachColIndex >= agent_col_min and eachColIndex <= agent_col_max:
                        if agent.isPlayer() == True:
                            self.board_array[eachRowIndex][eachColIndex] = 1
                        if agent.isPlayer() == False:
                            if agentIndex == 1:  # 1 should be reserved for player
                                self.board_array[eachRowIndex][eachColIndex] = 2  # force value to be 2
                            else:
                                self.board_array[eachRowIndex][eachColIndex] = agentIndex

    def populate_board_with_projectiles(self, bullet: ProjectileInterface):
        bullet_row_min, bullet_row_max = bullet.get_row_boundaries()
        bullet_col_min, bullet_col_max = bullet.get_col_boundaries()

        for eachRowIndex in range(len(self.board_array)):
            if eachRowIndex >= bullet_row_min and eachRowIndex <= bullet_row_max:
                for eachColIndex in range(len(self.board_array[eachRowIndex])):
                    if eachColIndex >= bullet_col_min and eachColIndex <= bullet_col_max:
                        if bullet.isPlayerBullet() == True:
                            self.board_array[eachRowIndex][eachColIndex] = "X"
                        if bullet.isPlayerBullet() == False:
                            self.board_array[eachRowIndex][eachColIndex] = "B"  # force value to be 2

    def setUpBlankBoard(self) -> None:
        '''
        Creates a board represented as a 2D array where all
        values inside each inner list is 0 and sets the .baoard_array
        attribute to it
        :return: {list[list[int]]} A 2D array of list
        '''

        board_2d_array: list = []

        for i in range(0, self.board_height):
            any_row = []
            for j in range(0, self.board_length):
                any_row.append(0)
            board_2d_array.append(any_row)

        self.board_array = board_2d_array

    def __str__(self):
        '''
        Converts the 2D array board representation
        into a string
        :return: {str} string representation of the board
        '''

        list_row_str = []
        board_str = ""

        for row in range(len(self.board_array)):  # amount of rows, or y values
            temp = "|"
            temp += "\u0332" + " "
            current_row_list = self.board_array[row]
            for col in range(len(current_row_list)):  # amount of col or x's
                string_add = None
                if type(current_row_list[col]) == int:
                    string_add = str(current_row_list[col])
                else:
                    string_add = current_row_list[col]
                temp += "\u0332" + (string_add)
                temp += "\u0332" + " "
                temp += "|"
                if col < len(current_row_list) - 1:
                    temp += "\u0332" + " "
                else:
                    list_row_str.append(temp)

        row_counter = self.board_height - 1

        for i in range(-1, -len(list_row_str) - 1, -1):
            # grab backwards so string rep axis makes sense
            board_str += str(row_counter) + " " + list_row_str[i] + "\n"
            row_counter -= 1

        # add col axis values
        x_axis_add_on = "  "
        for j in range(self.board_length):
            x_axis_add_on += "  " + str(j) + " "

        board_str += x_axis_add_on

        return board_str.encode('utf-8').decode("ascii", "ignore")

    def get_board_with_proj_RL(self, gameState, player: bool):
        myBoard = self.setUpBlankBoardRL()
        my_bullets_filtered = filter(lambda x: x.isPlayerBullet() == player, gameState.current_projectiles)

        for bullet in my_bullets_filtered:
            bullet_row_min, bullet_row_max = bullet.get_row_boundaries()
            bullet_col_min, bullet_col_max = bullet.get_col_boundaries()

            for eachRowIndex in range(len(myBoard)):
                if bullet_row_min <= eachRowIndex <= bullet_row_max:
                    for eachColIndex in range(len(myBoard[eachRowIndex])):
                        if bullet_col_min <= eachColIndex <= bullet_col_max:
                            myBoard[eachRowIndex][eachColIndex] = 1

        return myBoard

    def get_board_with_agents_RL(self, game_state, min_type: int, max_type:int):

        myBoard = self.setUpBlankBoardRL()
        my_agents_filtered = filter(lambda x: min_type <= x.getAgentType() <= max_type, game_state.current_agents)

        for agent in my_agents_filtered:
            agent_row_min, agent_row_max = agent.get_row_boundaries()
            agent_col_min, agent_col_max = agent.get_col_boundaries()

            for eachRowIndex in range(len(myBoard)):
                if agent_row_min <= eachRowIndex <= agent_row_max:
                    for eachColIndex in range(len(myBoard[eachRowIndex])):
                        if agent_col_min <= eachColIndex <= agent_col_max:
                            myBoard[eachRowIndex][eachColIndex] = 1

        return myBoard

    def get_board_with_agents_overlaps_RL(self, game_state, min_type: int, max_type:int):

        myBoard = self.setUpBlankBoardRL()
        myBoard2 = self.setUpBlankBoardRL()
        if(max_type == 6) :
            print("6 board")
            print(len(myBoard2))
        my_agents_filtered = filter(lambda x: min_type <= x.getAgentType() <= max_type, game_state.current_agents)

        for agent in my_agents_filtered:
            agent_row_min, agent_row_max = agent.get_row_boundaries()
            agent_col_min, agent_col_max = agent.get_col_boundaries()

            for eachRowIndex in range(len(myBoard)):
                if agent_row_min <= eachRowIndex <= agent_row_max:
                    for eachColIndex in range(len(myBoard[eachRowIndex])):
                        if agent_col_min <= eachColIndex <= agent_col_max:
                            if(myBoard[eachRowIndex][eachColIndex]) > 0:
                                myBoard2[eachRowIndex][eachColIndex] = 1
                            else:
                                myBoard[eachRowIndex][eachColIndex] = myBoard[eachRowIndex][eachColIndex] + 1

        if (max_type == 6):
            print("6 board 2")
            print(len(myBoard2))
            print("end")

        return myBoard2


    def setUpBlankBoardRL(self):
        '''
        Creates a board represented as a 2D array where all
        values inside each inner list is 0 and sets the .baoard_array
        attribute to it
        :return: {list[list[int]]} A 2D array of list
        '''

        board_2d_array: list = []

        for i in range(0, self.board_height):
            any_row = []
            for j in range(0, self.board_length):
                any_row.append(0)
            board_2d_array.append(any_row)

        return board_2d_array
