# Device Calibration Database

The capstone project for NCLAB python developer course. 

`Cal_Database` lets users add, delete, edit, and view a calibrated device database. Furthermore, it reminds custodians when their instruments are due for calibration.

Contents
========

 * [Overview](#Overview)
 * [Software Startup](#Startup)
 * [Initialization](#Initialization)
 * [Table Columns](#Table Columns)
 * [Event Loop](#Event Loop)
 * [Event Commands] (#Commands)

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

### Table Columns

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

### Event Commands