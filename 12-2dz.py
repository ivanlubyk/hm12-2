from collections import UserDict
from datetime import datetime
import pickle


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, number):
        self.number = self.validate_phone(number)

    def __str__(self):
        return self.number

    def validate_phone(self, number):
        if not isinstance(number, str):
            raise ValueError("Phone number should be a string")
        if not number.isdigit():
            raise ValueError("Phone number should contain only digits")
        if len(number) != 12:
            raise ValueError("Phone number should have 10 digits")
        return number


class Birthday(Field):
    def __init__(self, value=None):
        self.value = self.validate_birthday(value)

    def __str__(self):
        return self.value.strftime('%Y-%m-%d')

    def validate_birthday(self, value):
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError("Birthday should be a string in the format of YYYY-MM-DD")
        try:
            birthday = datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Birthday should be a string in the format of YYYY-MM-DD")
        return birthday


class Record:
    def __init__(self, name, birthday=None):
        self.name = name
        self.phones = []
        self.birthday = birthday

    def add_phone(self, phone):
        if not isinstance(phone, Phone):
            phone = Phone(phone)
        self.phones.append(phone)

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, phone, new_phone):
        index = self.phones.index(phone)
        if not isinstance(new_phone, Phone):
            new_phone = Phone(new_phone)
        self.phones[index] = new_phone

    def __str__(self):
        return f"{str(self.name)}: {', '.join(str(phone) for phone in self.phones)}"

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        birthday = self.birthday.replace(year=today.year)
        if today > birthday:
            birthday = birthday.replace(year=today.year + 1)
        return (birthday - today).days

class AddressBook(UserDict):
    def __init__(self, filename):
        self.filename = filename
        try:
            with open(self.filename, 'rb') as f:
                data = pickle.load(f)
            self.data = data
        except FileNotFoundError:
            self.data = {}

    def add_record(self, record):
        self.data[str(record.name)] = record
        self.save()

    def remove_record(self, name):
        del self.data[str(name)]
        self.save()

    def serealization(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.data, f)

    def deserealization(self):
        with open(self.filename, 'rb') as f:
            data = pickle.load(f)
        self.data = data
  

    def find_record(self, query):
        result = []
        for record in self.data.values():
            if query.lower() in str(record).lower():
                result.append(record)
        return result

    def __iter__(self):
        self.index = 0
        self.keys_list = list(self.data.keys())
        return self

    def __next__(self):
        if self.index < len(self.keys_list):
            record = self.data[self.keys_list[self.index]]
            self.index += 1
            return record
        else:
            raise StopIteration

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            print(f"Invalid input: KeyError '{e.args[0]}'")
        except ValueError as e:
            print(f"Invalid input: ValueError '{e.args[0]}'")
        except IndexError as e:
            print(f"Invalid input: IndexError '{e.args[0]}'")

    return inner


@input_error
def add_contact():
    name_value = input("Enter name: ")
    name = Name(name_value)
    phone_value = input("Enter phone: ")
    phone = Phone(phone_value)
    record = Record(name)
    record.add_phone(phone)
    address_book.add_record(record)
    print(f"Contact {str(name)} with phone {str(phone)} has been added.")


@input_error
def change_contact():
    name_value = input("Enter name: ")
    name = Name(name_value)
    record = address_book.data.get(str(name))
    if not record:
        print("Contact not found.")
        return
    phone_value = input("Enter new phone: ")
    phone = Phone(phone_value)
    record.edit_phone(record.phones[0], phone)
    print(f"Phone for contact {str(name)} has been changed to {str(phone)}.")


@input_error
def show_phone():
    name_value = input("Enter name: ")
    name = Name(name_value)
    record = address_book.data.get(str(name))
    if not record:
        print("Contact not found.")
        return
    print(f"{str(name)}: {str(record.phones[0])}")


@input_error
def remove_contact():
    name_value = input("Enter name: ")
    name = Name(name_value)
    if str(name) in address_book.data:
        del address_book.data[str(name)]
        print(f"Contact {str(name)} has been removed.")
    else:
        print("Contact not found.")


@input_error
def give_me_all():
    query = input("Enter search term: ")
    records = address_book.find_record(query)
    if not records:
        print("No matching contacts found.")
        return

    record_count = len(records)
    while True:
        page_size = input(f"Enter page size (max {record_count}): ")
        try:
            page_size = int(page_size)
            if page_size > record_count:
                raise ValueError
            break
        except ValueError:
            print(f"Invalid input. Please enter a number between 1 and {record_count}.")
    page_count = (record_count - 1) // page_size + 1
    current_page = 1
    while True:
        start_index = (current_page - 1) * page_size
        end_index = min(start_index + page_size, record_count)
        print(f"Page {current_page}:")

        for i in range(start_index, end_index):
            print(records[i])
        if current_page == page_count:
            break
        user_input = input("Press Enter to continue, or 'q' to quit: ")
        if user_input == 'q':
            break
        current_page += 1


def handler(command):
    if command.startswith("add"):
        add_contact()
    elif command.startswith("change"):
        change_contact()
    elif command.startswith("phone"):
        show_phone()
    elif command.startswith("show all"):
        give_me_all()
    elif command.startswith("remove"):
        remove_contact()
    else:
        print("Input error: Invalid command. Please try again.")


bye = ["good bye", "close", "exit"]
hel = ["hi", "hello"]



address_book = AddressBook('addressbook.pickle')
def primitive_bot():
    while True:
        action = input(
            "Welcome app to start work enter <hello> or <hi>\nTo finish, enter > (good bye, close, exit):").lower()
        if action in hel:
            print(
                "How can I help you?\nThe following commands are available to you,\n(add, change, phone, remove, show all, exit)")
        elif action in bye:
            print("Good bye!")
            break
        else:
            handler(action)


if __name__ == "__main__":
    primitive_bot()