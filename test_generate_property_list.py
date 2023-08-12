import unittest
from device_database import Cal_Database


class TestCal_Database(unittest.TestCase):

    def setUp(self) -> None:
        global C
        C = Cal_Database()

    def tearDown(self) -> None:
        global C
        del C

    def test_generate_property_list(self) -> True:
        # Initialize comparison property numbers
        test_property_numbers_true = ["B000001", "B000002", "B000003", "B000004", "B000005"]
        
        # Tests method output to test list
        self.assertEqual(C.generate_property_list(), test_property_numbers_true)
            

# Main Program
if __name__ == "__main__":
    unittest.main()
