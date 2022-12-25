import unittest

from Model.Agents.Actions import Actions
from Model.Agents.AgentSuperClass import AgentSuperClass

"""
This class verifies correct behavior of 
methods in the AgentSuperClass.
"""
class AgentSuperClassTest(unittest.TestCase):
    def setUp(self) -> None:

        self.a1 = AgentSuperClass()
        self.a2 = AgentSuperClass(agent_length=2, agent_height=3, lowest_row=4, least_col=6)

    def test_default_constructor(self):
        a1 = self.a1
        a2 = self.a2

        self.assertEquals((1,1), a1.get_agent_size())
        self.assertEquals((0,0), a1.get_position())

    def test_custom_construct_values(self):
        a1 = self.a1
        a2 = self.a2

        self.assertEquals((4,6), a2.get_position())
        self.assertEquals((2,3), a2.get_agent_size())

    def test_raise_constructor_errors(self):
        with self.assertRaises(ValueError):
            AgentSuperClass(agent_length= 0)

        with self.assertRaises(ValueError):
            AgentSuperClass(agent_height= 0)

    def test_get_min_col_boundary(self):
        a1 = self.a1
        a2 = self.a2

        a1_col_min = a1.get_col_boundaries()[0]
        a2_col_min = a2.get_col_boundaries()[0]

        self.assertEquals(0, a1_col_min)

        # i.e. if lowest col is 4 and length is 2
        # agent occupies spaces 4, and 5, not 6
        self.assertEquals(6, a2_col_min)

    def test_get_max_col_boundary(self):
        a1 = self.a1
        a2 = self.a2

        a1_max_col_b = a1.get_max_col_boundary()
        a2_max_col_b = a2.get_max_col_boundary()
        self.assertEquals(0, a1_max_col_b)
        self.assertEquals(7, a2_max_col_b)

    def test_get_col_boundaries(self):
        a1 = self.a1
        a2 = self.a2

        self.assertEquals((0,0), a1.get_col_boundaries())
        self.assertEquals((6,7), a2.get_col_boundaries())

    def test_get_min_row_boundary(self):
        a1 = self.a1
        a2 = self.a2

        a1_min_row_b = a1.lowest_row
        a2_min_row_b = a2.lowest_row

        self.assertEquals(0,a1_min_row_b)
        self.assertEquals(4, a2_min_row_b)

    def test_get_row_boundaries(self):
        a1 = self.a1
        a2 = self.a2
        a1_row_bounds = a1.get_row_boundaries()
        a2_row_bounds = a2.get_row_boundaries()

        self.assertEquals((0,0), a1_row_bounds)
        self.assertEquals((4,6), a2_row_bounds)

    def testSetGetHP(self):
        a1 = self.a1
        a2 = self.a2

        self.assertEquals(1,a1.get_hp())
        a2.set_hp(10)
        self.assertEquals(10, a2.get_hp())
        a1.set_hp(0)
        self.assertEquals(0,a1.get_hp())
        self.assertTrue(a1.is_dead()) # if hp = 0 then they are dead

    def testSetPos(self):
        a1 = self.a1
        a2 = self.a2

        a1.set_position(2,5)
        a1_row_bounds = a1.get_row_boundaries()
        a1_col_bounds = a1.get_col_boundaries()
        self.assertEquals((2,2), a1_row_bounds)
        self.assertEquals((5,5), a1_col_bounds)

        #a2_length=2, a2_height=3
        a2.set_position(-2,6)
        a2_row_bounds = a2.get_row_boundaries()
        a2_col_bounds = a2.get_col_boundaries()
        # -2 + 3 - 1 = 0
        self.assertEquals((-2,0), a2_row_bounds) # bounds of row/height
        # 6 + 2 - 1 = 7
        self.assertEquals((6,7), a2_col_bounds) # bounds of col/length

    def testPerformAction(self):
        a1 = self.a1
        a2 = self.a2

        UP = Actions.UP
        DOWN = Actions.DOWN
        LEFT = Actions.LEFT
        RIGHT = Actions.RIGHT

        a1.performAction(UP)
        self.assertEquals((1,1), a1.get_row_boundaries())

        a1.performAction(RIGHT)
        self.assertEquals((1,1), a1.get_col_boundaries())

        # a2_length=2, a2_height=3, least row = 4 , least col = 6
        a2.performAction(DOWN)
        self.assertEquals((3, 5), a2.get_row_boundaries())

        a2.performAction(LEFT)
        self.assertEquals((5, 6), a2.get_col_boundaries())



def main():
    unittest.main(verbosity=3)

if __name__ == '__main__':
    main()