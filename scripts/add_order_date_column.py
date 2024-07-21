import sqlite3

def add_order_date_column():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    
    # Vérifier si la colonne existe déjà
    cursor.execute("PRAGMA table_info(orders)")
    columns = cursor.fetchall()
    if any(column[1] == 'order_date' for column in columns):
        print("La colonne 'order_date' existe déjà.")
    else:
        cursor.execute('''
            ALTER TABLE orders ADD COLUMN order_date DATE
        ''')
        print("Colonne 'order_date' ajoutée avec succès.")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    add_order_date_column()
