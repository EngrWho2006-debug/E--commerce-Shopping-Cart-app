from flask import Flask, render_template, redirect, url_for, request, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'super_secret_secure_key_for_sessions'

# Initialize an in-memory database for demonstration purposes
def init_db():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            image_url TEXT
        )
    ''')
    # Insert sample products
    sample_products = [
        ('Wireless Headphones', 99.99, 'High-quality sound with noise cancellation.', 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500'),
        ('Minimalist Watch', 149.50, 'Sleek, elegant, and water-resistant.', 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500'),
        ('Mechanical Keyboard', 89.99, 'RGB backlit keys with tactile switches.', 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500')
    ]
    cursor.executemany('INSERT INTO products (name, price, description, image_url) VALUES (?, ?, ?, ?)', sample_products)
    conn.commit()
    return conn

db_conn = init_db()

@app.route('/')
def index():
    # Initialize cart if it doesn't exist in the user's session
    if 'cart' not in session:
        session['cart'] = {}
        
    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    
    # Calculate cart totals
    cart = session.get('cart', {})
    cart_items = []
    total_price = 0.0
    
    for product_id, quantity in cart.items():
        cursor.execute('SELECT id, name, price FROM products WHERE id = ?', (product_id,))
        prod = cursor.fetchone()
        if prod:
            item_total = prod[2] * quantity
            total_price += item_total
            cart_items.append({
                'id': prod[0],
                'name': prod[1],
                'price': prod[2],
                'quantity': quantity,
                'total': round(item_total, 2)
            })

    return render_template('index.html', products=products, cart_items=cart_items, total_price=round(total_price, 2))

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    cart = session.get('cart', {})
    # Convert ID to string because session keys must be strings
    prod_id_str = str(product_id)
    
    cart[prod_id_str] = cart.get(prod_id_str, 0) + 1
    session['cart'] = cart
    flash('Product added to cart!', 'success')
    return redirect(url_for('index'))

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    prod_id_str = str(product_id)
    
    if prod_id_str in cart:
        del cart[prod_id_str]
        session['cart'] = cart
        flash('Item removed from cart.', 'info')
    return redirect(url_for('index'))

@app.route('/checkout', methods=['POST'])
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty!', 'danger')
        return redirect(url_for('index'))
    
    # Secure Payment Processing Simulation
    # Real-world equivalent: Tokenizing data via Stripe/PayPal APIs over HTTPS
    card_number = request.form.get('card_number')
    expiry = request.form.get('expiry')
    cvv = request.form.get('cvv')
    
    if not card_number or not expiry or not cvv:
        flash('Payment details are missing or invalid.', 'danger')
        return redirect(url_for('index'))
    
    # Simulate API success validation
    # Clear the cart after successful "payment"
    session.pop('cart', None)
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)