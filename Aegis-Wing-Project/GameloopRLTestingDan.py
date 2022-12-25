import random

import Model.Agents.AgentInterface
from Model.Agents.Actions import Actions
from Model.Agents.AgentInterface import AgentInterface
from Model.Agents.BasicCounterAgent import BasicCounterAgent
from Model.Agents.EnemyAgentBasicFireAndMove import EnemyAgentBasicFireAndMove
from Model.Agents.EnemyMoveFireHeuristicAgent import EnemyMoveFireHeuristicAgent
from Model.Agents.PlayerAgent import PlayerAgent
from Model.Agents.SimpleGoLeftAgent import SimpleGoLeftAgent
from Model.EnemyPicker import EnemyPicker
from Model.GameBoard import GameBoard
from Model.GameState import GameState

"""
This game loop will be used to train a reinforcement model
"""

########## Basic Game Configuration ##########
BOARD_ROWS = 8
BOARD_COLUMNS = 7
MAX_ENEMIES_AT_ANY_TIME = 5
GENERAL_SPAWN_RATE = 50  # represents 50% general spawn rate
TURNS_UNTIL_GAME_FINISHED = 300
PLAYER_INITIAL_SPAWN_ROW_POSITION = BOARD_ROWS // 2  # spawn in middle of board rows
PLAYER_INITIAL_SPAWN_COL_POSITION = 0  # spawn player at furthest left position
PLAYER_LIVES = 1
PLAYER_HP = 3

########## Specific Enemy Spawn Rate Configuration ##########
# if enemy does get spawned then this is the probability they get chosen
HEURISTIC_SR = 15
TURN_SPAN_SR = 20  # a.k.a counter agent
BASIC_FIRE_AND_MOVE_SR = 20
SIMPLE_GO_LEFT_SR = 45

########## Counter 'type' Enemy Configuration ##########
TURNS_UNTIL_LEAVE_BOARD = 5

########## Enemy Spawner Configuration and set up ##########
# lowest row and least col don't matter because enemy spawner will change it
HEURISTIC_AGENT = EnemyMoveFireHeuristicAgent(0, 0,count=TURNS_UNTIL_LEAVE_BOARD)
TURN_SPAN_AGENT = BasicCounterAgent(0,0,TURNS_UNTIL_LEAVE_BOARD,0,0)
BASIC_FIRE_AND_MOVE_AGENT = EnemyAgentBasicFireAndMove(0,0)
SIMPLE_GO_LEFT_AGENT = SimpleGoLeftAgent(0,0)

# ENEMY_POOL and ENEMY_SPAWN_RATES are Associative arrays, please do NOT modify these lists
ENEMY_POOL = [HEURISTIC_AGENT, TURN_SPAN_AGENT, BASIC_FIRE_AND_MOVE_AGENT, SIMPLE_GO_LEFT_AGENT]
ENEMY_SPAWN_RATES = [HEURISTIC_SR, TURN_SPAN_SR, BASIC_FIRE_AND_MOVE_SR, SIMPLE_GO_LEFT_SR]

GAMEBOARD_INFO = GameBoard(board_length=BOARD_COLUMNS, board_height=BOARD_ROWS)
ENEMY_SPAWNER = EnemyPicker(GAMEBOARD_INFO, GENERAL_SPAWN_RATE)

for i in range(len(ENEMY_POOL)):
    ENEMY_SPAWNER.add_enemy_to_spawn_list(ENEMY_POOL[i],ENEMY_SPAWN_RATES[i])

ENEMY_SPAWNER.initialize_spawn_behavior()

def print_enemies_status(gameState: GameState ):
    all_enemy_agents = gameState.current_agents[1:]

    if len(all_enemy_agents) > 0:


        print(f"Total enemies on board: {len(all_enemy_agents)}")

        for each_enemy_index in range(len(all_enemy_agents)):
            print("\t" + str(each_enemy_index + 2) + ".) " + all_enemy_agents[each_enemy_index].__str__())

def print_player_status(gameState: GameState ):
    all_enemy_agents = gameState.current_agents[1]

    print(f"Player on board: {len(all_enemy_agents)}")
    if len(all_enemy_agents) > 0:

        print("\t" + str(all_enemy_agents + 2) + ".) " + all_enemy_agents.__str__())


def print_score(gameState: GameState):
    score = gameState.score

    print(f"Current Score: {score}")


def print_board(gameState: GameState):
    print(gameState.gameBoard)
    print(f"Turns left: {gameState.turns_left}")

def print_score_and_status(gameState: GameState):
    if gameState.isWin():
        print("Player WON! :D")
    elif gameState.isLose():
        print("Player LOST! :( ")
    print(f"Score: {gameState.score}")

def print_projectile_locations(gameState: GameState):
    all_projectiles = gameState.current_projectiles
    all_player_projectiles = list(filter(lambda x: x.isPlayerBullet(), all_projectiles))
    all_enemy_projectiles = list(filter(lambda x: x.isPlayerBullet() == False, all_projectiles))

    if len(all_player_projectiles) > 0:
        print(f"Total Player Projectiles on board: {len(all_player_projectiles)}")
        for i in range(len(all_player_projectiles)):
            if all_player_projectiles[i].get_position()[1] < BOARD_COLUMNS:
                print(f"\t{i}.) {all_player_projectiles[i]}")

    if len(all_enemy_projectiles) > 0:
        print(f"Total Enemy Projectiles on board: {len(all_enemy_projectiles)}")
        for j in range(len(all_enemy_projectiles)):
            if all_enemy_projectiles[j].get_position()[1] >= 0:
                print(f"\t{j}.) {all_enemy_projectiles[j]}")


def get_state(game: GameState):
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
    print("PLAYER")
    print(len(player_list_arr))

    state = []
    for eachRowIndex in range(len(player_list_arr)):
        for eachColIndex in range(len(player_list_arr[eachRowIndex])):
            #print(max(player_list_arr[eachRowIndex]))
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

def main():

    #set to false to turn off print statements
    visualize_game = True
    # set to true to look at agent and bullet matrices
    visualize_heuristics = False

    starting_gamestate = GameState(board_len=BOARD_COLUMNS, board_height=BOARD_ROWS,
                                   max_enemies_at_one_time=MAX_ENEMIES_AT_ANY_TIME,
                                   turns_left=TURNS_UNTIL_GAME_FINISHED,
                                   player_lives=PLAYER_LIVES)

    # player will be of size 1 X 1
    player_agent = PlayerAgent(1, 1, PLAYER_INITIAL_SPAWN_ROW_POSITION,
                               PLAYER_INITIAL_SPAWN_COL_POSITION)

    player_agent.set_hp(PLAYER_HP)


    did_add_agent = starting_gamestate.addAgent(player_agent)

    new_agent = SimpleGoLeftAgent(7, 6)
    starting_gamestate.addAgent(new_agent)


    if (did_add_agent == False):
        raise RuntimeError("Could not add player agent")

    current_state = starting_gamestate

    end_line = "=" * 50

    if visualize_game:
        print("Staring GameState")
        print_board(current_state)
        print_score_and_status(current_state)
        print(end_line,"\n")
        state_arr = get_state(current_state)
        print(len(state_arr))
        print(str(state_arr))
        print(max(state_arr))
        print(end_line, "\n")
        res_list = [i for i in range(len(state_arr)) if state_arr[i] == 1]
        print(str(res_list))
        print(end_line, "\n")

    if visualize_heuristics:
        myBoard = current_state.gameBoard.get_board_with_agents_RL(current_state,2,5)
        myBoard2 = current_state.gameBoard.get_board_with_proj_RL(current_state, True)

        for row in range(len(myBoard) - 1, -1, -1):
            print(myBoard[row])

        print(end_line, "\n")

        for row in range(len(myBoard2) - 1, -1, -1):
            print(myBoard2[row])
        print(end_line,"\n")

        myBoard3 = current_state.gameBoard.get_board_with_proj_RL(current_state, False)


        for row in range(len(myBoard3) - 1, -1, -1):
            print(myBoard3[row])

        print(end_line, "\n")
        myBoard4 = current_state.gameBoard.get_board_with_agents_overlaps_RL(current_state, 2, 6)
        print(len(myBoard4))
        for row in range(len(myBoard4) - 1, -1, -1):
            print(myBoard4[row])

        print(end_line, "\n")




    # game loop
    while current_state.isWin() is False and current_state.isLose() is False:
        #have each agent take an action
        for each_index in range(0,len(current_state.current_agents)):
            # print(f"Highest valid index is {len(current_state.current_agents)-1}")
            # print(f"Current index is {each_index}")
            # print(f"updating index -> {each_index} - {current_state.removed_agents} = {each_index - current_state.removed_agents}")
            each_index = each_index - current_state.removed_agents
            #print(f"updated index is {each_index}")

            try:
                each_agent : AgentInterface = current_state.current_agents[each_index]
            except IndexError:
                #print("BREAKING FOR LOOP")
                break

            # if each_agent.hasMoved():
            #     if each_index + 1 > len(current_state.current_agents) - 1:
            #         break
            #     else:
            #         continue # move on to next agent

            if each_agent.isPlayer():
                # TODO DAN YOU WILL HAVE TO MAKE YOUR OWN PLAYER AGENT CLASS and overwrite auto pick action
                DEFAULT_ACTION = Actions.FIRE
                agent_action = DEFAULT_ACTION

            elif each_agent.isHeuristicAgent():
                agent_action = each_agent.autoPickAction(current_state)
            else:
                agent_action = each_agent.autoPickAction()

            try:
                current_state = current_state.generateSuccessorState(each_index, agent_action)
            except IndexError:
                break


        #once all agents have taken an action decrement the turn
        current_state.decrement_turn()
        # Reset move status of agents after everyone has moved
        current_state.reset_agents_move_status()

        #print(end_line)

        # spawn enemies at the start of new turn
        if len(current_state.current_agents) - 1 < current_state.max_enemies_at_any_given_time:
            # spawn enemy based on spawn rate
            probability_to_spawn = random.randint(0, 100)
            if probability_to_spawn <= ENEMY_SPAWNER.spawn_rate:
                # pick an enemy
                enemy_to_spawn = ENEMY_SPAWNER.choose_enemy()
                current_state.addAgent(enemy_to_spawn)

        #Optional board visualization
        if visualize_game:
            print_projectile_locations(current_state)
            print_enemies_status(current_state)
            print_board(current_state)
            print(end_line, "\n")
            state_arr = get_state(current_state)
            print(len(state_arr))
            print(str(state_arr))
            print(max(state_arr))
            print(end_line, "\n")
            res_list = [i for i in range(len(state_arr)) if state_arr[i] == 1]
            print(str(res_list))
            print(end_line, "\n")

        if visualize_heuristics:
            myBoard = current_state.gameBoard.get_board_with_agents_RL(current_state, 2,5)
            myBoard2 = current_state.gameBoard.get_board_with_proj_RL(current_state, True)

            for row in range(len(myBoard) - 1, -1, -1):
                print(myBoard[row])

            print(end_line, "\n")
            for row in range(len(myBoard2) - 1, -1, -1):
                print(myBoard2[row])
            print(end_line, "\n")

            myBoard3 = current_state.gameBoard.get_board_with_proj_RL(current_state, False)

            myBoard4 = current_state.gameBoard.get_board_with_agents_overlaps_RL(current_state, 2, 6),

            for row in range(len(myBoard3) - 1, -1, -1):
                print(myBoard3[row])

            for row in range(len(myBoard4) - 1, -1, -1):
                print(myBoard4[row])

            print(end_line, "\n")



if __name__ == "__main__":
    main()

