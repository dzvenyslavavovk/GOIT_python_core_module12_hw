from contacts_book_classes import contacts, Record

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'Wrong name'
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return 'Pls print: name and number'
        except TypeError:
            return 'Wrong command.'
    return inner

def hello():
    return 'How can I help you?'

@input_error
def add(contact):
    name, phones = split_info(contact)
    if name in contacts:
        raise ValueError('This contact already exists.')
    record = Record(name)
    for phone in phones:
        record.add_phone(phone)   
    contacts.add_record(record)
    return f'Number {phone} with name {name} was added.'

@input_error
def change(contact):
    name, phone = split_info(contact)
    record = contacts[name]
    record.change_phones(phone)
    return f'Number {phone} with name {name} was changed.'


@input_error
def show_phone(contact):
    search_records = ''
    records = contacts.search(contact.strip())

    for record in records:
        search_records += f"{record.get_info()}\n"
    return search_records   

def show_all():
    all_contacts = ''
    page_number = 1

    for page in contacts.iterator():
        all_contacts += f'Page #{page_number}\n'

        for record in page:
            all_contacts += f'{record.get_info()}\n'
        page_number += 1
    return all_contacts


@input_error
def delete_contact(name):
    name = name.strip()
    contacts.remove_record(name)
    return "The contact was deleted."

def bye():
    return 'Good bye!'


@input_error
def add_birthday(data):
    name,  birthday = data.strip().split()
    record = contacts[name]
    record.add_birthday(birthday)
    return f'Birthday {birthday} for {name} was added'

@input_error
def days_to_next_birthday(name):
    name = name.strip()
    record = contacts[name]
    return f"{name} birthday will be in {record.get_days_to_birthday()} day(s)."

def unknown_action():
    return 'Such command is not available'

COMMANDS = {
    'hello': hello,
    'add': add,
    'change': change,
    'phone': show_phone,
    'show all': show_all,
    'delete': delete_contact,
    'good bye': bye,
    'exit': bye,
    'close': bye,
    '.':bye,
    'birthday': add_birthday,
    'days_to_birthday': days_to_next_birthday
    }

def change_input(user_input):
    new_input = user_input
    data = ''
    for key in COMMANDS:
        if user_input.strip().lower().startswith(key):
            new_input = key
            data = user_input[len(new_input):]
            break
    if data:
        return reaction_func(new_input)(data)
    return reaction_func(new_input)()


def reaction_func(reaction):
    return COMMANDS.get(reaction, unknown_action)

def split_info(data):
    name, *phones = data.strip().split(' ')

    if name.isnumeric():
        raise ValueError('Wrong name.')
    for phone in phones:
        if not phone.isnumeric():
            raise ValueError('Wrong phones.')
    return name, phones


def main():
    print('Input one of the commands from the COMANDS dictionary.')
    print('To stop the bot, input good bye, close, exit or .')
    try:
        while True:

            user_input = input('Input command: ')
            result = change_input(user_input)
            print(result)
            if result=='Good bye!':
                exit()
    finally:
        contacts.save_contacts_to_file()

main()
