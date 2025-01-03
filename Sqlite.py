import sqlite3
from sqlite3 import Error


class SqlLiteHelper:
    def __init__(self, db_file):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file, check_same_thread=False)
        except Error as e:
            print(e)
        self.cursor = self.conn.cursor()
        self.create_base_tables()

    def create_base_tables(self):
        try:
            self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS "contesters" (
                    "id"    INTEGER NOT NULL UNIQUE,
                    "fullname"      TEXT NOT NULL,
                    "username"      TEXT DEFAULT '',
                    "role"  TEXT NOT NULL DEFAULT 'registration',
                    "is_confirmed"  INTEGER NOT NULL DEFAULT 0,
                    PRIMARY KEY("id")
                    )
                    ''')
            self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS "main_store" (
                    "id"    INTEGER NOT NULL,
                    "description"   TEXT NOT NULL,
                    "donor_id"      INTEGER NOT NULL,
                    "reciever_id"   INTEGER NOT NULL,
                    "is_pizdyl"     INTEGER NOT NULL DEFAULT 0,
                    "date"  TEXT NOT NULL,
                    FOREIGN KEY("donor_id") REFERENCES "contesters"("id"),
                    FOREIGN KEY("reciever_id") REFERENCES "contesters"("id"),
                    PRIMARY KEY("id" AUTOINCREMENT)
                    )
                    ''')
            self.cursor.execute(
                '''
                ALTER TABLE main_store ADD COLUMN meme_filepath TEXT DEFAULT NULL;
                '''
            )

        except Error as e:
            print(e)

    def add_contester(self, id: int, fullname: str, username: str):
        try:
            sql = '''
                INSERT OR IGNORE INTO contesters(id, fullname, username) VALUES (?,?,?) RETURNING id
                '''
            self.cursor.execute(sql, (id, fullname, username))
            try:
                result = next(self.cursor)
            except Exception:
                result = 0
            self.conn.commit()
            return result != 0
        except Error as e:
            print(e)

    def add_record(self, description: str, donor_id: int, reciever_id: int, date: str, record_type: str):
        try:
            if record_type == 'pizdyl':
                is_pizdyl = 1
            else:
                is_pizdyl = 0
            sql = '''
                INSERT INTO main_store(description,donor_id,reciever_id,date,is_pizdyl) VALUES (?,?,?,?,?)
                '''
            self.cursor.execute(sql, (description, donor_id, reciever_id, date, is_pizdyl))
            self.conn.commit()
        except Error as e:
            print(e)

    def get_pryanik(self, pryanik_id: int):
        try:
            sql = f'''
                SELECT DISTINCT 
                    m.description, 
                    cr.fullname, 
                    cr.username, 
                    cd.fullname, 
                    cd.username, 
                    m.is_pizdyl, 
                    cr.id, 
                    cd.id
                FROM main_store m
                JOIN contesters cr ON m.reciever_id = cr.id
                JOIN contesters cd ON m.donor_id = cd.id
                WHERE m.id = {pryanik_id}
                '''
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            if data:
                data = data[0]
            return {
                'description': data[0],
                'is_pizdyl': data[5],
                'receiver': {
                    'fullname': data[1],
                    'username': data[2],
                    'id': data[6],
                },
                'donor': {
                    'fullname': data[3],
                    'username': data[4],
                    'id': data[7],
                }
            }
        except Error as e:
            print(e)

    def get_all_pryanik_by_contester(self, contester_id, month: str, year: str):
        try:
            sql = f'''
                        SELECT 
                            m.description as description, 
                            cd.fullname as sender_fullname, 
                            cd.username as sender_username,
                            m.date as date,
                            m.is_pizdyl as pizdyl
                        FROM main_store m
                        JOIN contesters cd ON m.donor_id = cd.id
                        WHERE m.reciever_id = {contester_id}
                        AND m.date LIKE "{year}-{month}-%"
                    '''
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data
        except Error as e:
            print(e)

    def update_role(self, role: str, contester_id):
        try:
            sql = f'''
            UPDATE contesters 
            SET role = "{role}" 
            WHERE id = {contester_id}
            '''
            self.cursor.execute(sql)
            self.conn.commit()
            return
        except Error as e:
            print(e)

    def get_auth_data(self, contester_id):
        try:
            sql = f'''
            SELECT DISTINCT username, role, is_confirmed FROM contesters
            WHERE id = {contester_id}
            '''
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            if data:
                return {
                    'username': data[0][0],
                    'role': data[0][1],
                    'is_confirmed': data[0][2],
                }
            else:
                return None
        except Error as e:
            print(e)

    def confirm_contester(self, contester_id):
        try:
            sql = f'''
                    UPDATE contesters 
                    SET is_confirmed = 1 
                    WHERE id = {contester_id}
                    '''
            self.cursor.execute(sql)
            self.conn.commit()
        except Error as e:
            print(e)

    def get_stat(self, month: str, year: str):
        try:
            sql = f'''
                SELECT 
                    c.id,
                    c.fullname,
                    (count(m.id)-sum(m.is_pizdyl) * 2) AS count,
                    c.username as username
                FROM main_store m
                JOIN contesters c ON m.reciever_id = c.id
                WHERE m.date LIKE "{year}-{month}-%" AND c.is_confirmed = 1
                GROUP BY c.fullname
                ORDER BY count DESC
                '''

            self.cursor.execute(sql)
            data = self.cursor.fetchall()

            result = list()
            place_num = 1
            for row in data:
                result.append(
                    {
                        'place': place_num,
                        'contester_id': row[0],
                        'fullname': row[1],
                        'count': row[2],
                        'username': row[3],
                    }
                )
                place_num += 1
            return result
        except Error as e:
            print(e)

    def get_user_memes(self, user_id: str, month: str, year: str):
        try:
            sql = f'''
                SELECT 
                    description as description,
                    meme_filepath AS meme_filepath
                FROM main_store
                WHERE date LIKE "{year}-{month}-%" AND reciever_id = {user_id}
            '''

            self.cursor.execute(sql)
            data = self.cursor.fetchall()

            result = list()
            for row in data:
                if row[1] is not None:
                    result.append(
                        {
                            'description': row[0],
                            'meme_filepath': row[1]
                        }
                    )
                else:
                    continue
            return result
        except Error as e:
            print(e)

    def get_all_contesters_except_one(self, caller_id: int):
        try:
            sql = f'''
            SELECT id, fullname FROM contesters 
            WHERE id <> {caller_id}
            AND (role = 'contester' OR role = 'ultimate_contester')
            AND is_confirmed = 1
            '''
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return [{'id': row[0], 'fullname': row[1]} for row in data]
        except Error as e:
            print(e)

    def add_description_to_last_record(self, contester_id, text, meme_filepath=None):
        try:
            if meme_filepath is not None:
                set_condition = f'''
                    description = "{str(text).replace('"', ",,")}",
                    meme_filepath = "{str(meme_filepath)}"
                    '''
            else:
                set_condition = f'''
                    description = "{str(text).replace('"', ",,")}"
                    '''

            sql = f'''
                UPDATE main_store
                SET {set_condition}
                WHERE donor_id = {contester_id} AND description = "no_data"
                RETURNING *
                '''
            self.cursor.execute(sql)
            result = next(self.cursor)
            self.conn.commit()
            return result[0]
        except Error as e:
            print(e)

    def get_sended_pryaniks_in_this_month(self, month: str, year: str, contester_id: str):
        try:
            sql = f'''
                SELECT 
                    m.description as description, 
                    cd.fullname as receiver_fullname, 
                    cd.username as receiver_username,
                    m.date as date,
                    m.is_pizdyl as pizdyl
                FROM main_store m
                JOIN contesters cd ON m.reciever_id = cd.id
                WHERE m.donor_id = {contester_id}
                AND m.date LIKE "{year}-{month}-%"
            '''
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data
        except Error as e:
            print(e)

    def change_user_fullname(self, contester_id, new_fullname):
        try:
            sql = f'''
                UPDATE contesters
                SET fullname = "{new_fullname}"
                WHERE id = {contester_id}
                '''
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except Error as e:
            print(e)
            return False

    def soft_delete_user(self, user_id, action):
        value = '0' if action == "delete" else '1'
        try:
            sql = f'''
                UPDATE contesters
                SET is_confirmed = {value}
                WHERE id = {user_id}
                '''
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except Error as e:
            print(e)
            return False

    def get_all_users_except_one(self, caller_id: int):
        try:
            sql = f'''
            SELECT id, fullname FROM contesters 
            WHERE id <> {caller_id}
            AND is_confirmed = 1
            '''
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return [{'id': row[0], 'fullname': row[1]} for row in data]
        except Error as e:
            print(e)

    def get_all_soft_delete_users(self, caller_id: int):
        try:
            sql = f'''
            SELECT id, fullname FROM contesters 
            WHERE id <> {caller_id}
            AND is_confirmed = 0
            '''
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return [{'id': row[0], 'fullname': row[1]} for row in data]
        except Error as e:
            print(e)

    def add_multipryanic(self, description: str, donor_id: int, reciever_id: int, date: str, count: int):
        try:
            is_pyzdyl = 0
            count_insert = count
            if (count_insert < 0):
                is_pyzdyl = 1
                count_insert = abs(count)

            all_data = [
                (description + f"-{pryanik_num}", donor_id, reciever_id, date, is_pyzdyl) for pryanik_num in range(1, int(count_insert) + 1)
            ]
            sql = 'INSERT INTO main_store(description,donor_id,reciever_id,date,is_pizdyl) VALUES (?,?,?,?,?)'
            self.cursor.executemany(sql, all_data)
            self.conn.commit()
            return True
        except Error as e:
            print(e)
            return False

    def get_user_data_by_username(self, contester_username):
        try:
            sql = f'''
            SELECT DISTINCT id, fullname FROM contesters
            WHERE username = '{contester_username}'
            '''
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            if data:
                return {
                    'id': data[0][0],
                    'fullname': data[0][1],
                }
            else:
                return None
        except Error as e:
            print(e)

    def update_username_for_existing_user(self, contester_id, username):
        try:
            sql = f'''
                       UPDATE contesters 
                       SET username = "{username}" 
                       WHERE id = {contester_id}
                       '''
            self.cursor.execute(sql)
            self.conn.commit()
            return
        except Error as e:
            print(e)
