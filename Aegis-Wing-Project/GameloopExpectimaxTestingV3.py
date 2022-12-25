import csv
import random
from datetime import datetime

from Model.Agents.Actions import Actions
from Model.Agents.AgentInterface import AgentInterface
from Model.Agents.BasicCounterAgent import BasicCounterAgent
from Model.Agents.EnemyAgentBasicFireAndMove import EnemyAgentBasicFireAndMove
from Model.Agents.EnemyMoveFireHeuristicAgent import EnemyMoveFireHeuristicAgent
from Model.Agents.ExpectimaxPlayerAgent3 import ExpectimaxPlayerAgent3
from Model.Agents.PlayerAgent import PlayerAgent
from Model.Agents.SimpleGoLeftAgent import SimpleGoLeftAgent
from Model.EnemyPicker import EnemyPicker
from Model.GameBoard import GameBoard
from Model.GameState import GameState

"""
This game loop will be used to train a reinforcement model
"""
BOARD_ROWS = 8
BOARD_COLUMNS = 7
MAX_ENEMIES_AT_ANY_TIME = 4
GENERAL_SPAWN_RATE = 50  # represents 50% general spawn rate
TURNS_UNTIL_GAME_FINISHED = 300
PLAYER_INITIAL_SPAWN_ROW_POSITION = BOARD_ROWS // 2  # spawn in middle of board rows
PLAYER_INITIAL_SPAWN_COL_POSITION = 0  # spawn player at furthest left position
PLAYER_LIVES = 1
PLAYER_HP = 3
EXPECTIMAX_DEPTH = 1
TOTAL_GAME_RUNS = 50

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
            print(f"\t{i}.) {all_player_projectiles[i]}")

    if len(all_enemy_projectiles) > 0:
        print(f"Total Enemy Projectiles on board: {len(all_enemy_projectiles)}")
        for j in range(len(all_enemy_projectiles)):
            print(f"\t{j}.) {all_enemy_projectiles[j]}")



def main():

    #set to false to turn off print statements
    visualize_game = False

    field_titles = ["Game#", "Enemies_Killed", "HP_Lost", "End_Status", "Turns_Survived", "Score",
                    "Time at End of Simulation"]

    list_values = []
    game_counter = 1

    for i in range(TOTAL_GAME_RUNS):

        starting_gamestate = GameState(board_len=BOARD_COLUMNS, board_height=BOARD_ROWS,
                                       max_enemies_at_one_time=MAX_ENEMIES_AT_ANY_TIME,
                                       turns_left=TURNS_UNTIL_GAME_FINISHED,
                                       player_lives=PLAYER_LIVES)

        # player will be of size 1 X 1
        expectimax_agent = ExpectimaxPlayerAgent3(1, 1, PLAYER_INITIAL_SPAWN_ROW_POSITION,
                                   PLAYER_INITIAL_SPAWN_COL_POSITION,expectimax_depth=EXPECTIMAX_DEPTH)
        expectimax_agent.set_hp(PLAYER_HP)

        did_add_agent = starting_gamestate.addAgent(expectimax_agent)

        if (did_add_agent == False):
            raise RuntimeError("Could not add player agent")

        current_state = starting_gamestate

        end_line = "=" * 50

        if visualize_game:
            print("Staring GameState")
            print_board(current_state)
            print_score_and_status(current_state)
            print(end_line,"\n")


        print(f"Starting Simulation for Game {game_counter} at {datetime.today().strftime('%H:%M %p')} with depth = {EXPECTIMAX_DEPTH}")
        # game loop
        while current_state.isWin() == False and current_state.isLose() == False:
            #print(f"Starting turn {current_state.turns_left},\t#agents = {len(current_state.current_agents)},\t#Bullets = {len(current_state.current_projectiles)} at {datetime.today().strftime('%H:%M %p')}")
            agent: ExpectimaxPlayerAgent3 = current_state.current_agents[0]
            expectimaxAgentAction = agent.autoPickAction(current_state)
            current_state = current_state.getStateAtNextTurn(expectimaxAgentAction)

            # spawn enemies at the start of new turn
            if len(current_state.current_agents) - 1 < current_state.max_enemies_at_any_given_time:
                # spawn enemy based on spawn rate
                probability_to_spawn = random.randint(0, 100)
                if probability_to_spawn <= ENEMY_SPAWNER.spawn_rate:
                    # pick an enemy
                    enemy_to_spawn = ENEMY_SPAWNER.choose_enemy()
                    current_state.addAgent(enemy_to_spawn)

            if current_state.turns_left % 50 == 0:
                print(f"Completed up to {300 - current_state.turns_left} turns of Game: {game_counter} at {datetime.today().strftime('%H:%M %p')}")

            #Optional board visualization
            if visualize_game:
                print_projectile_locations(current_state)
                print_enemies_status(current_state)
                print_board(current_state)
                if current_state.current_agents[0].isPlayer():
                    print(f"PLAYER HP: {current_state.current_agents[0].get_hp()}")
                else:
                    print("PLAYER HP: 0")
                print_score_and_status(current_state)
                print(end_line)

        if current_state.isLose() == True:
            lost_hp = 3
            endStatus = "Lose"
        else:
            lost_hp = 3 - current_state.current_agents[0].get_hp()
            endStatus = "Win"
        turns_survived = 300 - current_state.turns_left
        entry = [game_counter, current_state.removed_agents, lost_hp, endStatus, turns_survived, current_state.score,datetime.today().strftime('%H:%M %p')]
        list_values.append(entry)

        print(f"Game# {game_counter} Completed at {datetime.today().strftime('%H:%M %p')}")

        game_counter += 1

    with open('expectimaxStats-D3-SGL.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(field_titles)

        # write multiple rows
        writer.writerows(list_values)

    print("File complete")


if __name__ == "__main__":
    main()

