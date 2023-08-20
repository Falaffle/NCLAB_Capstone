# Device Calibration Database

The capstone project for NCLAB python developer course. 

`Cal_Database` lets users add, delete, edit, and view a calibrated device database. Furthermore, it reminds custodians when their instruments are due for calibration.

Contents
========

 * [Overview](#Overview)
 * [Software Startup](#Software-Startup)
 * [Initialization](#Initialization)
 * [Columns](#Columns)
 * [Event Loop](#Event-Loop)
 * [Commands](#Commands)
 * [Command Details](#Command-Details)
 * [Special Thanks](#Special-Thanks)

### Overview

Our facility needed a way to keep track of calibrated instruments. This software allows users to:

+ Add device entries manually through the software.
+ Add device entries through an external csv file.
+ Replace the table entries with an external csv file.
+ Make changes to existing device information.
+ Delete devices from the database table.
+ Sort and display all entries by the desired column.
+ Export the entire database table into a csv file.
+ Remind custodians of upcoming device calibration expiration.

With this, we'll be able to be more proactive with sending instruments for calibration before expiration.

### Software Startup

To start the software `Cal_Database`, run the terminal then change the directory to the software's location.
Afterwards, simply run the software through the terminal. An example is shown below.

```bash
PS C:\Users\User\Documents\Python Code\Capstone\Cal_Database> python device_database.py
```

### Initialization

During initialization, the software will connect to `device_database.db` or create it if the file does not exist.
Like the database file, the software will also create a table in the database named `devices` if it does not exist.
Lastly, the software will check for upcoming expiration and send a reminder if it's less than or equal to 60 days.

### Columns

The table created by the software will have six fixed column names. These are:

+ `property_number` - The column for the company given property number of the device. This column will not have duplicates.
+ `manufacturer` - The column for the device manufacturer.
+ `description` - The column to describe the name and use for the device to help the custodian.
+ `cal_date` - The column for the date the device was calibrated.
+ `cal_due` - The column for the date the calibration will expire.
+ `custodian email` - The column for the custodian's email address.

### Event Loop

After Initialization, the user will be prompted to enter a command.

```bash
Please enter a command.
```

The commands can be accessed by entering `HELP`. If an invalid command was entered, an error message will be displayed.

```bash
Please enter a command.
invalid
Error: Invalid command! Try again or type HELP.
```

### Commands

The list of commands recognized by the software are the following:
+ `ADD` - Add devices manually via user input.
+ `APPEND` - Add devices via an external csv file.
+ `DELETE` - Given a property number, deletes a device from the database
+ `DISPLAY` - Displays all data from the database table
+ `HELP` - Displays the commands and its description
+ `QUIT` - Closes connection from the database and exits the program
+ `REMIND` - Sends an email reminder to custodians with upcoming calibration expiration
+ `REPLACE` - Replaces data in the devices table with data from calibration_data.csv
+ `SAVE` - Saves the table content to a csv file named calibration_data.csv
+ `SELECT` - Useful for advanced searches for displays data using advanced SQL commands
+ `UPDATE` - Updates or edits device information from the database table

### Command Details

`ADD`
========

The `ADD` command allows the user to add devices manually through multiple user inputs.

```bash
Please enter a command
add
Enter device property number.
B000010
Enter device manufacturer.
Dell
Enter device description.
Monitor
Enter calibration date.
01/02/2023
Enter calibration due date.
01/02/2024
Enter custodian email.
john_doe1337@gmail.com
Device added!
```

When adding devices manually, make sure of the following:
+ Property number is not a duplicate
+ Ensure proper date format. The software looks for MM/DD/YYYY.

`APPEND`
========

The `APPEND` command adds additional devices through an external csv file named additional data.csv.

When adding devices through the file, ensure the following:
+ additional_data.csv is in the same file directory as the software
+ Users may create a duplicate copy of calibration_data.csv and rename it as additional_data.csv.

`DELETE`
========

The `DELETE` command prompts the user for a device property number then proceeds to delete the entire row from the table.

```bash
Please enter a command.
delete
Enter the property number of the device you wish to delete.
```

The software will print an error if the property number is not found.

```bash
Error: Property number not found.
```

`DISPLAY`
========

The `DISPLAY` command prompts the user on which column the command will sort by. It will then display all data. For more specific searches, the `SELECT` command would be more suitable.

```bash
Please enter a command
display
Enter column you want to sort by. 
cal_due
('property_number', 'manufacturer', 'description', 'cal_date', 'cal_due', 'custodian_email')
('B000001', 'Highland Technologies', 'T680 Time Interval Counter', '01/02/2023', '01/01/2024', 'john_doe1337@gmail.com')
('B000005', 'Thorlabs', 'Optical Power Meter', '01/02/2023', '01/01/2024', 'john_doe1337@gmail.com')
('B000002', 'National Instruments', 'PXIe 5160 Oscilloscope', '03/02/2023', '03/02/2024', 'john_doe1337@gmail.com')
('B000004', 'Newport', 'Optical Detector', '07/01/2022', '07/01/2023', 'john_doe1337@gmail.com')
('B000003', 'Fluke', 'Digital Multi-meter', '08/03/2022', '08/03/2023', 'john_doe1337@gmail.com')
```

`REMIND`
========

The `REMIND` command scans the database table for upcoming calibration expiration. If the difference between the calibration due date and today's date is 60 days or less, the software will send an email reminder to the custodian.

The current email server used is gmail and for the purposes of this project, the email information is in an `env` file.

`REPLACE`
========

The `REPLACE` command replaces the contents of the device table with files in calibration_database.csv. This is useful for when the csv file is more up-to-date than the device table.

```bash
Please enter a command
replace
Data replaced!
```

`SELECT`
========

The `SELECT` command takes in an SQLite query. This is very useful for more specific and advanced searches. Since this command executes an SQLite query, it can also perform other SQLite functions but the software will not be able to display some of the results such as if one uses a query that deletes a row.

```bash
Please enter a command
SELECT
Enter sql query
SELECT * FROM devices WHERE custodian_email = 'john_doe1337@gmail.com' 
('B000001', 'Highland Technologies', 'T680 Time Interval Counter', '01/02/2023', '01/01/2024', 'john_doe1337@gmail.com')
('B000002', 'National Instruments', 'PXIe 5160 Oscilloscope', '03/02/2023', '03/02/2024', 'john_doe1337@gmail.com')
('B000003', 'Fluke', 'Digital Multi-meter', '08/03/2022', '08/03/2023', 'john_doe1337@gmail.com')
('B000004', 'Newport', 'Optical Detector', '07/01/2022', '07/01/2023', 'john_doe1337@gmail.com')
('B000005', 'Thorlabs', 'Optical Power Meter', '01/02/2023', '01/01/2024', 'john_doe1337@gmail.com')
```

For more syntax information, refer to the SQLite documentation https://www.sqlite.org/lang.html.

`UPDATE`
========

The `UPDATE` command prompts the user for a property number they wishes to update, they will then be prompted to enter the column, then finally the value they wish to update. An example is shown below.

```bash
('B000005', 'Thorlabs', 'Optical Power Meter', '01/02/2023', '01/01/2024', 'john_doe1337@gmail.com')
Please enter a command
update
Enter the property number of the device you wish to update. 
B000005
Enter the column you would like to update. 
custodian_email
Enter the new value. 
jane_doe1337@yahoo.com
Device updated!
Please enter a command
display               
Enter column you want to sort by. 
custodian_email
('property_number', 'manufacturer', 'description', 'cal_date', 'cal_due', 'custodian_email')
('B000005', 'Thorlabs', 'Optical Power Meter', '01/02/2023', '01/01/2024', 'jane_doe1337@yahoo.com')
```

### Special Thanks

I would like to thank my NCLab coach and the NCLab support team for their guidance and assistance during this python developer program. You are all awesome!