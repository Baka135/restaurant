import sqlite3
import datetime

def update_order_dates():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE orders
        SET order_date = ?
    ''', (datetime.date.today(),))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_order_dates()
    print("Dates des commandes mises à jour avec succès.")
