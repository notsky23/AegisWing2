import random

from Model.Agents.AgentInterface import AgentInterface

#TODO write tests
from Model.Agents.BasicCounterAgent import BasicCounterAgent
from Model.GameBoard import GameBoard


class EnemyPicker():
    #TODO test
    def __init__(self, gameboard: GameBoard, spawn_rate: int):
        """
        Constructor for the EnemySpawnBehaviorSuperClass
        """
        #form associative array
        self.enemy_spawn_list = [] #list of AgentInterface Type objects
        self.enemy_weights = [] # list of ints of weights being chosen
        self.initialized = False
        self.board_min_col, self.board_max_col, \
        self.board_min_row, self.board_max_row = gameboard.getBoardBoundaries()

        #logic of actual spawning must be in game loop
        if spawn_rate < 0:
            raise ValueError("Spawn rate cannot be less than 0 (0%), must be 0 >= spawn_rate <= 100 ")
        if spawn_rate > 100:
            raise ValueError("Spawn rate cannot be greater than 100 (100%), must be  0 >= spawn_rate <= 100  ")

        self.spawn_rate = spawn_rate

    #TODO test
    def add_enemy_to_spawn_list(self, enemy: AgentInterface, weight: int):
        """
        Adds an enemy to the spawn list with a weight. The higher
        the weight, the more likely the enemy will be chosen by choose enemy method.
        Throw an error if enemy passed is a player agent
        :param enemy: {AgentInterface}
        :param weight: {int} influences probability of being chosen, cannot be negative or 0
        :return:
        """
        if self.initialized == True:
            raise RuntimeError("Cannot add new enemies after spawner has been initialized")
        if enemy.isPlayer() == True:
            raise ValueError("Cannot add player to enemy list")

        if weight < 0:
            raise ValueError("An enemy agent cannot have a weight < 0 ")

        self.enemy_spawn_list.append(enemy)
        self.enemy_weights.append(weight)

    # TODO test
    def initialize_spawn_behavior(self):
        """
        Performs proper checks to make sure choose enemy will not
        cause an error.
        :return: None
        """
        # check probabilities len matches spawn list len because they are
        #supposed to be associative array
        if (len(self.enemy_spawn_list) == 0):
            print("Warning no agents added to enemy spawn list")

        if len(self.enemy_spawn_list) != len(self.enemy_weights):
            raise RuntimeError("ERROR: enemy spawn list and probability mismatch\nPlease check len of spawn list and len weights are the same")

        self.initialized = True

    # TODO test
    def choose_enemy(self):
        """
        Chooses an enemy from list of enemies.
        The higher the weight of an enemy, the more likely
        they will be chosen.
        :return: {AgentInterface} enemy chosen
        """
        if self.initialized == False:
            raise RuntimeError("Spawn Behavior not initialized, please call .initialize_spawn_behavior method")

        #choose enemy by weight
        chosen_enemy: AgentInterface = (random.choices(population=self.enemy_spawn_list,
                       weights=self.enemy_weights,
                       k=1))[0]

        valid_pos = False

        while valid_pos == False:
            agent_lowest_row = random.randint(self.board_min_row, self.board_max_row)
            chosen_enemy.set_position(agent_lowest_row, self.board_max_col)
            if self.isValidEnemyPosition(chosen_enemy):
                valid_pos = True

        ##### Specific to integrating basic counter agents ####

        if type(chosen_enemy) == BasicCounterAgent:
            #randomly select row to go to
            chosen_ideal_row = random.choice(list(range(0,self.board_max_row)))

            #TODO heads up may cause issues if board lengths less than 3
            chosen_ideal_col = self.board_max_col - 3 #force position to be near right side of board

            if chosen_ideal_col <= 0:
                print(f"WARNING, BASIC COUNTER AGENT MAY NOT BE ABLE TO GO TO IDEAL POSITION row = {chosen_ideal_row}, col={chosen_ideal_col}")
                print(f"Gameboard row boundaries (inclusive) are {self.board_min_row, self.board_max_row}")
                print(f"Gameboard col boundaris (inclusive) are {self.board_min_col, self.board_max_col}")

            ce : BasicCounterAgent = BasicCounterAgent.convert_agentInterface_to_BasicCounter(chosen_enemy)
            ce.set_ideal_row(chosen_ideal_row)
            ce.set_ideal_col(chosen_ideal_col)
            chosen_enemy : AgentInterface = ce

        return chosen_enemy

    def isValidEnemyPosition(self, agent : AgentInterface):
        agent_row_min = agent.get_min_row_boundary()
        agent_row_max = agent.get_max_row_boundary()

        if (agent_row_min >= self.board_min_row) and (agent_row_max <= self.board_max_row):
            return True
        else:
            return False

