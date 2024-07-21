import sqlite3

def insert_drinks():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    drinks = [
        ("Coca-cola", 1000, "static/images/coca-cola.jpg", "drink"),
        ("Fanta", 1000, "static/images/fanta.jpg", "drink"),
        ("Maltina", 1500, "static/images/maltina.jpg", "drink"),
        ("Nkoyi", 1200, "static/images/nkoyi.jpg", "drink")
    ]

    cursor.executemany('''
        INSERT INTO menu_items (name, price, img, category)
        VALUES (?, ?, ?, ?)
    ''', drinks)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_drinks()
    print("Boissons ajoutées avec succès.")
