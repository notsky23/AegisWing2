from Model.GameBoard import GameBoard


def createAdapterDict(gameBoard : GameBoard) -> dict:
    """
    This function will create a dictionary that can be used to transform
    gameboard model data to appropriate view position data.
    :param gameBoard:
    :return:
    """


    adapterDictHeight = {}

    height = gameBoard.board_height
    #model has 0 at lower left corner and only pos values up and right
    #view has 0 at upper left corner with pos values Down and pos values to the right



    for j in range(height):
        adapterDictHeight[j] = height - 1 - j

    return adapterDictHeight