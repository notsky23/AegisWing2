#turtle screen set up
import turtle as turtle_module

from Model.Agents.AgentInterface import AgentInterface


class SimpleTurtleView:
    def __init__(self):
        #self.window = turtle_module.Screen()
        self.lowest_x_cord_value = None
        self.max_x_cord_value = None
        self.lowest_y_cord_value = None
        self.max_y_cord_value = None

        self.turtle_ships = []
        self.turtle_dict = {}

    def set_coord_values(self,min_x: int, max_x: int, min_y: int, max_y: int):
        self.lowest_x_cord_value = min_x
        self.max_x_cord_value = max_x
        self.lowest_y_cord_value = min_y
        self.max_y_cord_value = max_y

        self.window = turtle_module.Screen()
        self.window.setworldcoordinates(self.lowest_x_cord_value,
                                        self.lowest_y_cord_value,
                                        self.max_x_cord_value,
                                        self.max_y_cord_value)

    def produce_turtle(self,x_pos, y_pos, isPlayer: bool = False):
        turtle_color = "black"
        if isPlayer == False:
            turtle_color = "red"

        t = turtle_module.Turtle()
        t.hideturtle()
        t.shape("square")
        t.color(turtle_color)
        t.penup()
        t.shapesize(2,3,1)
        t.speed(0)
        t.setpos(x_pos,y_pos)
        t.showturtle()


    def set_up_turtles(self, list_agents):
        #clears registry as well so clears onkey press
        self.window.clear() # delete all turtles, maybe add a delay for movement?

        #for turtle in self.window.turtles():
            #turtle.reset()

        self.turtle_ships = []

        for i in range(len(list_agents)):
            each_enemy : AgentInterface = list_agents[i]

            # if enemy turtle larger size than 1
            x_low, x_high = each_enemy.get_col_boundaries()
            y_low, y_high = each_enemy.get_row_boundaries()

            x_range = x_high - x_low
            y_range = y_high - y_low

            if each_enemy.isPlayer() == True:
                is_player_turtle = True
            else:
                is_player_turtle = False

            # if length enemy > 1
            if x_range > 0:
                # make individual turtles to represent all segments
                #of current ship on that row
                # high + 1 because for loop is exclusive of last value
                for x_range_value in range(x_low, x_high + 1):
                    #more than 1 row tall
                    if y_range > 0:
                        for y_range_value in range(y_low, y_high + 1):
                            enemy_turtle = self.produce_turtle(x_range_value, y_range_value, is_player_turtle)
                            self.turtle_ships.append(enemy_turtle)
                    else:
                        enemy_turtle = self.produce_turtle(x_range_value, y_low, is_player_turtle)
                        self.turtle_ships.append(enemy_turtle)
            else:
                # if enemy only 1 unit long
                if y_range > 0:
                    for y_range_value in range(y_low, y_high + 1):
                        enemy_turtle = self.produce_turtle(x_low, y_range_value, is_player_turtle)
                        self.turtle_ships.append(enemy_turtle)
                else:
                    enemy_turtle = self.produce_turtle(x_low,y_low, is_player_turtle)
                    self.turtle_ships.append(enemy_turtle)