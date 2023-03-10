import pickle
import datetime
import uuid

class BankAccount:
    def __init__(self, user, balance=0):
        self.user = user
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return amount
        else:
            raise Exception("Insufficient balance.")

class Passenger:
    def __init__(self, name, bank_account):
        self.name = name
        self.bank_account = bank_account
        self.id = uuid.uuid4().hex # A unique ID generated by the program

class MetroCard:
    def __init__(self, user, balance=0):
        self.user = user
        self.balance = balance

    def charge(self, amount):
        self.balance += amount

    def deduct(self, amount):
        self.balance -= amount

class Trip:
    def __init__(self, fare, start_time, end_time):
        self.fare = fare
        self.start_time = start_time
        self.end_time = end_time
        self.is_active = True

    def deactivate(self):
        self.is_active = False

class SingleTable(MetroCard):
    def __init__(self, user):
        super().__init__(user)
        self.is_used = False

    def use(self, fare, start_time, end_time):
        if not self.is_used:
            self.is_used = True
            return Trip(fare, start_time, end_time)
        else:
            raise Exception("This card has already been used.")

class Credit(MetroCard):
    def use(self, fare, start_time, end_time):
        if self.balance >= fare:
            self.deduct(fare)
            return Trip(fare, start_time, end_time)
        else:
            raise Exception("Insufficient balance.")

class Term(MetroCard):
    def __init__(self, user, expiry_date):
        super().__init__(user)
        self.expiry_date = expiry_date

    def use(self, fare, start_time, end_time):
        if self.expiry_date > datetime.datetime.now().date():
            if self.balance >= fare:
                self.deduct(fare)
                return Trip(fare, start_time, end_time)
            else:
                raise Exception("Insufficient balance.")
        else:
            raise Exception("This card has expired.")

class Passenger:
    def __init__(self, name, bank_account):
        self.name = name
        self.id = self.generate_id()
        self.bank_account = bank_account

    @staticmethod
    def generate_id(cls):
        return hashlib.sha256(str(datetime.datetime.now().timestamp()).encode()).hexdigest()
        
    def show_id(self):
        print(f"Your unique ID is: {self.id}")

    def create_passenger(name):
        bank_account = BankAccount(name)
        passenger = Passenger(name, bank_account)
        with open("users.pickle", "ab") as f:
            pickle.dump(passenger, f)
        print("Passenger created successfully!")
        passenger.show_id()
        return passenger

def bank_account_management(user):
    print("Welcome to the bank account management system")
    print("1. Withdraw")
    print("2. Deposit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        amount = int(input("Enter the amount you want to withdraw: "))
        try:
            user.bank_account.withdraw(amount)
            print(f"{amount} has been withdrawn from your account.")
        except Exception as e:
            print(e)
    elif choice == 2:
        amount = int(input("Enter the amount you want to deposit: "))
        user.bank_account.deposit(amount)
        print(f"{amount} has been deposited to your account.")
    else:
        print("Invalid choice. Please try again.")

def metro_card_management(user):
    print("Welcome to the metro card management system")
    print("1. Credit card")
    print("2. Single-use card")
    print("3. Term card")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        user.metro_card = Credit(user)
        print("A credit card has been added to your account.")
    elif choice == 2:
        user.metro_card = SingleTable(user)
        print("A single-use card has been added to your account.")
    elif choice == 3:
        expiry_date = input("Enter the expiry date (YYYY-MM-DD): ")
        user.metro_card = Term(user, expiry_date)
        print("A term card has been added to your account.")
    else:
        print("Invalid choice. Please try again.")

def metro_travel_registration(user):
    if not hasattr(user, "metro_card"):
        print("You need to have a metro card to register for a trip.")
        return
    fare = int(input("Enter the fare: "))
    start_time = input("Enter the start time (YYYY-MM-DD HH:MM:SS): ")
    end_time = input("Enter the end time (YYYY-MM-DD HH:MM:SS): ")
    try:
        trip = user.metro_card.use(fare, start_time, end_time)
        print("Trip registered successfully.")
    except Exception as e:
        print(e)

def view_trips(trips):
    for i, trip in enumerate(trips):
        print(f"{i + 1}. {trip.start_time} to {trip.end_time}")
def edit_trip(trips, trip_number, user):
    if trip_number > len(trips) or trip_number < 1:
        print("Invalid trip number.")
        return
    trip = trips[trip_number - 1]
    if not trip.is_active:
        print("This trip has already been deactivated.")
        return
    print("1. Deactivate trip")

def login_as_admin():
    admin_id = input("Enter the administrator ID: ")
    admin_password = input("Enter the password: ")
    if admin_id == "admin" and admin_password == "admin123":
        return control_menu()
    else:
        print("Incorrect ID or password.")
        return main_menu()
def control_menu():
    print("\nWelcome to the Control Menu\n")
    print("1. Register a metro trip")
    print("2. Edit a registered trip")
    print("3. Return to Main Menu")
    choice = input("Enter your choice: ")

    if choice == "1":    # Register a metro trip
        pass
    elif choice == "2":    # Edit a registered trip
        pass
    elif choice == "3":    # Return to Main Menu
        return main_menu()
    else:
        print("Invalid option. Please try again.")
        return control_menu()
def main_menu():
    print("\nWelcome to the Main Menu\n")
    print("1. User Registration")
    print("2. Bank Account Management")
    print("3. Metro Travel Registration")
    print("4. Control Menu (Administrator Login)")
    print("5. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":       # User Registration
        name = input("Enter your name: ")
        create_passenger(name)
        return main_menu()
    elif choice == "2":     # Bank Account Management
        pass
    elif choice == "3":     # Metro Travel Registration
        pass
    elif choice == "4":     # Control Menu (Administrator Login)
        return login_as_admin()
    elif choice == "5":     # Exit
        print("Thank you for using our program.")
        exit()
    else:
        print("Invalid option. Please try again.")
        return main_menu()

if __name__ == '__main__':
    main_menu()



#
# import pickle
# from datetime import datetime, timedelta
#
# class Trip:
#     def __init__(self, start_time, end_time, cost):
#         self.start_time = start_time
#         self.end_time = end_time
#         self.cost = cost
#         self.is_active = True
#
#     def __repr__(self):
#         return f"Start Time: {self.start_time} - End Time: {self.end_time} - Cost: {self.cost} - Active: {self.is_active}"
#
# class Card:
#     def __init__(self, owner, card_type):
#         self.owner = owner
#         self.card_type = card_type
#         self.balance = 0
#         self.validity = None
#         self.expiry_date = None
#
#     def __repr__(self):
#         return f"{self.owner} - {self.card_type} - Balance: {self.balance} - Validity: {self.validity} - Expiry Date: {self.expiry_date}"
#
# class SingleTripCard(Card):
#     def __init__(self, owner):
#         super().__init__(owner, "Single Trip")
#         self.validity = 1
#
#     def use(self, trip):
#         if self.validity == 0:
#             print("This card has already been used.")
#         else:
#             print("Using single trip card.")
#             self.validity -= 1
#             trip.is_active = False
#
# class CreditCard(Card):
#     def __init__(self, owner, balance):
#         super().__init__(owner, "Credit")
#         self.balance = balance
#         self.validity = float('inf')
#
#     def use(self, trip, fare):
#         if self.balance >= fare:
#             print("Using credit card.")
#             self.balance -= fare
#             trip.is_active = False
#         else:
#             print("Insufficient balance.")
#
# class TermCard(Card):
#     def __init__(self, owner, validity, expiry_date):
#         super().__init__(owner, "Term")
#         self.validity = validity
#         self.expiry_date = expiry_date
#
#     def use(self, trip):
#         if self.validity == 0:
#             print("This card has expired.")
#         elif datetime.now() > self.expiry_date:
#             print("This card has expired.")
#         else:
#             print("Using term card.")
#             self.validity -= 1
#             trip.is_active = False
#
# def save_cards(cards):
#     with open("cards.pickle", "wb") as f:
#         pickle.dump(cards, f)
#
# def load_cards():
#     with open("cards.pickle", "rb") as f:
#         return pickle.load(f)
#
# # Example usage
#
# # Create cards
# card1 = SingleTripCard("User 1")
# card2 = CreditCard("User 2", 20)
# card3 = TermCard("User 3", 10, datetime.now() + timedelta(days=7))
#
# # Save cards

