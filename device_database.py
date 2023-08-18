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

    def create_cal_table(self):
        """Creates a new calibration table named devices if table does not exist"""

        sqlquery = "CREATE TABLE IF NOT EXISTS devices (property_number TEXT UNIQUE, manufacturer TEXT, description TEXT, cal_date TEXT, cal_due TEXT, custodian_email TEXT)"
        self.cur.execute(sqlquery)
        self.conn.commit()

    def generate_devices_list(self):
        """Populates a complete device data list from the devices table"""

        self.devices.clear()
        sqlquery = "SELECT * FROM devices ORDER BY property_number"
        device_data = self.cur.execute(sqlquery)
        for row in device_data:
            self.devices.append(row)

        return self.devices

    def generate_property_list(self):
        """Populates a property number list from the devices table"""

        self.property_numbers.clear()
        sqlquery = "SELECT * FROM devices ORDER BY property_number"
        device_data = self.cur.execute(sqlquery)
        for row in device_data:
            self.property_numbers.append(row[0])

        return self.property_numbers

    def pn_prompt(self):
        """Prompts users for a property number"""

        finished = False
        while finished == False:
            prompt = input("Enter device property number.\n").strip()
            if prompt in self.property_numbers:
                finished = True
            else:
                print("Error: Property number does not exist")
        return prompt
    
    def pn_prompt_add(self):
        """Prompts users for a property number for the add command"""

        finished = False
        while finished == False:
            prompt = input("Enter device property number.\n").strip()
            if prompt in self.property_numbers:
                print("Error: Property number already exists")
            else:
                finished = True
        return prompt

    def date_prompt(self):
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

    def due_prompt(self):
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

    def display_column_names(self):
        """Displays the column names into the terminal"""

        sqlquery = "SELECT * FROM devices"
        column = self.cur.execute(sqlquery)
        column_names = tuple(map(lambda x: x[0], column.description))
        return column_names

    def display_data(self):
        """Displays all data from the database table"""

        try:
            column_prompt = input("Enter column you want to sort by. \n").strip()

            print(self.display_column_names())

            sqlquery = "SELECT * FROM devices ORDER BY " + column_prompt
            device_data = self.cur.execute(sqlquery)
            for row in device_data:
                print(row)

        except Error as e:
            print("Error: " + str(e))
            return e

    def select(self):
        """Displays data using advanced SQL commands. Most useful for advanced SELECT searches. Refer to sqlite3 documentation for proper syntax."""

        try:
            sqlquery = input("Enter sql query\n").strip()
            data = self.cur.execute(sqlquery)
            for row in data:
                print(row)
            self.conn.commit()
        except Error as e:
            print("Error: " + str(e))
            return e

    def add_device(self):
        """Adds a device to the database"""

        try:
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
            self.cur.executemany(sqlquery, new_device)
            self.conn.commit()

            self.devices.append(new_device[0])
            self.property_numbers.append(pn_prompt)

            print("Device added!")
            return new_device

        except Error as e:
            print("Error: " + str(e))
            return e

    def add_from_file(self):
        """Add devices from a csv file called additional_data.csv"""

        try:
            df = pd.read_csv("additional_data.csv")

            df.to_sql("devices", self.conn, if_exists="append", index=False)

            self.generate_property_list()

            print("Devices added!")
            return True

        except Exception as e:
            print("Error: " + str(e))
            return e

    def add(self):
        """Add devices via user input or external csv file"""

        prompt = input("Add from file? Y/N \n").lower().strip()

        if prompt == "y":
            self.add_from_file()

        elif prompt == "n":
            self.add_device()

        else:
            print("Error: Invalid entry")
            return False

    def replace(self):
        """replaces data in the devices table with data from a csv file called calibration_data.csv"""

        try:
            df = pd.read_csv("calibration_data.csv")

            df.to_sql("devices", self.conn, if_exists="replace", index=False)

            self.generate_property_list()

            print("Data replaced!")
            return True

        except Exception as e:
            print("Error: " + str(e))
            return e

    def delete_device(self):
        """Given a property number, deletes a device from the database"""

        pn = input("Enter the property number of the device you wish to delete. \n").strip()

        if pn in self.property_numbers:
            sqlquery = "DELETE FROM devices WHERE property_number = '" + pn + "'"
            self.cur.execute(sqlquery)
            self.conn.commit()
            self.generate_devices_list()
            self.property_numbers.remove(pn)
            print("Device deleted!")

        else:
            e = "Error: Property number not found."
            print(e)
            return e

    def update_device(self):
        """Updates or edits device information from the database table"""

        pn = input("Enter the property number of the device you wish to update. \n").strip()

        if pn in self.property_numbers:
            try:
                col = input("Enter the column you would like to update. \n").lower().strip()
                
                if col == "cal_date":
                    value = self.date_prompt()
                elif col == "cal_due":
                    value = self.due_prompt()
                else:
                    value = input("Enter the new value. \n").strip()

                sqlquery = "UPDATE devices SET " + col + " = '" + value + "' WHERE property_number = '" + pn + "'"
                self.cur.execute(sqlquery)
                self.conn.commit()

                self.generate_property_list()
                print("Device updated!")

                return True
            
            except Error as e:
                print("Error: " + str(e))
                return e

        else:
            e = "Error: Property number not found."
            print(e)
            return e

    def save_csv(self):
        """Saves the table content to a csv file named calibration_data.csv"""

        sqlquery = "SELECT * FROM devices"
        self.cur.execute(sqlquery)
        result = self.cur.fetchall()

        for row in result:
            df = pd.read_sql_query(sqlquery, self.conn)
            df.to_csv("calibration_data.csv", index=False)

        print("File saved!")

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

    def generate_email_list(self):
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
                self.add()

            elif command == "display":
                self.display_data()

            elif command == "delete":
                self.delete_device()

            elif command == "update":
                self.update_device()

            elif command == "remind":
                self.remind()

            elif command == "replace":
                self.replace()

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

            else:
                print("Error: Invalid command! Try again or type HELP.")


# Main program:
C = Cal_Database()
C.start()
