import unittest
from unittest import mock
from unittest.mock import patch
from device_database import Cal_Database


class TestCal_Database(unittest.TestCase):
    def setUp(self) -> None:
        global C
        C = Cal_Database()

    def tearDown(self) -> None:
        global C
        del C

    def test_generate_devices_list(self) -> True:
        # Initialize comparison property numbers
        test_devices_list_true = [
            (
                "B000001",
                "Durgod",
                "Keyboard",
                "08/18/2023",
                "08/18/2024",
                "jane_doe@gmail.com",
            ),
            (
                "B000002",
                "National Instruments",
                "PXIe 5160 Oscilloscope",
                "01/01/2023",
                "03/02/2024",
                "john_doe1337@gmail.com",
            ),
            (
                "B000003",
                "Fluke",
                "Digital Multi-meter",
                "08/03/2022",
                "08/03/2023",
                "john_doe1337@gmail.com",
            ),
            (
                "B000004",
                "Newport",
                "Optical Detector",
                "07/01/2022",
                "07/01/2023",
                "john_doe1337@gmail.com",
            ),
            (
                "B000005",
                "Thorlabs",
                "Optical Power Meter",
                "01/02/2023",
                "01/01/2024",
                "jane_doe1337@yahoo.com",
            ),
        ]

        # Tests method output to test list
        self.assertEqual(C.generate_devices_list(), test_devices_list_true)

    def test_generate_property_list(self) -> True:
        # Initialize comparison property numbers
        test_property_numbers_true = ["B000001", "B000002", "B000003", "B000004", "B000005"]
        
        # Tests method output to test list
        self.assertEqual(C.generate_property_list(), test_property_numbers_true)

    def test_generate_email_list(self) -> True:
        # Initialize comparison property numbers
        test_email_list_true = ['john_doe1337@gmail.com']

        # Tests method output to test list
        self.assertEqual(C.generate_email_list(), test_email_list_true)

    def test_display_column_names(self) -> True:
        # Initialize comparison results
        test_column_names_true = ('property_number', 'manufacturer', 'description', 'cal_date', 'cal_due', 'custodian_email')

        # Tests method output to test list
        self.assertEqual(C.display_column_names(), test_column_names_true)

    @patch("builtins.input")
    def test_pn_prompt(self, mocked_input) -> True:
        # Initialize comparison results
        test_pn_prompt = 'B000001'

        # Tests method output to test prompt
        mocked_input.return_value = 'B000001'
        self.assertEqual(C.pn_prompt(), test_pn_prompt)

    @patch("builtins.input")
    def test_pn_prompt_add(self, mocked_input) -> True:
        # Initialize comparison results
        test_pn_prompt = 'B000099'

        # Tests method output to test prompt
        mocked_input.return_value = 'B000099'
        self.assertEqual(C.pn_prompt_add(), test_pn_prompt)

    @patch("builtins.input")
    def test_date_prompt(self, mocked_input) -> True:
        # Initialize comparison results
        test_date_prompt = '03/21/1989'

        # Tests method output to test prompt
        mocked_input.return_value = '03/21/1989'
        self.assertEqual(C.pn_prompt_add(), test_date_prompt)

    @patch("builtins.input")
    def test_date_prompt(self, mocked_input) -> True:
        # Initialize comparison results
        test_due_prompt = '03/21/1989'

        # Tests method output to test prompt
        mocked_input.return_value = '03/21/1989'
        self.assertEqual(C.pn_prompt_add(), test_due_prompt)

    '''@patch('device_database.Cal_Database.pn_prompt_add')
    def test_add_device(self, mock_pn_prompt):
        # Initialize comparison results
        test_new_device = [('B000010', 'Logi', 'Speakers','01/01/2023','01/01/2024','john_doe1337@gmail.com')]

        # Tests method output to test add device
        mock_pn_prompt.return_value = 'B000010'
        self.assertEqual(C.add_device(), test_new_device)'''


# Main Program
if __name__ == "__main__":
    unittest.main()
