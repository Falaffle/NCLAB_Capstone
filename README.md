# Device Calibration Database

The capstone project for NCLAB python developer course. 

`Cal_Database` lets users add, delete, edit, and view a calibrated device database. Furthermore, it reminds custodians when their instruments are due for calibration.

Contents
========

 * [Overview](#Overview)
 * [Software Startup](#Startup)

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
Afterwards, simply run the software through the terminal.

```bash
$ python device_database.py
```