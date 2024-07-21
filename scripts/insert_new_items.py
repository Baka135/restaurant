import sqlite3

def insert_new_items():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    # Ajouter les nouveaux plats
    dishes = [
        ("Poulet", 5000, "static/images/poulet.jpg", "dish"),
        ("Poisson", 6000, "static/images/poisson.jpg", "dish"),
        ("Makemba", 3000, "static/images/makemba.jpg", "dish"),
        ("Pâtes", 4000, "static/images/pâtes.jpg", "dish")
    ]
    
    # Ajouter les nouvelles boissons
    drinks = [
        ("Coca-cola", 1000, "static/images/coca-cola.jpg", "drink"),
        ("Fanta", 1000, "static/images/fanta.jpg", "drink"),
        ("Maltina", 1500, "static/images/maltina.jpg", "drink"),
        ("Nkoyi", 1200, "static/images/nkoyi.jpg", "drink")
    ]

    # Ajouter les nouveaux desserts
    desserts = [
        ("Crème", 2500, "static/images/crème.jpg", "dessert"),
        ("Tarte", 3000, "static/images/tarte.jpg", "dessert")
    ]

    cursor.executemany('''
        INSERT INTO menu_items (name, price, img, category)
        VALUES (?, ?, ?, ?)
    ''', dishes + drinks + desserts)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_new_items()
    print("Nouveaux éléments du menu ajoutés avec succès.")
