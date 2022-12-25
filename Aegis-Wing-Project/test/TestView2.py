from Model.GameModel import GameModel
from Controller.Controller import Controller
from View.View2 import View2

def main():
    """
    Example of gameplay
    :return:
    """
    view = View2()
    # default values
    gameModel = GameModel()
    controller = Controller(view, gameModel)
    controller.go()


if __name__ == "__main__":
    main()