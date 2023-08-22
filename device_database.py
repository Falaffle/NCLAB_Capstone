import pandas as pd
import sqlite3
import os
import ssl
import smtplib
from sqlite3 import Error
from datetime import datetime, date
from email.message import EmailMessage
from dotenv import load_dotenv, dotenv_values


class Cal_Database:
    """A program that manages a device calibration database."""

    def __init__(self):
        """Initiates Cal_Database"""

        self.conn = sqlite3.connect("device_database.db")
        self.cur = self.conn.cursor()
        self.devices = []
        self.property_numbers = []
        self.emails = []
        self.create_cal_table()
        self.generate_devices_list()
        self.generate_property_list()
        load_dotenv()
        # self.remind()

    def sql_execute(self, sqlquery='', message=''): #TESTED
        """Accepts SQLite string command then executes"""

        try:
            print(message)
            return self.cur.execute(sqlquery)

        except Exception and Error as e:
            print("Error: " + str(e))

    def sql_executemany(self, sqlquery='', device_list=[], message=''): #TESTED
        """Accepts SQLite parameters (sql string and list of tuples) then uses executemany"""

        try:
            print(message)
            return self.cur.executemany(sqlquery, device_list)

        except Exception and Error as e:
            print("Error: " + str(e))

    def create_cal_table(self, table_name='devices'): #TESTED
        """Creates a new calibration table named devices if table does not exist"""

        sqlquery = "CREATE TABLE IF NOT EXISTS " + table_name + " (property_number TEXT UNIQUE, manufacturer TEXT, description TEXT, cal_date TEXT, cal_due TEXT, custodian_email TEXT)"
        self.cur.execute(sqlquery)
        self.conn.commit()
        return sqlquery

    def generate_devices_list(self): #TESTED
        """Populates a complete device data list from the devices table"""

        self.devices.clear()
        sqlquery = "SELECT * FROM devices ORDER BY property_number"
        device_data = self.cur.execute(sqlquery)
        for row in device_data:
            self.devices.append(row)

        return self.devices

    def generate_property_list(self): #TESTED
        """Populates a property number list from the devices table"""

        self.property_numbers.clear()
        sqlquery = "SELECT * FROM devices ORDER BY property_number"
        device_data = self.cur.execute(sqlquery)
        for row in device_data:
            self.property_numbers.append(row[0])

        return self.property_numbers

    def pn_prompt(self): #TESTED
        """Prompts users for a property number"""

        finished = False
        while finished == False:
            prompt = input("Enter device property number.\n").strip()
            if prompt in self.property_numbers:
                finished = True
            else:
                print("Error: Property number does not exist")
        return prompt

    def pn_prompt_add(self): #TESTED
        """Prompts users for a property number for the add command"""

        finished = False
        while finished == False:
            prompt = input("Enter device property number.\n").strip()
            if prompt in self.property_numbers:
                print("Error: Property number already exists")
            else:
                finished = True
        return prompt

    def date_prompt(self): #TESTED
        """Prompts user for a calibration date"""

        finished = False
        while finished == False:
            try:
                prompt = input("Enter calibration date.\n").strip()
                datetime.strptime(prompt, "%m/%d/%Y").date()
                finished = True
            except ValueError or TypeError as e:
                print("Error: " + str(e))
        return prompt

    def due_prompt(self): #TESTED
        """Prompts user for a calibration due date"""

        finished = False
        while finished == False:
            try:
                prompt = input("Enter calibration due date.\n").strip()
                datetime.strptime(prompt, "%m/%d/%Y").date()
                finished = True
            except ValueError or TypeError as e:
                print("Error: " + str(e))
        return prompt

    def column_prompt(self): #TESTED
        """Prompts user for the table column"""

        column_dict = {
            "pn": "property_number",
            "mn": "manufacturer",
            "des": "description",
            "date": "cal_date",
            "due": "cal_due",
            "email": "custodian_email",
        }

        finished = False
        while finished == False:
            prompt = input("Enter column name.\n").lower().strip()
            if prompt in column_dict.values():
                finished = True
            elif prompt in column_dict.keys():
                prompt = column_dict[prompt]
                finished = True
            else:
                print("Error: Column name does not exist")
        print(prompt)
        return prompt

    def display_column_names(self): #TESTED
        """Displays the column names into the terminal"""

        sqlquery = "SELECT * FROM devices"
        column = self.cur.execute(sqlquery)
        column_names = tuple(map(lambda x: x[0], column.description))
        return column_names

    def display_data(self): #TESTED
        """Displays all data from the database table"""

        try:
            column_prompt = self.column_prompt()
            print(self.display_column_names())

            sqlquery = "SELECT * FROM devices ORDER BY " + column_prompt
            device_data = self.cur.execute(sqlquery)
            for row in device_data:
                print(row)

        except Error as e:
            print("Error: " + str(e))
            return e

    def select(self): #TESTED
        """Displays data using advanced SQL commands. Most useful for advanced SELECT searches. Refer to sqlite3 documentation for proper syntax."""

        try:
            sqlquery = input("Enter sql query\n").strip()
            data = self.cur.execute(sqlquery)
            for row in data:
                print(row)
        except Error as e:
            print("Error: " + str(e))
            return e

    def add_device(self): #TESTED
        """Adds a device to the database"""

        pn_prompt = self.pn_prompt_add()
        mn_prompt = input("Enter device manufacturer.\n").strip()
        des_prompt = input("Enter device description.\n").strip()
        date_prompt = self.date_prompt()
        due_prompt = self.due_prompt()
        email_prompt = input("Enter custodian email.\n").strip()

        new_device = [
            (
                pn_prompt,
                mn_prompt,
                des_prompt,
                date_prompt,
                due_prompt,
                email_prompt,
            )
        ]

        sqlquery = "INSERT INTO devices (property_number, manufacturer, description, cal_date, cal_due, custodian_email) VALUES (?, ?, ?, ?, ?, ?)"
        message = "Device added!"

        return sqlquery, new_device, message

    def append(self, table_name='devices'): #TESTED
        """Add devices from a csv file called additional_data.csv"""

        try:
            df = pd.read_csv("additional_data.csv")
            df.to_sql(table_name, self.conn, if_exists="append", index=False)
            message = "Devices added!"
            print(message)

        except Exception as e:
            print("Error: " + str(e))
            return e

    def replace(self, table_name='devices'): #TESTED
        """replaces data in the devices table with data from a csv file called calibration_data.csv"""

        try:
            df = pd.read_csv("calibration_data.csv")
            df.to_sql(table_name, self.conn, if_exists="replace", index=False)
            message = "Data replaced!"
            print(message)

        except Exception as e:
            print("Error: " + str(e))
            return e

    def delete_device(self): #TESTED
        """Given a property number, deletes a device from the database"""

        finished = False

        while not finished:
            pn = input(
                "Enter the property number of the device you wish to delete. \n"
            ).strip()

            if pn in self.property_numbers:
                sqlquery = "DELETE FROM devices WHERE property_number = '" + pn + "'"
                finished = True
            else:
                e = "Error: Property number not found."
                print(e)

        message = "Device deleted!"
        return sqlquery, message

    def update_device(self, table_name='devices'): #TESTED
        """Updates or edits device information from the database table"""

        finished = False

        while not finished:
            pn = self.pn_prompt()

            if pn in self.property_numbers:
                try:
                    col = self.column_prompt()

                    if col == "cal_date":
                        value = self.date_prompt()
                    elif col == "cal_due":
                        value = self.due_prompt()
                    else:
                        value = input("Enter the new value. \n").strip()

                    sqlquery = (
                        "UPDATE " + table_name + " SET "
                        + col
                        + " = '"
                        + value
                        + "' WHERE property_number = '"
                        + pn
                        + "'"
                    )
                    finished = True

                except Error as e:
                    print("Error: " + str(e))

            else:
                e = "Error: Property number not found."
                print(e)

        message = "Device updated!"
        return sqlquery, message

    def save_csv(self, table_name="devices", file_name="calibration_data.csv"): #TESTED
        """Saves the table content to a csv file named calibration_data.csv"""

        sqlquery = "SELECT * FROM " + table_name
        self.cur.execute(sqlquery)
        result = self.cur.fetchall()

        for row in result:
            df = pd.read_sql_query(sqlquery, self.conn)
            df.to_csv(file_name, index=False)

        message = "File saved!"
        print(message)

    def date_math(self, cal_due):
        """Computes the remaining days until calibration expiration"""

        try:
            x = date.today().strftime("%m/%d/%Y")
            x = datetime.strptime(x, "%m/%d/%Y").date()
            y = datetime.strptime(cal_due, "%m/%d/%Y").date()
            z = y - x

            return z.days

        except ValueError and TypeError as e:
            # "Error: Date not in the correct format (mm/dd/yyyy)"
            return e

    def generate_email_list(self): #TESTED
        """Adds into a list custodian email with expiring devices"""

        try:
            sqlquery = "SELECT * FROM devices ORDER BY property_number"
            device_data = self.cur.execute(sqlquery)
            for row in device_data:
                days = self.date_math(row[4])

                if days <= 60 and row[5] not in self.emails:
                    self.emails.append(row[5])

            return self.emails

        except ValueError and TypeError as e:
            # "Error: Date not in the correct format (mm/dd/yyyy)"
            return e

    def send_email_gmail(self, email_receiver):
        """Sends email reminders to custodians using gmail"""

        try:
            email_sender = os.getenv("EMAIL")
            email_password = os.getenv("PASSWORD")

            subject = "Calibration Reminder"
            body = "Greetings,\n\nOne or more of your devices need to be calibrated.\n\nThank you."

            em = EmailMessage()
            em["From"] = email_sender
            em["To"] = email_receiver
            em["subject"] = subject
            em.set_content(body)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())

            print("Reminders sent!")

        except Exception as e:
            print("Error: " + str(e) + " check .env file.")
            return e

    def remind(self):
        """Sends an email reminder to custodians with upcoming calibration expiration"""

        try:
            email_list = self.generate_email_list()
            if email_list != []:
                for i in email_list:
                    self.send_email_gmail(i)
            else:
                print("No upcoming device calibration required.")

        except ValueError and TypeError as e:
            print("Error: Date not in the correct format (mm/dd/yyyy)")
            return e

    def help(self):
        """Displays the commands and its description"""

        print("LIST OF COMMANDS\n")
        print("ADD - " + self.add.__doc__ + "\n")
        print("APPEND - " + self.append.__doc__ + "\n")
        print("DELETE - " + self.delete_device.__doc__ + "\n")
        print("DISPLAY - " + self.display_data.__doc__ + "\n")
        print("HELP - " + self.help.__doc__ + "\n")
        print("QUIT - Closes connection from the database and exits the program\n")
        print("REMIND - " + self.remind.__doc__ + "\n")
        print("REPLACE - " + self.replace.__doc__ + "\n")
        print("SAVE - " + self.save_csv.__doc__ + "\n")
        print("SELECT = " + self.select.__doc__ + "\n")
        print("UPDATE - " + self.update_device.__doc__ + "\n")

    def start(self):
        """The event loop"""

        # Event loop:
        finished = False
        while not finished:
            command = input("Please enter a command\n").lower().strip()

            if command == "quit":
                self.cur.close()
                self.conn.close()
                finished = True

            elif command == "add":
                sqlquery, new_device, message = self.add_device()
                self.sql_executemany(sqlquery, new_device, message)
                self.conn.commit()
                self.generate_devices_list()
                self.generate_property_list()

            elif command == "append":
                self.append()
                self.generate_devices_list()
                self.generate_property_list()

            elif command == "display":
                self.display_data()

            elif command == "delete":
                sqlquery, message = self.delete_device()
                self.sql_execute(sqlquery, message)
                self.conn.commit()
                self.generate_devices_list()
                self.generate_property_list()

            elif command == "update":
                sqlquery, message = self.update_device()
                self.sql_execute(sqlquery, message)
                self.conn.commit()
                self.generate_devices_list()
                self.generate_property_list()

            elif command == "remind":
                self.remind()

            elif command == "replace":
                self.replace()
                self.generate_devices_list()
                self.generate_property_list()

            elif command == "save":
                self.save_csv()

            elif command == "help":
                self.help()

            elif command == "list":
                self.generate_devices_list
                print(self.devices)
                self.generate_property_list
                print(self.property_numbers)

            elif command == "select":
                self.select()
                self.conn.commit()

            else:
                print("Error: Invalid command! Try again or type HELP.")


# Main program:
C = Cal_Database()
C.create_cal_table('test_devices')
C.start()
