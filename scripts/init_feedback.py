import sqlite3

def create_feedback_table():
    connection = sqlite3.connect('restaurant.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(item_id) REFERENCES menu_items(id)
        )
    ''')
    connection.commit()
    connection.close()

if __name__ == '__main__':
    create_feedback_table()
