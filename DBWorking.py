import sqlite3


path = r'C:\artem\forPyCharm\TelegramCountBot\DB\MainDB.db'


def create_table(name, user):
    con = sqlite3.connect(path)
    cur = con.cursor()

    cur.execute(f"INSERT INTO ChatIDs(id, Total) VALUES({name}, 0)")
    con.commit()
    name = str(name)
    cur.execute(f"""CREATE TABLE IF NOT EXISTS "{name}" (
                                        id INTEGER PRIMARY KEY,
                                        messages INTEGER
                    );""")
    con.commit()
    cur.execute(f'INSERT INTO "{name}"(id, messages) VALUES("{user}", 0)')
    con.commit()


def get_chats():
    con = sqlite3.connect(path)
    cur = con.cursor()

    temp = cur.execute("SELECT * FROM ChatIDs;").fetchall()

    ans = list()
    for i in temp:
        ans.append(i[0])
    return ans


def add_message(chat_id, user_id):
    con = sqlite3.connect(path)
    cur = con.cursor()

    temp = cur.execute(f"SELECT * FROM ChatIDs WHERE id = {chat_id};").fetchall()
    print(temp)
    cur.execute(f"UPDATE ChatIDs SET Total={temp[0][1] + 1} WHERE id={chat_id};")
    con.commit()

    temp = cur.execute(f'SELECT * FROM "{chat_id}" WHERE id = {user_id};').fetchall()
    print(temp)
    cur.execute(f'UPDATE "{chat_id}" SET messages={temp[0][1] + 1} WHERE id={user_id};')
    con.commit()


def get_total(chat_id):
    con = sqlite3.connect(path)
    cur = con.cursor()

    return cur.execute(f"SELECT * FROM ChatIDs WHERE id = {chat_id};").fetchall()[0][1]


def get_users(chat_id):
    con = sqlite3.connect(path)
    cur = con.cursor()

    temp = cur.execute(f'SELECT * FROM "{chat_id}";').fetchall()

    ans = list()
    for i in temp:
        ans.append(i[0])
    return ans


def get_users_full(chat_id):
    con = sqlite3.connect(path)
    cur = con.cursor()

    return cur.execute(f'SELECT * FROM "{chat_id}";').fetchall()


def new_user(chat_id, user_id):
    con = sqlite3.connect(path)
    cur = con.cursor()

    cur.execute(f'INSERT INTO "{chat_id}"(id, messages) VALUES("{user_id}", 1)')
    con.commit()