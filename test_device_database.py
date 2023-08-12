import unittest, random
from othello17 import Othello


class TestOthello(unittest.TestCase):
    def setUp(self):
        global O_1, O_2, O_3, O_4
        O_1 = Othello(active_player=1, players=["human", "human"])
        O_2 = Othello(active_player=2, players=["computer", "computer"])

        blue = []
        for i in range(2, 6):
            blue += [[2, i, 1], [i, 2, 1], [5, i, 1], [i, 5, 1]]
            orange = []
        for i in range(1, 7):
            orange += [[1, i, 2], [i, 1, 2], [6, i, 2], [i, 6, 2]]

        O_3 = Othello(discs=blue + orange, active_player=1, players=["human", "human"])
        O_4 = Othello(discs=blue + orange, active_player=2, players=["human", "human"])

        self.player_1_legal_moves = [[2, 4], [3, 5], [4, 2], [5, 3]]
        self.player_2_legal_moves = [[2, 3], [3, 2], [4, 5], [5, 4]]
        self.invalid_moves = [[1, 2], [1, 3], [7, 7], [6, 4]]

    def tearDown(self):
        global O_1, O_2, O_3, O_4
        del O_1, O_2, O_3, O_4

    def test_get_board_pos(self):
        # Ranges for mouse values:
        mouse_x_min = O_1.offset
        x_width = 8 * O_1.tile_size  # width of board in pixels
        mouse_y_min = O_1.offset
        y_height = 8 * O_1.tile_size  # height of board in pixels

        # Emulate 100 random mouse clicks:
        for i in range(100):
            mx = mouse_x_min + random.random() * x_width
            my = mouse_y_min + random.random() * y_height
            col_actual, row_actual = O_1.get_board_pos(mx, my)
            col_correct = int((mx - O_1.offset) / O_1.tile_size)
            row_correct = 7 - int((my - O_1.offset) / O_1.tile_size)
            self.assertEqual(col_actual, col_correct)
            self.assertEqual(row_actual, row_correct)

    def test_move_legal(self) -> True:
        # test the valid and invalid moves for player 1
        if O_1.active_player == 1:
            for [col, row] in self.player_1_legal_moves:
                legal_move1 = O_1.move_legal(col, row)
                self.assertTrue(legal_move1)
            for [col, row] in self.invalid_moves:
                invalid_move1 = O_1.move_legal(col, row)
                self.assertFalse(invalid_move1)

        # test the valid and invalid moves for player 2
        if O_2.active_player == 2:
            for [col, row] in self.player_2_legal_moves:
                legal_move2 = O_2.move_legal(col, row)
                self.assertTrue(legal_move2)
            for [col, row] in self.invalid_moves:
                invalid_move2 = O_2.move_legal(col, row)
                self.assertFalse(invalid_move2)

    def test_player_human(self) -> True:
        # test both players to be human for test class O_1
        test1_a = O_1.player_human()
        self.assertTrue(test1_a)
        O_1.switch_active_player()
        test1_b = O_1.player_human()
        self.assertTrue(test1_b)

        # test both players to be computers for test class O_2
        test2_a = O_2.player_human()
        self.assertFalse(test2_a)
        O_2.switch_active_player()
        test2_b = O_2.player_human()
        self.assertFalse(test2_b)

    def test_valid_pos(self) -> True:
        # test all 64 col and row positions
        for col in range(0, 8):
            for row in range(0, 8):
                valid_test = O_1.valid_pos(col, row)
                self.assertTrue(valid_test)

        # test 16 invalid positions
        invalid_pos = [
            [-1, 23],
            [13, 13],
            [2, 19],
            [0, 7.019],
            [3, -19],
            [1, 8],
            [0, 100],
            [62, 1],
            [5, 10],
            [12, 29],
            [3, 21],
            [5, -10],
            [9, 1],
            [65, 65],
            [-76, 54],
            [99, 99],
        ]

        for [col, row] in invalid_pos:
            invalid_test = O_1.valid_pos(col, row)
            self.assertFalse(invalid_test)

    def test_switch_active_player(self) -> True:
        # Initialize two variables
        player_one = 1
        player_two = 2

        # Tests switching active player ten times starting with active player one
        for i in range(10):
            self.assertEqual(O_1.active_player, player_one)
            O_1.switch_active_player()
            self.assertEqual(O_1.active_player, player_two)
            O_1.switch_active_player()

    def test_count(self) -> True:
        first_set_up = O_1.count()
        second_set_up = O_3.count()
        self.assertEqual(first_set_up, (2, 2))
        self.assertEqual(second_set_up, (12, 20))

    def test_get_value(self) -> True:
        # Set values to the array A in order to test it
        for col in range(8):
            for row in range(4):
                O_1.set_value(col, row, 1)

        for col in range(8):
            for row in range(4, 8):
                O_1.set_value(col, row, 2)

        # Test the method get_value(). If this will pass, the method set_value() also works.
        for col in range(8):
            for row in range(4):
                value = O_1.get_value(col, row)
                self.assertEqual(value, 1)

        for col in range(8):
            for row in range(4, 8):
                value = O_1.get_value(col, row)
                self.assertEqual(value, 2)

    def test_check_board_pos(self) -> True:
        player_1_legal_moves = [
            [3, 3, 0],
            [0, 4, 2],
            [4, 3, 0],
            [7, 0, 1],
            [7, 1, 1],
            [5, 0, 2],
        ]
        player_2_legal_moves = [
            [3, 3, 5],
            [4, 3, 5],
            [5, 0, 0],
            [0, 4, 0],
            [7, 2, 0],
            [3, 7, 0],
        ]

        if O_3.active_player == 1:
            for [col, row, captured] in player_1_legal_moves:
                captured_actual = O_3.check_board_pos(col, row)
                self.assertEqual(captured_actual, captured)

        if O_4.active_player == 2:
            for [col, row, captured] in player_2_legal_moves:
                captured_actual = O_4.check_board_pos(col, row)
                self.assertEqual(captured_actual, captured)


if __name__ == "__main__":
    unittest.main()
