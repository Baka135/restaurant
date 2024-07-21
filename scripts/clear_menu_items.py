import sqlite3

def clear_menu_items():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM menu_items')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    clear_menu_items()
    print("Tous les éléments du menu ont été supprimés avec succès.")
