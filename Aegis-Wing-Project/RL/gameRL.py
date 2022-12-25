import argparse
import csv
# from bayesOpt import *
import datetime
# Imports for game loop
import random
import statistics
import sys
from datetime import datetime
from random import randint

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import torch
import torch.optim as optim

from DQN import DQNAgent
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

# Constant for training

DEVICE = 'cpu'  # 'cuda' if torch.cuda.is_available() else 'cpu'
LOGGING = True
# Constants for our Game Loop
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
DEFAULT_PLAYER_ACTION = Actions.FIRE

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
HEURISTIC_AGENT = EnemyMoveFireHeuristicAgent(0, 0, count=TURNS_UNTIL_LEAVE_BOARD)
TURN_SPAN_AGENT = BasicCounterAgent(0, 0, TURNS_UNTIL_LEAVE_BOARD, 0, 0)
BASIC_FIRE_AND_MOVE_AGENT = EnemyAgentBasicFireAndMove(0, 0)
SIMPLE_GO_LEFT_AGENT = SimpleGoLeftAgent(0, 0)

# ENEMY_POOL and ENEMY_SPAWN_RATES are Associative arrays, please do NOT modify these lists
ENEMY_POOL = [HEURISTIC_AGENT, TURN_SPAN_AGENT, BASIC_FIRE_AND_MOVE_AGENT, SIMPLE_GO_LEFT_AGENT]
ENEMY_SPAWN_RATES = [HEURISTIC_SR, TURN_SPAN_SR, BASIC_FIRE_AND_MOVE_SR, SIMPLE_GO_LEFT_SR]

GAMEBOARD_INFO = GameBoard(board_length=BOARD_COLUMNS, board_height=BOARD_ROWS)
ENEMY_SPAWNER = EnemyPicker(GAMEBOARD_INFO, GENERAL_SPAWN_RATE)

for i in range(len(ENEMY_POOL)):
    ENEMY_SPAWNER.add_enemy_to_spawn_list(ENEMY_POOL[i], ENEMY_SPAWN_RATES[i])

ENEMY_SPAWNER.initialize_spawn_behavior()

# The first action our PLAYER will take as default for training
FIRST_ACTION = Actions.FIRE


####################################
#  HELPER FUNCTIONS FOR GAME LOOP  #
####################################

def print_player_status(gameState: GameState):

    if len(gameState.current_agents) > 0 and gameState.current_agents[0].isPlayer():
        player_agent = gameState.current_agents[0]

        print("\n" + "PLAYER AGENT:" + player_agent.__str__())


def print_score(gameState: GameState):
    score = gameState.score

    print(f"Current Score: {score}")

def print_enemies_status(gameState: GameState):
    all_enemy_agents = gameState.current_agents[1:]

    if len(gameState.current_agents) > 2 and len(all_enemy_agents) > 0:

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
            if all_player_projectiles[i].get_position()[1] < BOARD_COLUMNS:
                print(f"\t{i}.) {all_player_projectiles[i]}")

    if len(all_enemy_projectiles) > 0:
        print(f"Total Enemy Projectiles on board: {len(all_enemy_projectiles)}")
        for j in range(len(all_enemy_projectiles)):
            if all_enemy_projectiles[j].get_position()[1] >= 0:
                print(f"\t{j}.) {all_enemy_projectiles[j]}")





def plot_seaborn(array_counter, array_score, train):
    sns.set(color_codes=True, font_scale=1.5)
    sns.set_style("white")
    plt.figure(figsize=(13, 8))
    fit_reg = False if train == False else True
    ax = sns.regplot(
        np.array([array_counter])[0],
        np.array([array_score])[0],
        # color="#36688D",
        x_jitter=.1,
        scatter_kws={"color": "#36688D"},
        label='Data',
        fit_reg=fit_reg,
        line_kws={"color": "#F49F05"}
    )
    # Plot the average line
    y_mean = [np.mean(array_score)] * len(array_counter)
    ax.plot(array_counter, y_mean, label='Mean', linestyle='--')
    ax.legend(loc='upper right')
    ax.set(xlabel='# games', ylabel='score')
    plt.show()


def get_mean_stdev(array):
    return statistics.mean(array), statistics.stdev(array)


def test(params):
    params['load_weights'] = True
    params['train'] = False
    params["test"] = False
    score, mean, stdev = run(params)
    return score, mean, stdev


# TODO: Throw this in the game loop for the first player move
# once it gets to the players turn start with a default action
# then we can train
def initialize_game(start_state: GameState, agent: DQNAgent, batch_size):
    state_init1 = agent.get_state(start_state)
    next_state = run_game_loop(start_state, True, False, True, agent, state_init1)
    action = [1, 0, 0, 0, 0, 0]
    state_init2 = agent.get_state(next_state)
    reward1 = agent.set_reward(next_state)
    isFin = next_state.isWin() or next_state.isLose()
    agent.remember(state_init1, action, reward1, state_init2, isFin)
    agent.replay_new(agent.memory, batch_size)
    return next_state


def translateAction(actionArr):
    if actionArr[0] == 1:
        return Actions.FIRE
    elif actionArr[1] == 1:
        return Actions.RIGHT
    elif actionArr[2] == 1:
        return Actions.UP
    elif actionArr[3] == 1:
        return Actions.LEFT
    elif actionArr[4] == 1:
        return Actions.DOWN
    elif actionArr[5] == 1:
        return Actions.STOP

def get_record(score, record):
    if score >= record:
        return score
    else:
        return record

def run(params):
    """
        Run the DQN algorithm, based on the parameters previously set.
    """
    # set to false to turn off print statements
    visualize_game = True
    # set to true to look at agent and bullet matrices
    visualize_heuristics = False

    agent = DQNAgent(params)
    agent = agent.to(DEVICE)
    agent.optimizer = optim.Adam(agent.parameters(), weight_decay=0, lr=params['learning_rate'])
    counter_games = 0
    score_plot = []
    counter_plot = []
    record = 0
    total_score = 0


    if params['test']:
        field_titles = ["Game#", "Enemies_Killed", "Enemy Types Killed", "HP_Lost", "End_Status", "Turns_Survived", "Score",
                    "Time at End of Simulation"]

        list_values = []
    game_counter = 1

    while counter_games < params['episodes']:
        # Initialize classes
        starting_gamestate = GameState(board_len=BOARD_COLUMNS, board_height=BOARD_ROWS,
                                       max_enemies_at_one_time=MAX_ENEMIES_AT_ANY_TIME,
                                       turns_left=TURNS_UNTIL_GAME_FINISHED,
                                       player_lives=PLAYER_LIVES)

        # player will be of size 1 X 1
        player_agent = PlayerAgent(1, 1, PLAYER_INITIAL_SPAWN_ROW_POSITION,
                                   PLAYER_INITIAL_SPAWN_COL_POSITION)

        player_agent.set_hp(PLAYER_HP)

        did_add_agent = starting_gamestate.addAgent(player_agent)

        if (did_add_agent == False):
            raise RuntimeError("Could not add player agent")

        end_line = "=" * 50

        if visualize_game:
            print("Staring GameState")
            print_board(starting_gamestate)
            print(end_line, "\n")

        # now we must run the game through a single loop
        current_state = initialize_game(starting_gamestate, agent, params['batch_size'])

        steps = 0  # steps since the last positive reward
        while current_state.isWin() is False and current_state.isLose() is False:
            if not params['train']:
                agent.epsilon = 0.01
            else:
                # agent.epsilon is set to give randomness to actions
                agent.epsilon = 1 - (counter_games * params['epsilon_decay_linear'])

            # get old state
            state_old = agent.get_state(current_state)

            current_state, final_move = run_game_loop(current_state, visualize_game,
                                                        visualize_heuristics, False, agent, state_old)
            #now that we have the old

            state_new = agent.get_state(current_state)

            # set reward for the new state
            reward = agent.set_reward(current_state)

            isFin = current_state.isWin() or current_state.isLose()

            # if food is eaten, steps is set to 0
            if reward > 0:
                steps = 0

            if params['train']:
                # train short memory base on the new action and state
                agent.train_short_memory(state_old, final_move, reward, state_new, isFin)
                # store the new data into a long term memory
                agent.remember(state_old, final_move, reward, state_new, isFin)

            record = get_record(current_state.score, record)

            steps += 1

        if params['train']:
            agent.replay_new(agent.memory, params['batch_size'])
        counter_games += 1
        print(f"Game# {counter_games} Completed at {datetime.today().strftime('%H:%M %p')}")
        total_score += current_state.score
        print(f'Game {counter_games}      Score: {current_state.score}')

        if params['test']:
            if current_state.isLose() == True:
                lost_hp = 3
                endStatus = "Lose"
            else:
                lost_hp = 3 - current_state.current_agents[0].get_hp()
                endStatus = "Win"
            turns_survived = 300 - current_state.turns_left
            entry = [counter_games, current_state.removed_agents, current_state.removed_types, lost_hp,
                     endStatus, turns_survived,
                     current_state.score,datetime.today().strftime('%H:%M %p')]
            list_values.append(entry)
        score_plot.append(current_state.score)
        counter_plot.append(counter_games)

    mean, stdev = get_mean_stdev(score_plot)
    if params['train']:
        model_weights = agent.state_dict()
        torch.save(model_weights, params["weights_path"])
    if params['test']:
        with open(LOG_CSV, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(field_titles)

            # write multiple rows
            writer.writerows(list_values)

        print("File complete")
    if params['plot_score']:
        plot_seaborn(counter_plot, score_plot, params['train'])
    return total_score, mean, stdev


# This also needs to return the action take as a vector
def run_game_loop(current_state: GameState, visualize_game, visualize_heuristics, def_Action, agent, state_old):
    end_line = "=" * 50
    # have each agent take an action
    final_move = None
    for each_index in range(0, len(current_state.current_agents)):

        each_index = each_index - current_state.removed_agents
        # print(f"updated index is {each_index}")

        try:
            each_agent: AgentInterface = current_state.current_agents[each_index]
        except IndexError:
            # print("BREAKING FOR LOOP")
            break

        if each_agent.hasMoved():
            if each_index + 1 > len(current_state.current_agents) - 1:
                break
            else:
                continue  # move on to next agent

        if each_agent.isPlayer():
            # TODO DAN YOU WILL HAVE TO MAKE YOUR OWN PLAYER AGENT CLASS and overwrite auto pick action

            if (def_Action):
                agent_action = DEFAULT_PLAYER_ACTION

            else:
                # perform random actions based on agent.epsilon, or choose the action
                if random.uniform(0, 1) < agent.epsilon:
                    final_move = np.eye(6)[randint(0, 5)]
                else:
                    # predict action based on the old state
                    with torch.no_grad():
                        state_old_tensor = torch.tensor(state_old.reshape((1, 392)), dtype=torch.float32).to(DEVICE)
                        prediction = agent(state_old_tensor)
                        final_move = np.eye(6)[np.argmax(prediction.detach().cpu().numpy()[0])]

                agent_action = translateAction(final_move)

        elif each_agent.isHeuristicAgent():
            agent_action = each_agent.autoPickAction(current_state)
        else:
            agent_action = each_agent.autoPickAction()

        try:
            current_state = current_state.generateSuccessorState(each_index, agent_action)
        except IndexError:
            break

    # once all agents have taken an action decrement the turn
    current_state.decrement_turn()
    # Reset move status of agents after everyone has moved
    current_state.reset_agents_move_status()

    # print(end_line)

    # spawn enemies at the start of new turn
    if len(current_state.current_agents) - 1 < current_state.max_enemies_at_any_given_time:
        # spawn enemy based on spawn rate
        probability_to_spawn = random.randint(0, 100)
        if probability_to_spawn <= ENEMY_SPAWNER.spawn_rate:
            # pick an enemy
            enemy_to_spawn = ENEMY_SPAWNER.choose_enemy()
            current_state.addAgent(enemy_to_spawn)

    # Optional board visualization
    if visualize_game:
        print_projectile_locations(current_state)
        print_enemies_status(current_state)
        print_player_status(current_state)
        print_score(current_state)
        print_board(current_state)
        print(f"HP left: {current_state.current_agents[0].get_hp()}")
        print(f"Game Over: {current_state.isWin() or current_state.isLose()}")
        print(end_line, "\n")

    if visualize_heuristics:
        myBoard = current_state.gameBoard.get_board_with_agents_RL(current_state, 2, 5)
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

    if def_Action:
        return current_state
    else:
        return current_state, final_move


#################################
#   Define parameters manually  #
#################################
LOADED_TRAINING = '3000'
LOG_CSV = 'logs/RLStats_' + LOADED_TRAINING + '_2' + '.csv'
LOG_NAME = 'logs/logfile_' + LOADED_TRAINING + '_2' + '.txt'
if LOGGING:
    sys.stdout = open(LOG_NAME, 'w')
def define_parameters():
    params = dict()
    # Neural Network
    params['epsilon_decay_linear'] = 1 / 100
    params['learning_rate'] = 0.00013629
    params['first_layer_size'] = 200  # neurons in the first layer
    params['second_layer_size'] = 100  # neurons in the second layer
    params['third_layer_size'] = 50  # neurons in the third layer
    params['episodes'] = 10
    params['memory_size'] = 2500
    params['batch_size'] = 1000
    # Settings
    params['weights_path'] = 'weights/weights' + LOADED_TRAINING + '.h5'
    params['train'] = False
    params["test"] = True
    params['plot_score'] = True
    params['log_path'] = 'logs/scores_' + str(datetime.now().strftime("%Y%m%d%H%M%S")) + "_" + LOADED_TRAINING + '.txt'
    params['turns'] = TURNS_UNTIL_GAME_FINISHED
    return params

if __name__ == '__main__':
    # Set options to activate or deactivate the game view, and its speed
    parser = argparse.ArgumentParser()
    params = define_parameters()
    #parser.add_argument("--bayesianopt", nargs='?', type=distutils.util.strtobool, default=False)
    args = parser.parse_args()
    print("Args", args)
    params['display'] = False
    #params['speed'] = args.speed
    if params['train']:
        print("Training...")
        params['load_weights'] = False  # when training, the network is not pre-trained
        run(params)
    if params['test']:
        print("Testing...")
        params['train'] = False
        params['load_weights'] = True
        run(params)
