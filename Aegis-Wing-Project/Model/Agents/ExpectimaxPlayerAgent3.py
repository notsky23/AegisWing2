import random

from Model.Agents.Actions import Actions
from Model.Agents.AgentSuperClass import AgentSuperClass
from Model.Agents.PlayerAgent import PlayerAgent
#TODO delete import below
from Model.GameState import GameState

#global DEBUG_TEST_COUNTER
#DEBUG_TEST_COUNTER = 0

class ExpectimaxPlayerAgent3(PlayerAgent):
    def __init__(self, agent_length: int = 1, agent_height: int = 1, lowest_row: int = 0, least_col: int = 0, expectimax_depth: int =0):
        super().__init__(agent_length, agent_height, lowest_row, least_col)
        self.isInvulnerable = False
        self.turnsUntilInvulnerabilityOver = 0
        self.spawn_x = least_col
        self.spawn_y = lowest_row
        self.id = "1"
        self.expectimaxDepth = expectimax_depth

    def isExpectimaxAgent(self) -> bool:
        return True

    def deepcopy(self):
        copy = ExpectimaxPlayerAgent3(self.agent_length, self.agent_height, self.lowest_row, self.least_col,self.expectimaxDepth)
        copy.hasAlreadyMoved = self.hasAlreadyMoved
        copy.hp = self.get_hp()
        return copy

      #TODO test this method if necessary, use when player dies and has another life left
    def respawnPlayer(self):
        #TODO would be an issue if game has more than 1 player life beacuse health not copied over
        respawned = ExpectimaxPlayerAgent3(self.agent_length,self.agent_height,self.spawn_y, self.spawn_x)
        return respawned

    def autoPickAction(self, state: GameState =None) -> Actions:
        if state == None:
            raise RuntimeError("Expectimax agent autopick action requires state")

        #Expectimax Algorithm
        best_action = None
        best_score = float('-inf')
        all_potential_actions = state.getAllLegalActions(0)

        #stores states which have the same score
        tied_states = []

        for i in range(len(all_potential_actions)):
            each_action = all_potential_actions[i]
            #all potential next states, these can be thought of as the chance nodes
            next_state = state.getStateAfterAction(0,each_action,moveBullets=True)

            #TODO delete
            # if each_action == Actions.FIRE:
            #     x = 5

            #score only matters if player is still alive
            if len(next_state.current_agents) > 1 and next_state.current_agents[0].isPlayer() == True:
                state_score = self.expectimax(1,0,next_state)
            else:
                state_score = next_state.score

            #TODO delete
            # print(each_action, state_score)

            if state_score > best_score:
                best_score = state_score
                best_action = each_action
            elif state_score == best_score:
                tied_states.append((each_action, state_score))
                if (best_action,best_score) not in tied_states:
                    tied_states.append((best_action, best_score))


        if len(tied_states) > 1:
            # choice will return a tuple where first elem is the action
            best_action = random.choice(tied_states)[0]


        #TODO DELETE
        #print("==========END OF PLAYER TURN==============")
        #print(f"tied states at turn={state.turns_left}\n{tied_states}")

        return best_action

    def expectimax(self, agentIndex: int, depth: int, state: GameState):
        #terminal condition(s)
        """
        1.) Beyond max depth
        2.) No agents on the board (implies player lost)
        3.) Enemy agent is index = 0 (implies player lost)
        so just return the score instead of exploring any further
        """
        if depth >= self.expectimaxDepth or len(state.current_agents) == 0 or state.current_agents[0].isPlayer() == False:
            return state.score


        #if maximizer node, i.e. start of a new depth
        if agentIndex == 0 and state.current_agents[0].isPlayer() == True:
            #get max score among all actions
            best_score = float('-inf')
            all_potential_actions = state.getAllLegalActions(0)

            for each_action in all_potential_actions:
                nextState = state.getStateAfterAction(agentIndex,each_action,True)
                next_score = None

                #if game is over given this action taken return just the score
                if nextState.isLose() == True or nextState.current_agents[0].isPlayer == False \
                        or len(nextState.current_agents) == 0:
                    next_score = nextState.score
                else:
                    #player is the only agent, going to next depth
                    if len(nextState.current_agents) == 1:
                        next_score = self.expectimax(0, depth + 1, nextState)
                    else:
                        next_score = self.expectimax(agentIndex + 1, depth,nextState)

                if next_score > best_score:
                    best_score = next_score

            return best_score

        #minimizer node
        else:
            # want average of all actions
            average_score = 0
            all_potential_actions = state.getAllLegalActions(agentIndex)

            probability_choose = 1 / len(all_potential_actions)

            for each_action in all_potential_actions:
                nextState = state.getStateAfterAction(agentIndex,each_action)

                #if game is over given this action taken add up just the score
                if nextState.isLose() == True or nextState.current_agents[0].isPlayer == False \
                        or len(nextState.current_agents) == 0:
                    average_score += nextState.score * probability_choose
                else:
                    # means continue down the tree at the same depth
                    nextIndex = None
                    # this means we should transition to next depth since all enemy agents have moved
                    if agentIndex + 1 > len(nextState.current_agents) - 1:
                        nextIndex = 0
                        nextDepth = depth + 1
                        nextState.checkBulletAgentClashes()
                        nextState.removeBullets()
                        nextState.checkPlayerAgentClashes()
                        nextState.updateAgentsList()
                        nextState.update_board()
                        nextState.reset_agents_move_status()
                        nextState.decrement_turn()
                    else:
                        nextIndex = agentIndex + 1
                        nextDepth = depth

                    average_score += (self.expectimax(nextIndex, nextDepth, nextState )) * probability_choose

            return average_score

