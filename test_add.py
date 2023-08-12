import unittest
from unittest import mock
from device_database import Cal_Database


class TestCal_Database(unittest.TestCase):

    def setUp(self) -> None:
        global C
        C = Cal_Database()

    def tearDown(self) -> None:
        global C
        del C

    @mock.patch('device_database.add_device')
    def test_add(self, mock_add_device) -> True:
        # Initialize comparison property numbers
        mock_add_device.return_value = True

        # Tests method output to test list
            

# Main Program
if __name__ == "__main__":
    unittest.main()
