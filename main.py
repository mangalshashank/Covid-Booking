import hashlib
import sqlite3

conn = sqlite3.connect('covid.db')
cursor = conn.cursor()
while True:
    print("Welcome to the Covid Vaccination Booking System")
    print("Choose from the following options:")
    print("1. Admin")
    print("2. User")
    print("3. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        print("Welcome Admin")
        print("Enter your username and password to login")
        username = input("Enter your mail id: ")
        password = input("Enter your password: ")
        #password = hashlib.md5(password.encode()).hexdigest()
        cursor.execute("SELECT * FROM credentials WHERE mailid = ? AND password = ?", (username, password))
        admin = cursor.fetchone()
        if admin is None:
            print("Invalid username or password")
            exit()
        else:
            print("Login successful")
            print("---------------------")
            print("Welcome ", admin[2])
            print("---------------------")
            print("Choose from the following options:")
            print("1. Add a new vaccination center")
            print("2. View booking for a vaccination center")
            print("3. Delete a vaccination center")
            
            admin_choice = int(input("Enter your choice: "))

            if admin_choice == 1:
                print("Add a new vaccination center")
                center_name = input("Enter the name of the vaccination center: ")
                vaccines = int(input("Enter the number of vaccines available: "))
                address = input("Enter the address of the vaccination center: ")
                cursor.execute("INSERT INTO hospitals (availableSlots, hospitalName, hospitalAddress) VALUES (?, ?, ?)", (vaccines, center_name, address))
                conn.commit()
                print("Vaccination center added successfully\n")

            elif admin_choice == 2:
                print("View booking for a vaccination center")
                print("Available vaccination centers: ")
                cursor.execute("SELECT * FROM hospitals")
                for it in cursor.fetchall():
                    print("Hospital ID: ", it[0], "| Hospital Name: ", it[2], " | Vaccines available: ", it[1], " | Location: ", it[3])
                    cursor.execute("SELECT * FROM booking_table WHERE hospitalId = ?", (it[0],))
                    bookings = cursor.fetchall()
                    if len(bookings) == 0:
                        print("No bookings available")
                    else:
                        print("Bookings: ")
                        for it in bookings:
                            print("User mail: ", it[0])
                    print("-------------------------------------------------------------------------------------------------------------------------------------")
            elif admin_choice == 3:
                print("Delete a vaccination center")
                print("Available vaccination centers: ")
                cursor.execute("SELECT * FROM hospitals")
                for it in cursor.fetchall():
                    print("Hospital ID: ", it[0], "| Hospital Name: ", it[2], " | Vaccines available: ", it[1], " | Location: ", it[3])
                hospital_id = int(input("Enter hospital id to delete: "))
                cursor.execute("DELETE FROM hospitals WHERE hospitalId = ?", (hospital_id,))
                cursor.execute("DELETE FROM booking_table WHERE hospitalId = ?", (hospital_id,))
                conn.commit()
            else:
                print("Invalid choice")
    elif choice == 3:
        print("Exiting")
        exit()
    else:
        print("Welcome User")
        print("Sign up or login to continue")
        print("Choose from the following options:")
        print("1. Sign up (New user)")
        print("2. Login (Existing user)")
        print("3. Exit")
        user_choice = int(input("Enter your choice: "))
        if user_choice == 1:
            print("Sign up")
            print("Enter your details")
            mailid = input("Enter your mail id: ")
            password = input("Enter your password: ")
            #password = hashlib.md5(password.encode()).hexdigest()
            name = input("Enter your name: ")
            age = int(input("Enter your age: "))
            cursor.execute("INSERT INTO credentials VALUES (?, ?, ?, ?)", (mailid, password, name, age))
            conn.commit()
            print("Sign up successful")

        elif user_choice == 2:
            print("Login")
            print("Enter your mail id and password to login")
            mailid = input("Enter your mail id: ")
            password = input("Enter your password: ")
            #password = hashlib.md5(password.encode()).hexdigest()
            cursor.execute("SELECT * FROM credentials WHERE mailid = ? AND password = ?", (mailid, password))
            user = cursor.fetchone()
            if user is None:
                print("Invalid username or password")
                exit()
            else:
                print("Login successful")
                print("---------------------")
                print("Welcome ", user[2])
                print("age: ", user[3])
                print("---------------------")
                print("Choose from the following options:")
                print("1. search a vaccination slot")

                user_choice = int(input("Enter your choice: "))
                if user_choice == 1:
                    print("Available vaccination centers: ")
                    cursor.execute("SELECT * FROM hospitals")
                    for it in cursor.fetchall():
                        print("Hospital ID: ", it[0], "| Hospital Name: ", it[2], " | Vaccines available: ", it[1], " | Location: ", it[3])
                    
                    print("---------------------")
                    print("choose from the following options:")
                    print("1. Enter the hospital id to book a slot")
                    print("2. exit")
                    user_choice = int(input("Enter your choice: "))
                    if user_choice == 1:
                        hospital_id = int(input("Enter hospital id: "))
                        cursor.execute("SELECT * FROM hospitals WHERE hospitalId = ?", (hospital_id,))
                        hospital = cursor.fetchone()
                        if hospital is None:
                            print("Invalid hospital id")
                            exit()
                        else:
                            cursor.execute("SELECT * FROM booking_table WHERE hospitalId = ? AND user_mail = ?", (hospital_id, mailid))
                            booking = cursor.fetchone()
                            if booking is not None:
                                print("You have already booked a slot")
                                exit()
                            if hospital[1] == 0:
                                print("No vaccines available")
                                exit()
                            else:
                                print("Vaccination slot booked successfully")
                                cursor.execute("UPDATE hospitals SET availableSlots = availableSlots - 1 WHERE hospitalId = ?", (hospital_id,))
                                cursor.execute("INSERT INTO booking_table (user_mail,hospitalId) VALUES (?, ?)", ( mailid,hospital_id))
                                conn.commit()
                    else:
                        print("Exiting")
                else:
                    print("Invalid choice")