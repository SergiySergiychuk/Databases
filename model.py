import psycopg2


class Model:

    def __init__(self):
        try:
            self.connection = psycopg2.connect(dbname='postgres', user='postgres',
                                               password='1', host='localhost')
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.Error) as error:
            print("Error during connection to PostgreSQL", error)

    def test(self):
        print(self.cursor.description)

    def get_col_names(self):
        return [d[0] for d in self.cursor.description]

    def set_data_to_db(self, reset):
        if reset:
            f = open("db.txt", "r")
            self.cursor.execute(f.read())
            self.connection.commit()

    def get(self, t_name, condition):
        try:
            query = f'SELECT * FROM {t_name}'

            if condition:
                query += ' WHERE ' + condition

            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def insert(self, t_name, columns, values):
        try:
            query = f'INSERT INTO {t_name} ({columns}) VALUES ({values});'

            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def delete(self, t_name, condition):
        try:
            query = f'DELETE FROM {t_name} WHERE {condition};'

            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def update(self, t_name, condition, statement):
        try:
            query = f'UPDATE {t_name} SET {statement} WHERE {condition}'

            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def search_book_by_author(self, author_id):
        try:

            query = f'''
            SELECT * from book
            WHERE id in(
                SELECT book_id FROM author_book
                WHERE author_id =  {author_id}
            );'''
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def search_author_by_book(self, book_id):

        try:
            query = f'''
                    SELECT * from author
                    WHERE id in(
                        SELECT author_id FROM author_book
                        WHERE book_id =  {book_id}
                        );'''
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def fill_book_by_random_data(self):
        sql = """
        CREATE OR REPLACE FUNCTION randomDepartments()
            RETURNS void AS $$
        DECLARE
            step integer  := 0;
        BEGIN
            LOOP EXIT WHEN step > 10;
                INSERT INTO book (name, year)
                VALUES (
                    substring(md5(random()::text), 1, 10),
                    (random() * (2000 - 1800) + 1800)::integer
                );
                step := step + 1;
            END LOOP ;
        END;
        $$ LANGUAGE PLPGSQL;
        SELECT randomDepartments();
        """
        try:
            self.cursor.execute(sql)
        finally:
            self.connection.commit()






