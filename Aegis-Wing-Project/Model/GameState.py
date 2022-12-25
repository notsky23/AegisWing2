from random import random

from Model.Agents.Actions import Actions
from Model.Agents.AgentInterface import AgentInterface
from Model.Agents.AgentSuperClass import AgentSuperClass
from Model.Agents.PlayerAgent import PlayerAgent
from Model.GameBoard import GameBoard
from Model.Projectiles.ProjectileInterface import ProjectileInterface
from Model.Projectiles.ProjectileSuperClass import ProjectileSuperClass
from Model.Projectiles.SimpleAgentBullet import SimpleAgentBullet


class GameState:


    '''
    This class represents any given state during the game
    It keeps track of:
        - gameBoard
        - how many turns left until game ends
        - player lives left
        - amount of enemies on screen at any one time
        - agents
    '''
    def __init__(self, board_len: int = 10, board_height: int = 10,
                 max_enemies_at_one_time: int =1,
                 turns_left: int = 100, player_lives: int = 1):
        '''
        Constuctor for the gameState
        :param board_len: {int} length of the board
        :param board_height: {int} height of the board
        :param max_enemies_at_one_time: {int} amount of enemies allows at any one turn
        :param turns_left: {int} turns until the game ends
        :param player_lives: {int} how many lives a player has
        '''
        self.turns_left = turns_left
        self.gameBoard = GameBoard(board_len, board_height)
        self.max_enemies_at_any_given_time = max_enemies_at_one_time
        self.current_player_lives = player_lives
        self.current_agents = [] #list of AgentInterface Objects
        self.current_projectiles = []
        self.isPlayerAdded = False
        self.fireActions = [Actions.FIRE, Actions.FIRERIGHT, Actions.FIRELEFT,
                            Actions.FIREDOWN, Actions.FIREUP]
        self.score = 0 #TODO test
        self.won_flag = False

        #Added late
        self.removed_agents = 0
        self.removed_types = ""

        #Added for DQN model
        self.lastHit = 0
        self.lostLife = False


    def addAgent(self, agent: AgentSuperClass) -> bool:
        '''
        Adds an agent to the list of current agents. Player agent
        MUST be first agent added. This does not care about agent
        positions to allow for agents to come into board
        from outside the boundary
        :param agent: {Agent} adds an agent to list of current agents
        :return: {bool} True if successfully added, false otherwise
        '''

        # empty agent list
        if len(self.current_agents) == 0:
            # enforce that player agent is first element, so don't add enemies first
            if agent.isPlayer == False:
                print("WARNING: Player agent must be added first, no agent added")
                return False
            else: # adding player agent as first element
                # check if player position is valid
                if self.isValidAgent(agent):
                    self.current_agents.append(agent)
                    self.isPlayerAdded = True
                    self.update_board()
                    return True
                else:
                    print(f"WARNING: Player agent is killed, No point in adding more enemies")
                    self.update_board()
                    return False

        else: # length of list > 1 i.e. player already added
            if agent.isPlayer() == True and self.isPlayerAdded == True:
                print("WARNING: Player agent already added, cannot add more player agents")
                self.update_board()
                return False
            else: # if enemy agent, check we don't add more than allowed at one state
                current_amt_enemies = len(self.current_agents) - 1
                if (current_amt_enemies < self.max_enemies_at_any_given_time):
                    # now we check that enemy doesn't spawn inside player agent
                    self.current_agents.append(agent)
                    self.update_board()
                    return True
                else:
                    print("WARNING: Cannot exceed enemy agent limit, agent not added")
                    self.update_board()
                    return False

    def getPlayerPos(self):
        if len(self.current_agents) > 0:
            playerAgent =  self.current_agents[0]
            return playerAgent.get_position()
        else:
            print("WARNING: No player agent to return position from.")
            return None

    def getPlayer(self):
        return self.current_agents[0]

    def addProjectile(self, bullet: ProjectileSuperClass, agent: AgentSuperClass) -> bool:
        '''
        Adds a projectile to the list of bulletagents. 
        :param bullet: {ProjectileSuperClass} adds a projectile to list of current projectiles
        :return: {bool} True if successfully added, false otherwise
        '''


        if agent is not None:
            playerBullet  = SimpleAgentBullet(agent)
            self.current_projectiles.append(playerBullet)
            return True
        else:
            #TODO: Create non agent projectiles.
            return False
            # this is for adding projectiles not related to agents


    def decrement_turn(self):
            self.turns_left -= 1
            if len(self.current_agents) > 0:
                #only add survival point if player is still in the game
                if self.current_agents[0].isPlayer() and self.current_agents[0].get_hp() > 0:
                    self.score += 1

    def set_turn(self, turns_left: int) -> None:
        if turns_left < 0:
            raise ValueError("turns_left cannot be less than 0")
        self.turns_left = turns_left

    def isWin(self) -> bool:

        #you win game if player still has lives and timer has reached 0
        if self.current_player_lives > 0 and self.isGameOver():
            if self.won_flag == False:
                self.score += 10000
            self.won_flag = True
            return True
        return False

    def isLose(self):
        if (self.current_player_lives <= 0):
            self.score -= 1000
            return True
        else:
            return False

    def isGameOver(self) -> bool:
        if self.turns_left <= 0:
            return True
        else:
            return False

    def checkBulletAgentClashes(self):
        for i in range(len(self.current_projectiles)):
            each_bullet: ProjectileSuperClass = self.current_projectiles[i]
            for j in range(len(self.current_agents)):
                each_agent: AgentInterface = self.current_agents[j]

                # if bullet hits the agent
                if each_bullet.get_hp() > 0 and each_bullet.didHitAgent(each_agent):
                    each_bullet.set_hp(each_bullet.get_hp() - 1)
                    each_agent.set_hp(each_agent.get_hp() - 1)

                    if each_agent.isPlayer(): #if agent that got hit was the player then reduce score
                        self.score -= 100
                        self.lostLife = True
                    else:
                        self.removed_types += "_" + str(each_agent.getAgentType())
                        self.removed_agents += 1

    def haveAllAgentsMoved(self) -> bool:
        for each in self.current_agents:
            each_agent: AgentInterface = each
            if each_agent.hasMoved() == False:
                return False

        return True


    def removeBullets(self):
        bullets_to_remove = []

        for each in self.current_projectiles:
            each_bullet: ProjectileInterface = each
            if each_bullet.get_hp() <= 0 or \
                    each_bullet.get_min_col_boundary() < self.gameBoard.min_col or \
                    each_bullet.get_max_col_boundary() > self.gameBoard.board_max_x_boundary:
                bullets_to_remove.append(each_bullet)

        for bullet in bullets_to_remove:
            #each_bullet: ProjectileInterface = bullet
            #TODO delete print
            #print("removing bullets")
            self.current_projectiles.remove(bullet)



    def checkPlayerAgentClashes(self):
        """
        Checks for if player clashes with enemy agents and adjusts
        hp of objects accordingly
        Enemies allowed to overlap with each other.
        Call in generateSuccessor
        :return: {None}
        """
        # agent crashing logic, check if player is overlapping with enemy agents
        player_agent: AgentInterface = self.current_agents[0]
        list_enemy_agents = self.current_agents[1:]

        for i in range(len(list_enemy_agents)):
            enemy_agent: AgentInterface = list_enemy_agents[i]

            # if overlapping, player and agent lose health
            #TODO maybe just have them blow up instead of subtracting health? Already happens since player hp = 1
            if (player_agent.is_overlapping_other_agent(enemy_agent)):
                player_agent.set_hp(player_agent.get_hp() - 1)
                self.lostLife = True
                #TODO Test
                self.score += player_agent.getPointValue() #returns negative so adding is subtracting
                enemy_agent.set_hp(enemy_agent.get_hp() - 1)

        #TODO test case where playern and enemy right next to each other then move past each other, this should cause a hit
    def updateAgentsList(self):
        """
        update the agents list. If player health = 0, remove them
        If enemy agent health = 0 remove them
        If enemy agent_max_col < board_col_min remove them.
        Call this in generateSuccessor
        :return: {None}
        """
        board_min_col = self.gameBoard.min_col
        agent_indexes_to_be_popped = []

        for i in range(len(self.current_agents)):
            already_popped = False
            each_agent: AgentInterface = self.current_agents[i]
            # check if agent is dead
            if each_agent.is_dead() == True:
                # add agent index to list to be popped
                agent_indexes_to_be_popped.append(i)
                already_popped = True
                if each_agent.isPlayer() == False:
                    self.score += each_agent.getPointValue() #represents destruction of enemy ship
                    self.lastHit += each_agent.getPointValue()

            if already_popped == True:
                # will go to next agent if agent is dead
                continue
            else:
                # if enemy max col beyond board min boundary,
                # don't need to check for player because state.getAllLegalActions(0) will tell you
                # this already
                if each_agent.get_max_col_boundary() < board_min_col:
                    agent_indexes_to_be_popped.append(i)

        subtract_by = 0

        # COde below handles if player dies and can or does not respawn
        for each_index in agent_indexes_to_be_popped:
            value_to_pop = each_index - subtract_by
            try:
                current_agent: AgentInterface = self.current_agents[value_to_pop]
            except IndexError:
                #print(f"Index error, list length = {len(self.current_agents)}")
                #print(f"trying to pop: {value_to_pop}")
                break
            # if player agent died
            if current_agent.isPlayer() == True: # if player agent was destroyed
                if (current_agent.is_dead()):
                    self.current_player_lives -= 1
                    self.score -= 500 # lose 1 life score decreases
                    if self.current_player_lives > 0:
                        self.isPlayerAdded = False
                        # if more lives left than player agent gets restarted at initial point
                        #player should always be first index i.e. 0
                        player: PlayerAgent = self.current_agents[0]
                        self.current_agents[0] = player.respawnPlayer()
                        continue

            if value_to_pop == 0 and self.current_player_lives <= 0:
                self.current_agents.pop(value_to_pop)
                subtract_by = 1
                #TODO Delete print
                #print("Removing Player Agent")
                self.removed_agents += 1

            elif value_to_pop == 0 and self.current_player_lives >= 1:
                continue
            else:
                value_to_pop = each_index - subtract_by
                self.current_agents.pop(value_to_pop)
                subtract_by = each_index
                #TODO Delete print
                #print("Removing Agent")
                self.removed_agents += 1


    def update_board(self):
        '''
        Updates the gameBoard attribute with positions of each agent.
        Call this method after calling
        - checkPlayerAgentClashes
        - updateAgentsList
        :return:
        '''
        #TODO update with bullet logic

        self.gameBoard.setUpBlankBoard()

        for i in range(len(self.current_agents)):
            self.gameBoard.populate_board_with_agents(i + 1, self.current_agents[i])

        for j in range(len(self.current_projectiles)):
            self.gameBoard.populate_board_with_projectiles(self.current_projectiles[j])

        #for loop for bullet list
        #if bullet is player bullet
        #   board value = -1
        #else
        #   board value = -2
        #.populateboard(board_value, bulletAgent)


    def isValidAgent(self, agent: AgentInterface) -> bool:
        """
        Helper method to getAllLegalActions and addAgent. Checks if
        the agent position is valid within the board.
        :param agent: {AgentInterface}
        :return: {bool} True if agent position is valid, false otherwise
        """

        board_min_x,board_max_x, board_min_y, board_max_y = self.gameBoard.getBoardBoundaries()
        agent_min_x, agent_max_x = agent.get_row_boundaries() # x is up or down so row bounds
        agent_min_y, agent_max_y = agent.get_col_boundaries() # y is left or right so col bounds
        isAgentPlayer = agent.isPlayer()

        # if it is a player agent
        # cannot go beyond any boundaries
        if isAgentPlayer:
            if (agent_min_x < board_min_x):
                return False
            elif (agent_max_x - 1 > board_max_x): #may potentially cause bugged behavior
                return False
            elif (agent_min_y < board_min_y):
                return False
            elif (agent_max_y > board_max_y):
                return False
            else:
                return True
        #enemies are allowed to go beyond left boundary (beyond board min col/y)
        # and come in from right boundary (beyond board max col/y)
        if isAgentPlayer == False:
            if agent_min_x < board_min_x:
                return False
            if agent_max_x - 1 > board_max_x:
                return False
            else:
                return True

    def getAllLegalActions(self, agentIndex: int) -> list:
        """
        Gets all legals actions of an agent at agentIndex
        :param agentIndex: {int} index of agent in agent list
        :return: {list} a list of legal actions an agent can perform
        """
        agentTakingAction: AgentInterface = self.current_agents[agentIndex]

        all_actions = agentTakingAction.get_all_possible_raw_actions()
        legal_actions = []

        for eachAction in all_actions:
            # if action is valid add it to legal actions list
            if self.isValidAgent(agentTakingAction.take_action(eachAction)):
                legal_actions.append(eachAction)

        return legal_actions

    #TODO write test
    def deepCopy(self):
        copy = GameState()
        copy.isPlayerAdded = False
        copy.gameBoard = self.gameBoard #game board only used for rendering and boundaries, its ok to shallow copy
        copy.current_player_lives = self.current_player_lives
        copy.turns_left = self.turns_left
        copy.max_enemies_at_any_given_time = self.max_enemies_at_any_given_time
        copy.score = self.score
        copy.removed_agents = self.removed_agents
        copy.removed_types = self.removed_types
        #TODO NOTE does not copy bullet_agents, or current projectiles

        #copy agents over
        for each in self.current_agents:
            each_agent: AgentInterface = each
            copy.addAgent(each_agent.deepcopy())

        #copy bullets over
        for each_b in self.current_projectiles:
            each_bullet : ProjectileInterface = each_b
            copy.current_projectiles.append(each_bullet.deepcopy())

        return copy

    def moveAllProjectiles(self):
        copy = self.deepCopy()

        for i in range(len(copy.current_projectiles)):
            current_bullet: ProjectileInterface = copy.current_projectiles[i]
            if current_bullet.hasMoved() == False:
                bullet_action = current_bullet.autoPickAction()
                #TODO test this makes deepcopy
                bullet_after_move = current_bullet.take_action(bullet_action)
                bullet_after_move.setHasMovedStatus(True)
                #replace bullet with bullet at new position
                copy.current_projectiles[i] = bullet_after_move
            else:
                continue

        return copy

    def getStateAfterAction(self,agentIndex: int, action: Actions, moveBullets=False):
        '''
        Helper method for expectimax calculations. One individual agent will take an action,
        and changes the gamestate (i.e. firing a bullet or moving).
        Does not remove agents due to hp loss or change the score in anyway.
        This is helpful to maintain len of current_agents list.
        :param agentIndex: index of agent that will take the action
        :param action: : {Actions} the action, the agent will take
        :return: a GameState instance reflecting the change after an agent has taken an action
        '''

        if agentIndex > len(self.current_agents) - 1 or agentIndex < 0:
            raise RuntimeError(f"There are no agents with index = {agentIndex}, min=0, max={len(self.current_agents) - 1}")

        if moveBullets == True:
            successor_state = self.moveAllProjectiles()
        else:
            successor_state = self.deepCopy()

        if successor_state.current_agents[agentIndex].isExpectimaxAgent() == True:
            current_agent = successor_state.current_agents[agentIndex]
        else:
            current_agent: AgentInterface = successor_state.current_agents[agentIndex]
        all_legal_agent_actions = successor_state.getAllLegalActions(agentIndex)


        if action in all_legal_agent_actions: #is action legal?
            if action in self.fireActions:
                if current_agent.isHeuristicAgent():
                    #heuristic agent bullet speed is 2
                    newBullet = SimpleAgentBullet(current_agent, 2)
                    newBullet.setHasMovedStatus(True) # bullet will not take an action this turn
                    successor_state.current_projectiles.append(newBullet)
                    movedAgent: AgentInterface = current_agent.take_action(action)
                    successor_state.current_agents[agentIndex] = movedAgent
                elif current_agent.isExpectimaxAgent() or current_agent.isPlayer():
                    newBullet = SimpleAgentBullet(current_agent)
                    newBullet.setHasMovedStatus(True)
                    successor_state.current_projectiles.append(newBullet)
                    movedAgent: AgentInterface = successor_state.current_agents[agentIndex]
                elif current_agent.isBasicCounter() == True:
                    newBullet = SimpleAgentBullet(current_agent)
                    newBullet.setHasMovedStatus(True)
                    successor_state.current_projectiles.append(newBullet)
                    movedAgent: AgentInterface = current_agent.take_action(action)
                    successor_state.current_agents[agentIndex] = movedAgent
                else:
                    newBullet = SimpleAgentBullet(current_agent)
                    newBullet.setHasMovedStatus(True)
                    successor_state.current_projectiles.append(newBullet)
                    movedAgent: AgentInterface = successor_state.current_agents[agentIndex]
                # Agent has made a move if they fire
                movedAgent.setHasMovedStatus(True)
            else:
                #agent is just moving
                movedAgent = current_agent.take_action(action)
                movedAgent.setHasMovedStatus(True)
                successor_state.current_agents[agentIndex] = movedAgent
        else:
            successor_state.current_agents[agentIndex].setHasMovedStatus(True)
            #raise RuntimeError(f"Agent at index {agentIndex} of type {type(current_agent)} cannot take action {action}")

        successor_state.update_board()

        return successor_state

    def getStateAtNextTurn(self,playerAction: Actions):
        """
        Returns the state at the next turn i.e. after all have moved/taken action
        :param playerAction:
        :return: GameState
        """

        #move all existing bullets
        state_all_bullets_have_moved = self.moveAllProjectiles()

        playerAliveFlag = False

        if len(state_all_bullets_have_moved.current_agents) == 0: #no agents so no changes to be made
            state_all_bullets_have_moved.turns_left -= 1
            return state_all_bullets_have_moved

        if state_all_bullets_have_moved.current_agents[0].isPlayer():
            state_player_has_moved = state_all_bullets_have_moved.getStateAfterAction(0, playerAction)
            playerAliveFlag = True

        state_all_agents_have_moved = None

        # if player is alive
        if playerAliveFlag == True:

            state_ready_to_move_agents = state_player_has_moved

            #if there are existing enemy agents, we want to move just the enemies
            if len(state_player_has_moved.current_agents) > 1:
                #move each enemy
                for i in range(1,len(state_ready_to_move_agents.current_agents)):
                    each_agent : AgentSuperClass = state_ready_to_move_agents.current_agents[i]
                    agent_action = each_agent.autoPickAction(state=state_ready_to_move_agents)
                    state_ready_to_move_agents = state_ready_to_move_agents.getStateAfterAction(i,agent_action)

        else:
            #player is dead so we want to move everybody
            state_ready_to_move_agents = state_all_bullets_have_moved

            for i in range(len(state_ready_to_move_agents.current_agents)):
                each_agent: AgentSuperClass = state_ready_to_move_agents.current_agents[i]
                agent_action = each_agent.autoPickAction(state=state_ready_to_move_agents)
                state_ready_to_move_agents = state_ready_to_move_agents.getStateAfterAction(i, agent_action)

        state_all_agents_have_moved = state_ready_to_move_agents
        state_all_agents_have_moved.checkBulletAgentClashes()
        state_all_agents_have_moved.removeBullets()
        state_all_agents_have_moved.checkPlayerAgentClashes()
        state_all_agents_have_moved.updateAgentsList()
        state_all_agents_have_moved.update_board()
        state_all_agents_have_moved.reset_agents_move_status()
        state_all_agents_have_moved.decrement_turn()

        return state_all_agents_have_moved






    def generateSuccessorState(self, agentIndex: int, action: Actions):
        #check if player agent is an expetimax agent
        #if it is then choose autopick action
        #setters for iteration depth and gamestate
        #move all projectiles first before making any agent moves
        if (agentIndex == 0 and self.current_agents[agentIndex].hasMoved() == False):
            successor_state = self.moveAllProjectiles()
        else:
            successor_state = self.deepCopy()

        current_agent: AgentInterface = successor_state.current_agents[agentIndex]
        all_legal_agent_actions = successor_state.getAllLegalActions(agentIndex)

        # TODO: TEST THIS --> IF IS HEURISTIC AGENT --> IF IT SHOOTS AND MOVES THEN MOVE FIRST
        #  UPDATE AGENT AND THEN PASS UPDATED AGENT TO THE BULLET

        if current_agent.isHeuristicAgent():
            if action in all_legal_agent_actions:
                movedAgent = current_agent.take_action(action)
                successor_state.current_agents[agentIndex] = movedAgent
                if action in self.fireActions:
                    newBullet = SimpleAgentBullet(movedAgent, 2)
                    successor_state.current_projectiles.append(newBullet)
                    current_agent: AgentInterface = successor_state.current_agents[agentIndex]
                    current_agent.setHasMovedStatus(True)

        elif current_agent.isExpectimaxAgent(): #this check is not necessary
            if action in all_legal_agent_actions:
                movedAgent = current_agent.take_action(action)
                successor_state.current_agents[agentIndex] = movedAgent
                if action in self.fireActions:
                    newBullet = SimpleAgentBullet(movedAgent, 2)
                    newBullet.setHasMovedStatus(True)
                    successor_state.current_projectiles.append(newBullet)
                    current_agent: AgentInterface = successor_state.current_agents[agentIndex]
                    current_agent.setHasMovedStatus(True)

        elif action in all_legal_agent_actions:
            if action == Actions.FIRE:
                newBullet = SimpleAgentBullet(current_agent)
                newBullet.setHasMovedStatus(True)
                successor_state.current_projectiles.append(newBullet)
                current_agent: AgentInterface = successor_state.current_agents[agentIndex]
                current_agent.setHasMovedStatus(True)
            else:
                successor_state.current_agents[agentIndex] = current_agent.take_action(action)

        # if all agents have moved then check for clashes
        if successor_state.haveAllAgentsMoved() == True:
            successor_state.checkBulletAgentClashes()
            successor_state.removeBullets()

        #after action check if player has clashed with any enemy agents
        successor_state.checkPlayerAgentClashes()
        # update the list to reflect any clashes
        successor_state.updateAgentsList()
        #update the board representation
        successor_state.update_board()

        return successor_state

    #TODO write test
    def reset_agents_move_status(self):
        for each_index in range(len(self.current_agents)):
            each_agent: AgentInterface = self.current_agents[each_index]
            each_agent.resetMoveStatus()
            
        for each_index in range(len(self.current_projectiles)):
            each_bullet: ProjectileInterface = self.current_projectiles[each_index]
            each_bullet.resetMoveStatus()

        self.removed_agents = 0


    def print_board(self):
        print(self.gameBoard)

    def print_score(self):
        print("Score: ", self.score)

    def print_status(self):
        print(f"Turns Left: {self.turns_left}")
        if self.isWin():
            print("Player WON! :D")
        elif self.isLose():
            print("Player LOST! :( ")
        else:
            return

    def print_agent_locations(self):

        if len(self.current_agents) == 0:
            print("There are no Agents in the game")
        else:
            all_enemy_agents = []
            if self.current_agents[0].isPlayer():
                print(f"Player agent is at location: {self.current_agents[0].get_position()}")
                all_enemy_agents = self.current_agents[1:]
            else:
                all_enemy_agents = self.current_agents

            print(f"Total enemies on board: {len(all_enemy_agents)}")

            all_enemy_agents = self.current_agents[1:]

            for each_enemy_index in range(len(all_enemy_agents)):
                print("\t" + str(each_enemy_index + 2) + ".) " + all_enemy_agents[each_enemy_index].__str__())


    def print_projectile_locations(self):
        all_projectiles = self.current_projectiles
        all_player_projectiles = list(filter(lambda x: x.isPlayerBullet(), all_projectiles))
        all_enemy_projectiles = list(filter(lambda x: x.isPlayerBullet() == False, all_projectiles))

        if len(all_player_projectiles) > 0:
            print(f"Total Player Projectiles on board: {len(all_player_projectiles)}")
            for i in range(len(all_player_projectiles)):
                print(f"\t{i}.) {all_player_projectiles[i]}")

        if len(all_enemy_projectiles) > 0:
            print(f"Total Enemy Projectiles on board: {len(all_enemy_projectiles)}")
            for j in range(len(all_enemy_projectiles)):
                if all_enemy_projectiles[j].get_position()[1] >= 0:
                    print(f"\t{j}.) {all_enemy_projectiles[j]}")
