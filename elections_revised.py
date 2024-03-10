# Import Statements
import sqlite3
import matplotlib.pyplot as plt
from colorama import Fore, Back, Style

# connect to elections database
conn = sqlite3.connect('ELECTIONS.db')
c = conn.cursor()

# create tables to store user creds
c.execute('''CREATE TABLE IF NOT EXISTS Player_Panel (
    PLAYER_ID int,
    USERNAME text,
    PASSWORD text,
    RESIDENCY text,
    STATUS text
    )''')
c.execute('''CREATE TABLE IF NOT EXISTS EO_Panel (
    USERNAME text,
    PASSWORD text
    )''')
c.execute('''CREATE TABLE IF NOT EXISTS Admin_Panel (
    USERNAME text,
    PASSWORD text
    )''')
conn.commit()


# fucntion to allow players to login to the elections system
def player_login():
    while True: # loop for multiple password attempts
        username_input = input("Enter Your Username : ")

        try:
            c = conn.cursor()
            c.execute('SELECT password FROM Student_Panel WHERE username = ? ', username_input)
            found_password = c.fetchone()[0]
            conn.commit()

        except:
            print(Fore.RED + '')
            print(Back.BLACK + '')
            print(Style.BRIGHT + " \n                              There is no user found with this user name ,\n                          Please Signup Before You Login  \n")
            print(Style.RESET_ALL + " ")
            return None
        
        for password_attempts in range(5):
            password = input("Enter Your Password : ")
            
            if password_checkpoint != password and password_attempts == 4:
                print(Fore.RED + '')
                print(Back.BLACK + '')
                print(Style.BRIGHT + "                   You Can't Vote Temporarily. Please Contact An Admin To Reset Your Account\n ")
                print(Style.RESET_ALL + " ")

                c = conn.cursor()
                c.execute("UPDATE Player_Panel set STATUS = 'locked_out' WHERE USERNAME = ?", username_input)
                return None

            
            elif password_checkpoint != password:
                print("Wrong password. Please enter the correct password.")
                wrong_password_flag = input("Do You To Continue y/n : ")
                if wrong_password_flag == 'y':
                    continue
                else:
                    return None
            else:
                print(Fore.GREEN + '')
                print(Back.BLACK + '')
                print(Style.BRIGHT + "                                 ########## Player Panel Login Successful ##########\n ")
                print(Style.RESET_ALL + " ")
                break
        
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM Elections")
            current_elections = c.fetchall()
            conn.commit()

            total = 0
            for row in c:
                total = total + 1
            
            print(Fore.GREEN + '')
            print(Back.BLACK + '')
            print(Style.BRIGHT + "                                There Are Currently {total} Elections Open.\n ")
            print(Style.RESET_ALL + " ")
            elections = total
            
        except:
            print(Fore.RED+ '')
            print(Back.BLACK + '')
            print(Style.BRIGHT + "                                 Currently There Is No Election In Progress\n ")
            print(Style.RESET_ALL + " ")
            return None

        

        
