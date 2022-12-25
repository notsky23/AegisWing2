import unittest

from Model.GameBoard import GameBoard
from modelPositionToTkinterViewAdapter import createAdapterDict

"""
This class tests that the modelToView Adapter method.
"""
class TestModelToViewAdapter(unittest.TestCase):
    def setUp(self) -> None:
        self.gboard = GameBoard(5,8)

    def test_adapater(self):
        height_dict = createAdapterDict(self.gboard)

        self.assertEquals(7, height_dict[0])
        self.assertEquals(6, height_dict[1])
        self.assertEquals(5, height_dict[2])
        self.assertEquals(4, height_dict[3])
        self.assertEquals(3, height_dict[4])
        self.assertEquals(2, height_dict[5])
        self.assertEquals(1, height_dict[6])
        self.assertEquals(0, height_dict[7])

def main():
    unittest.main(verbosity=3)

if __name__ == '__main__':
    main()