import sqlite3

def insert_dishes():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    dishes = [
        ("Poulet", 5000, "static/images/poulet.jpg", "dish"),
        ("Poisson", 6000, "static/images/poisson.jpg", "dish"),
        ("Makemba", 3000, "static/images/makemba.jpg", "dish"),
        ("Pâtes", 4000, "static/images/pâtes.jpg", "dish")
    ]

    cursor.executemany('''
        INSERT INTO menu_items (name, price, img, category)
        VALUES (?, ?, ?, ?)
    ''', dishes)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_dishes()
    print("Plats ajoutés avec succès.")
