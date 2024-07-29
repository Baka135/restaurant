from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import CSRFProtect
import sqlite3
import datetime
from datetime import timedelta
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
csrf = CSRFProtect(app)

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

def init_db():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    
    # Crée les tables si elles n'existent pas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            table_number TEXT NOT NULL,
            items TEXT NOT NULL,
            total_price INTEGER NOT NULL,
            order_date DATE NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            img TEXT NOT NULL,
            category TEXT NOT NULL,
            stock INTEGER NOT NULL DEFAULT 10
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (item_id) REFERENCES menu_items(id)
        )
    ''')

    conn.commit()
    conn.close()

# Initialisation de la base de données au démarrage de l'application
init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu_items WHERE category='dish' ORDER BY RANDOM() LIMIT 3")
    dishes = cursor.fetchall()
    conn.close()
    return render_template('index.html', items=dishes)

@app.route('/dishes')
def dishes():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu_items WHERE category='dish'")
    dishes = cursor.fetchall()
    conn.close()
    return render_template('dishes.html', items=dishes)

@app.route('/drinks')
def drinks():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu_items WHERE category='drink'")
    drinks = cursor.fetchall()
    conn.close()
    return render_template('drinks.html', items=drinks)

@app.route('/desserts')
def desserts():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu_items WHERE category='dessert'")
    desserts = cursor.fetchall()
    conn.close()
    return render_template('desserts.html', items=desserts)

@app.route('/cart')
def cart():
    total_price = sum(item['price'] for item in session.get('cart', []))
    return render_template('cart.html', total_price=total_price)

@app.route('/add-to-cart', methods=['POST'])
@csrf.exempt
def add_to_cart():
    item_id = request.form['item_id']
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu_items WHERE id=?", (item_id,))
    item = cursor.fetchone()
    conn.close()

    if not item:
        flash("Article non trouvé.")
        return redirect(url_for('cart'))

    if len(item) < 6 or item[5] <= 0:  # Vérifie que l'index 5 existe et que le stock est suffisant
        flash("L'article est en rupture de stock.")
        return redirect(url_for('cart'))

    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append({
        'id': item[0],
        'name': item[1],
        'price': item[2],
        'img': item[3]
    })
    session.modified = True
    flash(f"{item[1]} a été ajouté au panier.")
    return redirect(url_for(request.form['redirect']))

@app.route('/remove-from-cart', methods=['POST'])
@csrf.exempt
def remove_from_cart():
    item_id = int(request.form['item_id'])
    session['cart'] = [item for item in session['cart'] if item['id'] != item_id]
    session.modified = True
    flash("Article retiré du panier.")
    return redirect(url_for('cart'))

@app.route('/place-order', methods=['POST'])
@csrf.exempt
def place_order():
    if 'cart' not in session or len(session['cart']) == 0:
        flash("Votre panier est vide. Ajoutez des articles avant de commander.")
        return redirect(url_for('cart'))

    table_number = request.form['table_number']
    items = session['cart']
    total_price = sum(item['price'] for item in items)

    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO orders (table_number, items, total_price, order_date)
        VALUES (?, ?, ?, ?)
    ''', (table_number, json.dumps(items), total_price, datetime.date.today()))

    for item in items:
        cursor.execute("UPDATE menu_items SET stock = stock - 1 WHERE id=?", (item['id'],))

    conn.commit()
    conn.close()
    session.pop('cart', None)
    flash("Commande passée avec succès!")
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
@csrf.exempt
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            flash('Connexion réussie.')
            return redirect(url_for('admin'))
        else:
            flash('Identifiants invalides.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
@csrf.exempt
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if user:
            flash('Le nom d\'utilisateur existe déjà.')
            return redirect(url_for('register'))
        
        cursor.execute('''
            INSERT INTO users (username, password)
            VALUES (?, ?)
        ''', (username, hashed_password))
        conn.commit()
        conn.close()
        flash('Inscription réussie. Vous pouvez maintenant vous connecter.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/admin')
def admin():
    if 'user_id' not in session:
        flash('Veuillez vous connecter pour accéder à cette page.')
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE order_date = ?', (datetime.date.today(),))
    orders = cursor.fetchall()
    cursor.execute('SELECT SUM(total_price) FROM orders WHERE order_date = ?', (datetime.date.today(),))
    total_revenue = cursor.fetchone()[0]
    total_revenue = total_revenue if total_revenue else 0
    conn.close()

    # Convert JSON string to Python objects for items
    for i, order in enumerate(orders):
        try:
            orders[i] = list(order)
            orders[i][2] = json.loads(order[2])
        except json.JSONDecodeError:
            orders[i][2] = []

    return render_template('admin.html', orders=orders, total_revenue=total_revenue)

@app.route('/user_orders')
def user_orders():
    if 'user_id' not in session:
        flash('Veuillez vous connecter pour accéder à cette page.')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE table_number = ?', (user_id,))
    orders = cursor.fetchall()
    conn.close()
    
    return render_template('user_orders.html', orders=orders)

@app.route('/feedback', methods=['POST'])
@csrf.exempt
def feedback():
    if 'user_id' not in session:
        flash('Veuillez vous connecter pour laisser un commentaire.')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    item_id = request.form['item_id']
    rating = int(request.form['rating'])
    comment = request.form['comment']

    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO feedback (user_id, item_id, rating, comment)
        VALUES (?, ?, ?, ?)
    ''', (user_id, item_id, rating, comment))
    conn.commit()
    conn.close()
    flash('Merci pour votre commentaire.')
    return redirect(url_for('index'))

@app.route('/api/orders', methods=['GET'])
def api_orders():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE order_date = ?', (datetime.date.today(),))
    orders = cursor.fetchall()
    conn.close()

    # Convert JSON string to Python objects for items
    for i, order in enumerate(orders):
        try:
            orders[i] = list(order)
            orders[i][2] = json.loads(order[2])
        except json.JSONDecodeError:
            orders[i][2] = []

    return jsonify(orders)

@app.route('/api/revenue', methods=['GET'])
def api_revenue():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    start_date = datetime.date.today() - datetime.timedelta(days=6)
    end_date = datetime.date.today()
    cursor.execute('''
        SELECT order_date, SUM(total_price) FROM orders
        WHERE order_date BETWEEN ? AND ?
        GROUP BY order_date
    ''', (start_date, end_date))
    revenue = cursor.fetchall()
    conn.close()
    return jsonify(revenue)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Déconnexion réussie.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
