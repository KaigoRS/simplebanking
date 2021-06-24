import random
import sqlite3
from typing import List, Any


class Banking:
    details = {}
    card_numbers: list[Any] = []
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS card ('
                'id INTEGER,'
                'number TEXT,'
                'pin TEXT, '
                'balance INTEGER DEFAULT 0);')
    conn.commit()

    def __init__(self):
        self.IIN = 400000
        self.account_num = 000000000
        self.checksum = 0
        self.pin = '0000'
        self.card_num = str(self.IIN) + str(self.account_num) + str(self.checksum)
        self.balance = 0
        self.menu()

    def menu(self):
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')
        n = int(input())
        if n == 1:
            print()
            self.create_account()
        elif n == 2:
            print()
            self.log_account()
        elif n == 0:
            print()
            self.exit()
        else:
            print('Incorrect input')
            self.menu()

    def create_account(self):
        while True:
            self.account_num = str(random.randint(0, 10 ** 9 - 1))
            self.account_num = (9 - len(self.account_num)) * '0' + self.account_num
            self.card_num = str(self.IIN) + str(self.account_num) + str(self.checksum)
            self.checksum = self.make_checksum(self.card_num)
            self.card_num = str(self.IIN) + str(self.account_num) + str(self.checksum)
            if self.card_num not in self.card_numbers:
                self.card_numbers.append(self.card_num)
                break
            else:
                continue
        self.pin = str(random.randint(0, 10 ** 4 - 1))
        self.pin = (4 - len(self.pin)) * '0' + self.pin
        self.details[self.card_num] = [self.pin, self.balance]
        print('Your card number has been created')
        print('Your card number:')
        print(self.card_num)
        print('Your card PIN:')
        print(self.pin)
        print()
        self.cur.execute(f"INSERT INTO card (number, pin) VALUES ({self.card_num}, {self.pin})")
        self.conn.commit()
        self.menu()

    def make_checksum(self, number):
        number = number[:-1]
        number = [int(i) for i in number]
        number = [number[i - 1] if i % 2 == 0 else number[i - 1] * 2 for i in range(1, 16)]
        number = [number[i - 1] if number[i - 1] < 10 else number[i - 1] - 9 for i in range(1, 16)]
        count = sum(number)
        if count % 10 == 0:
            self.checksum = '0'
        else:
            self.checksum = str(10 - count % 10)
        return self.checksum

    def log_account(self):
        print('Enter your card number:')
        num = input()
        print('Enter your PIN:')
        pin = input()

        if num in self.card_numbers:

            cardnum = num
            digit_sum = 0

            for i, digit in enumerate(reversed(cardnum)):
                n = int(digit)
                if i % 2 == 0:
                    digit_sum += n
                elif n >= 5:
                    digit_sum += n * 2 - 9
                else:
                    digit_sum += n * 2
            if digit_sum % 10 == 0:
                if self.details[num][0] == pin:
                    print('You have successfully logged in!')
                    self.account_details(num)
                else:
                    print('Wrong card number or PIN!')
                    self.menu()
            else:
                print("Wrong card number or PIN!")
                self.menu()

        else:
            print('Wrong card number or PIN!')
            self.menu()

    def account_details(self, card_number):
        print()
        x = True
        while x:
            print('1. Balance')
            print('2. Add income')
            print('3. Do Transfer')
            print('4. Close account')
            print('5. Log out')
            print('0. Exit')
            n = int(input())
            if n == 1:
                print(f'Balance: {self.balance}')
                print()
                self.account_details(card_number)
            elif n == 2:
                self.add_income()
                print()
            elif n == 3:
                self.transfer_income(card_number)
                print()
            elif n == 4:
                self.close_account()
                print()
            elif n == 5:
                print('You have successfully logged out!')
                print()
                self.menu()
            elif n == 0:
                print()
                self.exit()
                x = 0

    def add_income(self):
        print("Enter how much money you want to add:")
        self.income = float(input())
        self.balance = self.balance + self.income
        self.cur.execute(f"UPDATE card SET balance = {self.balance}")
        self.conn.commit()
        print("Success!")

    def transfer_income(self, card_number):
        print("Enter card number:")
        num = input()
        self.cur.execute("SELECT number FROM card")
        result = self.cur.fetchall()
        final_result = [i[0] for i in result]

        cardnum = num
        digit_sum = 0

        for i, digit in enumerate(reversed(cardnum)):
            n = int(digit)
            if i % 2 == 0:
                digit_sum += n
            elif n >= 5:
                digit_sum += n * 2 - 9
            else:
                digit_sum += n * 2
        if digit_sum % 10 == 0:
            if num in final_result:
                print("Enter how much you want to transfer:")
                self.transfer = float(input())
                if self.transfer > self.balance:
                    print("Not enough money!")
                elif self.transfer <= self.balance:
                    self.balance = self.balance - self.transfer
                    print("Success!")
                    self.cur.execute(f"UPDATE card SET balance = {self.balance}")
                    self.conn.commit()
                    self.account_details(card_number)
            else:
                print('Such a card does not exist.')
                self.account_details(card_number)
        else:
            print("Probably you made a mistake in the card number. Please try again!")
            self.account_details(card_number)




    def close_account(self):
        self.cur.execute(f"DELETE FROM card WHERE number = {self.card_num}")
        self.conn.commit()
        print("The account has been closed!")

    def exit(self):
        print('Bye!')
        quit()

my_bank = Banking()
