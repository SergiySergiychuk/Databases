from consolemenu import SelectionMenu

from model import Model
from view import View

TABLES_NAMES = ['author', 'book', 'author_book', 'visitor', 'season_ticket']
TABLES = {
    'author': ['id', 'fullname', 'birthday'],
    'book': ['id', 'name', 'year'],
    'author_book': ['id', 'author_id', 'book_id'],
    'visitor': ['id', 'fullname', 'birthday', 'id_season_ticket'],
    'season_ticket': ['id', 'name', 'price']
}


def get_input(msg, table_name=''):
    print(msg)
    if table_name:
        print(' | '.join(TABLES[table_name]), end='\n\n')
    return input()


def get_insert_input(msg, table_name):
    print(msg)

    print(' | '.join(TABLES[table_name]), end='\n\n')
    return input(), input()


def press_enter():
    input()


class Controller:

    def __init__(self):
        self.model = Model()
        self.view = View()
        self.model.set_data_to_db(1)
        self.model.test()

    def show_init_menu(self, msg=''):
        selection_menu = SelectionMenu(
            TABLES_NAMES + ['Fill table "book" by random data (10 items)'],
            title='Select the table to work with | command:', subtitle=msg)

        selection_menu.show()

        index = selection_menu.selected_option
        if index < len(TABLES_NAMES):
            table_name = TABLES_NAMES[index]
            self.show_entity_menu(table_name)
        elif index == 5:
            self.fill_by_random()
        else:
            print('Bye, have a beautiful day!')

    def show_entity_menu(self, table_name, msg=''):
        options = ['Get', 'Delete', 'Update', 'Insert']

        functions = [self.get, self.delete, self.update, self.insert]

        if table_name == 'author':
            options.append('Search book by author')
            functions.append(self.search_book_by_author)
        elif table_name == 'book':
            options.append('Search authors that wrote the book')
            functions.append(self.search_author_by_book)

        selection_menu = SelectionMenu(options, f'Name of table: {table_name}', exit_option_text='Back', subtitle=msg)
        selection_menu.show()
        try:
            function = functions[selection_menu.selected_option]
            function(table_name)
        except IndexError:
            self.show_init_menu()

    def get(self, table_name):
        try:
            condition = get_input(
                f'GET {table_name}\nEnter condition (SQL) or leave empty:', table_name)
            data = self.model.get(table_name, condition)
            self.view.print(data)
            press_enter()
            self.show_entity_menu(table_name)
        except Exception as err:
            self.show_entity_menu(table_name, str(err))

    def insert(self, table_name):
        try:

            columns, values = get_insert_input(
                f"INSERT {table_name}\nEnter columns divided with commas, then do the same for values in format: ['value1', 'value2', ...]",
                table_name)

            self.model.insert(table_name, columns, values)
            self.show_entity_menu(table_name, 'Insert is successful!')
        except Exception as err:
            self.show_entity_menu(table_name, str(err))

    def delete(self, table_name):
        try:
            condition = get_input(
                f'DELETE {table_name}\n Enter condition (SQL):', table_name)

            self.model.delete(table_name, condition)
            self.show_entity_menu(table_name, 'Delete is successful')
        except Exception as err:
            self.show_entity_menu(table_name, str(err))

    def update(self, table_name):
        try:
            condition = get_input(
                f'UPDATE {table_name}\nEnter condition (SQL):', table_name)

            statement = get_input(
                "Enter SQL statement in format [<key>='<value>']", table_name)

            self.model.update(table_name, condition, statement)
            self.show_entity_menu(table_name, 'Update is successful')
        except Exception as err:
            self.show_entity_menu(table_name, str(err))

    def search_book_by_author(self, table_name):
        try:
            author_id = get_input(
                'Search book by author\'s id are: \nEnter id divided with commas:')

            data = self.model.search_book_by_author(author_id)
            self.view.print(data)
            press_enter()
            self.show_entity_menu(table_name)
        except Exception as err:
            self.show_entity_menu(table_name, str(err))

    def search_author_by_book(self, table_name):
        try:
            book_id = get_input('Search authors that wrote the book.\nEnter book\'s id:')

            data = self.model.search_author_by_book(book_id)
            self.view.print(data)
            press_enter()
            self.show_entity_menu(table_name)
        except Exception as err:
            self.show_entity_menu(table_name, str(err))

    def fill_by_random(self):
        try:
            self.model.fill_book_by_random_data()

            self.show_init_menu('Generated successfully')

        except Exception as err:
            self.show_init_menu(str(err))
