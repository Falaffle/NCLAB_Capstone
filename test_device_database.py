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

    def test_sql_execute(self) -> True:
        # Initialize test parameters
        sqlquery = "SELECT * FROM devices WHERE property_number = 'b000001'"
        message = "Showing devices..."

        test_sql_output = [
            (
                "b000001",
                "Durgod",
                "Keyboard",
                "08/02/2023",
                "08/18/2024",
                "jane_doe@gmail.com",
            )
        ]
        actual_sql_output = []

        data = C.sql_execute(sqlquery, message)
        for row in data:
            actual_sql_output.append(row)

        # Test method output to test list
        self.assertEqual(actual_sql_output, test_sql_output)

    def test_sql_executemany(self) -> True:
        # Initialize test parameters
        sqlquery1 = "INSERT INTO devices (property_number, manufacturer, description, cal_date, cal_due, custodian_email) VALUES (?, ?, ?, ?, ?, ?)"
        test_devices = [
            (
                "b000007",
                "Filco",
                "Keyboard",
                "08/18/2023",
                "08/18/2024",
                "jane_doe1337@gmail.com",
            )
        ]
        message1 = "Adding devices..."
        data = C.sql_executemany(sqlquery1, test_devices, message1)

        sqlquery2 = "SELECT * FROM devices WHERE property_number = 'b000007'"
        message2 = "Showing devices..."

        actual_sql_output = []

        data = C.sql_execute(sqlquery2, message2)
        for row in data:
            actual_sql_output.append(row)

        # Test method output to test list
        self.assertEqual(actual_sql_output, test_devices)

    def test_generate_devices_list(self) -> True:
        # Initialize comparison property numbers
        test_devices_list_true = [
            (
                "b000001",
                "Durgod",
                "Keyboard",
                "08/02/2023",
                "08/18/2024",
                "jane_doe@gmail.com",
            ),
            (
                "b000002",
                "National Instruments",
                "PXIe 5160 Oscilloscope",
                "03/02/2023",
                "03/02/2024",
                "john_doe1337@gmail.com",
            ),
            (
                "b000003",
                "Fluke",
                "Digital Multi-meter",
                "08/03/2022",
                "08/03/2023",
                "john_doe1337@gmail.com",
            ),
            (
                "b000004",
                "Newport",
                "Optical Detector",
                "07/01/2022",
                "07/01/2023",
                "john_doe1337@gmail.com",
            ),
            (
                "b000005",
                "Thorlabs",
                "Optical Power Meter",
                "01/02/2023",
                "01/01/2024",
                "john_doe1337@gmail.com",
            ),
        ]

        # Tests method output to test list
        self.assertEqual(C.generate_devices_list(), test_devices_list_true)

    def test_generate_property_list(self) -> True:
        # Initialize comparison property numbers
        test_property_numbers_true = [
            "b000001",
            "b000002",
            "b000003",
            "b000004",
            "b000005",
        ]

        # Tests method output to test list
        self.assertEqual(C.generate_property_list(), test_property_numbers_true)

    def test_generate_email_list(self) -> True:
        # Initialize comparison property numbers
        test_email_list_true = ["john_doe1337@gmail.com"]

        # Tests method output to test list
        self.assertEqual(C.generate_email_list(), test_email_list_true)

    def test_display_column_names(self) -> True:
        # Initialize comparison results
        test_column_names_true = (
            "property_number",
            "manufacturer",
            "description",
            "cal_date",
            "cal_due",
            "custodian_email",
        )

        # Tests method output to test list
        self.assertEqual(C.display_column_names(), test_column_names_true)

    @patch("builtins.input")
    def test_pn_prompt(self, mocked_input) -> True:
        # Initialize comparison results
        test_pn_prompt = "b000001"

        # Tests method output to test prompt
        mocked_input.return_value = "b000001"
        self.assertEqual(C.pn_prompt(), test_pn_prompt)

    @patch("builtins.input")
    def test_pn_prompt_add(self, mocked_input) -> True:
        # Initialize comparison results
        test_pn_prompt = "b000099"

        # Tests method output to test prompt
        mocked_input.return_value = "b000099"
        self.assertEqual(C.pn_prompt_add(), test_pn_prompt)

    @patch("builtins.input")
    def test_date_prompt(self, mocked_input) -> True:
        # Initialize comparison results
        test_date_prompt = "03/21/1989"

        # Tests method output to test prompt
        mocked_input.return_value = "03/21/1989"
        self.assertEqual(C.pn_prompt_add(), test_date_prompt)

    @patch("builtins.input")
    def test_date_prompt(self, mocked_input) -> True:
        # Initialize comparison results
        test_due_prompt = "03/21/1989"

        # Tests method output to test prompt
        mocked_input.return_value = "03/21/1989"
        self.assertEqual(C.pn_prompt_add(), test_due_prompt)

    @patch("builtins.input")
    def test_column_prompt(self, mocked_input) -> True:
        # Initialize comparison results
        test_column_prompt = [
            "property_number",
            "manufacturer",
            "description",
            "cal_date",
            "cal_due",
            "custodian_email",
        ]

        # Tests method output to test prompt
        for i in range(len(test_column_prompt)):
            mocked_input.return_value = test_column_prompt[i]
            self.assertEqual(C.column_prompt(), test_column_prompt[i])

    @patch("builtins.input")
    def test_add_device(self, mock_pn_prompt) -> True:
        # Initialize comparison list
        test_list = [
            "INSERT INTO devices (property_number, manufacturer, description, cal_date, cal_due, custodian_email) VALUES (?, ?, ?, ?, ?, ?)",
            [
                (
                    "b000010",
                    "Logi",
                    "Speakers",
                    "01/01/2023",
                    "01/01/2024",
                    "john_doe1337@gmail.com",
                )
            ],
            "Device added!",
        ]

        # Tests method output to test add device
        mock_pn_prompt.side_effect = [
            "b000010",
            "Logi",
            "Speakers",
            "01/01/2023",
            "01/01/2024",
            "john_doe1337@gmail.com",
        ]

        actual_sqlquery, actual_device, actual_message = C.add_device()
        actual_list = [actual_sqlquery, actual_device, actual_message]
        self.assertEqual(actual_list, test_list)

    def test_create_cal_table(self) -> True:
        # Initialize comparison result
        test_result = "CREATE TABLE IF NOT EXISTS test_devices (property_number TEXT UNIQUE, manufacturer TEXT, description TEXT, cal_date TEXT, cal_due TEXT, custodian_email TEXT)"

        # Tests method output
        self.assertEqual(C.create_cal_table('test_devices'), test_result)

    @patch("builtins.print")
    @patch("builtins.input")
    def test_display_data(self, mocked_input, mocked_print) -> True:
        # Actual test
        mocked_input.side_effect = ["pn"]
        C.display_data()
        mocked_print.assert_called_with(
            (
                "b000005",
                "Thorlabs",
                "Optical Power Meter",
                "01/02/2023",
                "01/01/2024",
                "john_doe1337@gmail.com",
            )
        )
    
    @patch("builtins.print")
    @patch("builtins.input")
    def test_select(self, mocked_input, mocked_print) -> True:
        # Actual test
        mocked_input.side_effect = ["SELECT * FROM devices WHERE property_number = 'b000001'"]
        C.select()
        mocked_print.assert_called_with(('b000001', 'Durgod', 'Keyboard', '08/02/2023', '08/18/2024', 'jane_doe@gmail.com'))

    @patch("builtins.input")
    def test_delete_device(self, mocked_input) -> True:
        # Initialize comparison result
        test_sqlquery = "DELETE FROM devices WHERE property_number = 'b000001'"
        test_message = "Device deleted!"
        test_result = [test_sqlquery, test_message]
        mocked_input.side_effect = ['b000001']
        
        # Test method output
        actual_sqlquery, actual_message = C.delete_device()
        actual_result = [actual_sqlquery, actual_message]
        self.assertEqual(actual_result, test_result)
    
    @patch("builtins.print")
    @patch("builtins.input")
    def test_append(self, mocked_input, mocked_print) -> True:
        C.append('test_devices')
        mocked_input.side_effect = ["SELECT * FROM test_devices WHERE property_number = 'b000006'"]
        C.select()
        mocked_print.assert_called_with(('b000006', 'Thorlabs', 'Optical Power Meter', '01/01/23', '01/01/24', 'john_doe1337@gmail.com'))
        
    @patch("builtins.print")
    @patch("builtins.input")
    def test_replace(self, mocked_input, mocked_print) -> True:
        C.create_cal_table('test_replace_devices')
        C.replace('test_replace_devices')
        mocked_input.side_effect = ["SELECT * FROM test_replace_devices WHERE property_number = 'b000005'"]
        C.select()
        mocked_print.assert_called_with(('b000005', 'Thorlabs', 'Optical Power Meter', '01/02/2023', '01/01/2024', 'john_doe1337@gmail.com'))


# Main Program
if __name__ == "__main__":
    unittest.main()
