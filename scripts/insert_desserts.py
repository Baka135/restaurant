import sqlite3

def insert_desserts():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    desserts = [
        ("Crème", 2500, "static/images/crème.jpg", "dessert"),
        ("Tarte", 3000, "static/images/tarte.jpg", "dessert")
    ]

    cursor.executemany('''
        INSERT INTO menu_items (name, price, img, category)
        VALUES (?, ?, ?, ?)
    ''', desserts)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_desserts()
    print("Desserts ajoutés avec succès.")
