from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from datetime import datetime, timedelta
from functools import wraps
import uuid
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'tindahan_secret_key_2026'

# ==================== DATA STORAGE (In-Memory) ====================

# Users database with roles
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "staff": {"password": "staff123", "role": "staff"},
    "manager": {"password": "manager123", "role": "admin"}
}

# Products: {product_id: {'name': str, 'price': float, 'quantity': int}}
products = {
    "prod_001": {'name': 'Rice', 'price': 50.00, 'quantity': 100},
    "prod_002": {'name': 'Sugar', 'price': 60.00, 'quantity': 75},
    "prod_003": {'name': 'Flour', 'price': 45.00, 'quantity': 50},
    "prod_004": {'name': 'Salt', 'price': 25.00, 'quantity': 120},
    "prod_005": {'name': 'Cooking Oil', 'price': 180.00, 'quantity': 30},
}

# Sales transactions
sales = []

# Stock history
stock_history = []

# ==================== AUTHENTICATION & AUTHORIZATION ====================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        user_role = users[session['user']]['role']
        if user_role != 'admin':
            return render_template('unauthorized.html'), 403
        return f(*args, **kwargs)
    return decorated_function

# ==================== AUTHENTICATION ROUTES ====================

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if username in users and users[username]['password'] == password:
            session['user'] = username
            session['role'] = users[username]['role']
            return redirect(url_for('dashboard'))
        
        return render_template('login.html', error="Invalid username or password.")
    
    return render_template('login.html', error=None)

@app.route("/logout")
def logout():
    session.pop('user', None)
    session.pop('role', None)
    return redirect(url_for('login'))

# ==================== DASHBOARD ROUTE ====================

@app.route("/dashboard")
@login_required
def dashboard():
    total_products = len(products)
    total_inventory_value = sum(p['price'] * p['quantity'] for p in products.values())
    total_sales = len(sales)
    total_sales_value = sum(s['total_price'] for s in sales)
    low_stock_items = sum(1 for p in products.values() if p['quantity'] < 20)
    out_of_stock = sum(1 for p in products.values() if p['quantity'] == 0)
    
    stats = {
        'total_products': total_products,
        'total_inventory_value': f"₱{total_inventory_value:,.2f}",
        'total_sales': total_sales,
        'total_sales_value': f"₱{total_sales_value:,.2f}",
        'low_stock_items': low_stock_items,
        'out_of_stock': out_of_stock,
        'user': session.get('user'),
        'role': session.get('role')
    }
    
    return render_template('dashboard.html', stats=stats)

# ==================== MODULE 1: PRODUCT MANAGEMENT ====================

@app.route("/inventory")
@admin_required
def inventory():
    products_list = []
    for prod_id, prod_data in products.items():
        status = "Out of Stock" if prod_data['quantity'] == 0 else ("Low Stock" if prod_data['quantity'] < 20 else "In Stock")
        products_list.append({
            'id': prod_id,
            'name': prod_data['name'],
            'price': f"₱{prod_data['price']:,.2f}",
            'quantity': prod_data['quantity'],
            'value': f"₱{prod_data['price'] * prod_data['quantity']:,.2f}",
            'status': status
        })
    
    return render_template('inventory.html', products=products_list)

@app.route("/inventory/add", methods=["POST"])
@admin_required
def add_product():
    try:
        product_id = f"prod_{len(products) + 1:03d}"
        name = request.form.get("name").strip()
        price = float(request.form.get("price"))
        quantity = int(request.form.get("quantity"))
        
        if not name or price <= 0 or quantity < 0:
            return jsonify({'success': False, 'message': 'Invalid product data'}), 400
        
        products[product_id] = {'name': name, 'price': price, 'quantity': quantity}
        
        stock_history.append({
            'product_id': product_id,
            'old_qty': 0,
            'new_qty': quantity,
            'action': 'ADD_PRODUCT',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user': session.get('user')
        })
        
        return jsonify({'success': True, 'message': f'Product {product_id} added successfully'}), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route("/inventory/update/<product_id>", methods=["POST"])
@admin_required
def update_product(product_id):
    try:
        if product_id not in products:
            return jsonify({'success': False, 'message': 'Product not found'}), 404
        
        name = request.form.get("name").strip()
        price = float(request.form.get("price"))
        quantity = int(request.form.get("quantity"))
        
        if not name or price <= 0 or quantity < 0:
            return jsonify({'success': False, 'message': 'Invalid product data'}), 400
        
        old_qty = products[product_id]['quantity']
        products[product_id] = {'name': name, 'price': price, 'quantity': quantity}
        
        if old_qty != quantity:
            stock_history.append({
                'product_id': product_id,
                'old_qty': old_qty,
                'new_qty': quantity,
                'action': 'UPDATE_PRODUCT',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'user': session.get('user')
            })
        
        return jsonify({'success': True, 'message': 'Product updated successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route("/inventory/delete/<product_id>", methods=["POST"])
@admin_required
def delete_product(product_id):
    try:
        if product_id not in products:
            return jsonify({'success': False, 'message': 'Product not found'}), 404
        
        product_name = products[product_id]['name']
        del products[product_id]
        
        stock_history.append({
            'product_id': product_id,
            'old_qty': 0,
            'new_qty': 0,
            'action': 'DELETE_PRODUCT',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user': session.get('user')
        })
        
        return jsonify({'success': True, 'message': f'Product {product_name} deleted'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

# ==================== MODULE 2: STOCK MANAGEMENT ====================

@app.route("/stock-management")
@admin_required
def stock_management():
    products_list = []
    for prod_id, prod_data in products.items():
        status = "Out of Stock" if prod_data['quantity'] == 0 else ("Low Stock" if prod_data['quantity'] < 20 else "In Stock")
        products_list.append({
            'id': prod_id,
            'name': prod_data['name'],
            'quantity': prod_data['quantity'],
            'status': status
        })
    
    low_stock = [p for p in products_list if p['status'] == "Low Stock" or p['status'] == "Out of Stock"]
    
    return render_template('stock_management.html', products=products_list, low_stock=low_stock)

@app.route("/stock/increase", methods=["POST"])
@admin_required
def increase_stock():
    try:
        product_id = request.form.get("product_id")
        quantity = int(request.form.get("quantity"))
        
        if product_id not in products:
            return jsonify({'success': False, 'message': 'Product not found'}), 404
        
        if quantity <= 0:
            return jsonify({'success': False, 'message': 'Quantity must be greater than 0'}), 400
        
        old_qty = products[product_id]['quantity']
        products[product_id]['quantity'] += quantity
        
        stock_history.append({
            'product_id': product_id,
            'old_qty': old_qty,
            'new_qty': products[product_id]['quantity'],
            'action': 'RESTOCK',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user': session.get('user')
        })
        
        return jsonify({
            'success': True,
            'message': f'Stock increased by {quantity}',
            'new_qty': products[product_id]['quantity']
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route("/stock/decrease", methods=["POST"])
@admin_required
def decrease_stock():
    try:
        product_id = request.form.get("product_id")
        quantity = int(request.form.get("quantity"))
        
        if product_id not in products:
            return jsonify({'success': False, 'message': 'Product not found'}), 404
        
        if quantity <= 0:
            return jsonify({'success': False, 'message': 'Quantity must be greater than 0'}), 400
        
        if products[product_id]['quantity'] < quantity:
            return jsonify({'success': False, 'message': f'Insufficient stock. Available: {products[product_id]["quantity"]}'}), 400
        
        old_qty = products[product_id]['quantity']
        products[product_id]['quantity'] -= quantity
        
        stock_history.append({
            'product_id': product_id,
            'old_qty': old_qty,
            'new_qty': products[product_id]['quantity'],
            'action': 'MANUAL_ADJUSTMENT',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user': session.get('user')
        })
        
        return jsonify({
            'success': True,
            'message': f'Stock decreased by {quantity}',
            'new_qty': products[product_id]['quantity']
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

# ==================== MODULE 3: SALES TRANSACTION PROCESSING ====================

@app.route("/sales")
@login_required
def sales_page():
    products_list = [{'id': pid, 'name': pdata['name'], 'price': pdata['price'], 'quantity': pdata['quantity']} 
                     for pid, pdata in products.items() if pdata['quantity'] > 0]
    
    recent_sales = []
    for s in sales[-10:]:
        recent_sales.append({
            'id': s['transaction_id'],
            'product': s['product_name'],
            'quantity': s['quantity'],
            'unit_price': f"₱{s['unit_price']:,.2f}",
            'total': f"₱{s['total_price']:,.2f}",
            'timestamp': s['timestamp'],
            'cashier': s['cashier']
        })
    
    recent_sales.reverse()
    
    return render_template('sales.html', products=products_list, recent_sales=recent_sales)

@app.route("/sales/process", methods=["POST"])
@login_required
def process_sale():
    try:
        product_id = request.form.get("product_id")
        quantity = int(request.form.get("quantity"))
        
        if product_id not in products:
            return jsonify({'success': False, 'message': 'Product not found'}), 404
        
        if quantity <= 0:
            return jsonify({'success': False, 'message': 'Quantity must be greater than 0'}), 400
        
        product = products[product_id]
        
        if product['quantity'] < quantity:
            return jsonify({'success': False, 'message': f'Insufficient stock. Available: {product["quantity"]}'}), 400
        
        transaction = {
            'transaction_id': str(uuid.uuid4())[:8],
            'product_id': product_id,
            'product_name': product['name'],
            'quantity': quantity,
            'unit_price': product['price'],
            'total_price': product['price'] * quantity,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'cashier': session.get('user'),
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        
        old_qty = product['quantity']
        product['quantity'] -= quantity
        
        stock_history.append({
            'product_id': product_id,
            'old_qty': old_qty,
            'new_qty': product['quantity'],
            'action': 'SALE',
            'timestamp': transaction['timestamp'],
            'user': session.get('user')
        })
        
        sales.append(transaction)
        
        return jsonify({
            'success': True, 
            'message': 'Sale processed successfully',
            'transaction': transaction
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

# ==================== MODULE 4: SALES HISTORY MANAGEMENT ====================

@app.route("/sales-history")
@login_required
def sales_history():
    history = []
    for s in sales:
        history.append({
            'id': s['transaction_id'],
            'product': s['product_name'],
            'quantity': s['quantity'],
            'unit_price': f"₱{s['unit_price']:,.2f}",
            'total': f"₱{s['total_price']:,.2f}",
            'timestamp': s['timestamp'],
            'date': s['date'],
            'cashier': s['cashier']
        })
    
    history.reverse()
    
    return render_template('sales_history.html', sales=history)

@app.route("/sales/details/<transaction_id>")
@login_required
def sales_details(transaction_id):
    transaction = next((s for s in sales if s['transaction_id'] == transaction_id), None)
    
    if not transaction:
        return render_template('404.html'), 404
    
    details = {
        'id': transaction['transaction_id'],
        'product_name': transaction['product_name'],
        'product_id': transaction['product_id'],
        'quantity': transaction['quantity'],
        'unit_price': f"₱{transaction['unit_price']:,.2f}",
        'total_price': f"₱{transaction['total_price']:,.2f}",
        'timestamp': transaction['timestamp'],
        'date': transaction['date'],
        'cashier': transaction['cashier']
    }
    
    return render_template('transaction_details.html', transaction=details)

# ==================== MODULE 5: REPORTING MODULE ====================

@app.route("/reports")
@admin_required
def reports():
    return render_template('reports_menu.html')

# 5.1 Daily Sales Report
@app.route("/reports/daily")
@admin_required
def daily_sales_report():
    today = datetime.now().strftime('%Y-%m-%d')
    today_sales = [s for s in sales if s['date'] == today]
    
    total_transactions = len(today_sales)
    total_amount = sum(s['total_price'] for s in today_sales)
    
    product_sales = {}
    for s in today_sales:
        if s['product_id'] not in product_sales:
            product_sales[s['product_id']] = {'name': s['product_name'], 'quantity': 0, 'value': 0}
        product_sales[s['product_id']]['quantity'] += s['quantity']
        product_sales[s['product_id']]['value'] += s['total_price']
    
    top_product = max(product_sales.items(), key=lambda x: x[1]['value'], default=(None, {'name': 'N/A', 'quantity': 0, 'value': 0}))
    top_product_data = {'name': top_product[1]['name'], 'quantity': top_product[1]['quantity'], 'value': f"₱{top_product[1]['value']:,.2f}"} if top_product[0] else {'name': 'N/A', 'quantity': 0, 'value': '₱0.00'}
    
    report = {
        'date': today,
        'total_transactions': total_transactions,
        'total_amount': f"₱{total_amount:,.2f}",
        'best_selling': top_product_data,
        'transactions': []
    }
    
    for s in today_sales:
        report['transactions'].append({
            'id': s['transaction_id'],
            'product': s['product_name'],
            'quantity': s['quantity'],
            'unit_price': f"₱{s['unit_price']:,.2f}",
            'total': f"₱{s['total_price']:,.2f}",
            'time': s['timestamp'].split(' ')[1],
            'cashier': s['cashier']
        })
    
    report['transactions'].reverse()
    
    return render_template('daily_report.html', report=report)

# 5.2 Monthly Sales Report
@app.route("/reports/monthly", methods=["GET", "POST"])
@admin_required
def monthly_sales_report():
    if request.method == "POST":
        month_year = request.form.get("month_year")
    else:
        month_year = datetime.now().strftime('%Y-%m')
    
    month_sales = [s for s in sales if s['date'].startswith(month_year)]
    
    total_amount = sum(s['total_price'] for s in month_sales)
    total_transactions = len(month_sales)
    
    daily_totals = defaultdict(float)
    for s in month_sales:
        daily_totals[s['date']] += s['total_price']
    
    avg_daily_sales = total_amount / len(daily_totals) if daily_totals else 0
    
    product_sales = {}
    for s in month_sales:
        if s['product_id'] not in product_sales:
            product_sales[s['product_id']] = {'name': s['product_name'], 'quantity': 0, 'value': 0}
        product_sales[s['product_id']]['quantity'] += s['quantity']
        product_sales[s['product_id']]['value'] += s['total_price']
    
    product_summary = [
        {'name': v['name'], 'quantity': v['quantity'], 'value': f"₱{v['value']:,.2f}"}
        for k, v in sorted(product_sales.items(), key=lambda x: x[1]['value'], reverse=True)
    ]
    
    daily_breakdown = [
        {'date': date, 'amount': f"₱{amount:,.2f}"}
        for date, amount in sorted(daily_totals.items())
    ]
    
    report = {
        'month_year': month_year,
        'total_transactions': total_transactions,
        'total_amount': f"₱{total_amount:,.2f}",
        'average_daily': f"₱{avg_daily_sales:,.2f}",
        'product_summary': product_summary,
        'daily_breakdown': daily_breakdown
    }
    
    return render_template('monthly_report.html', report=report)

# 5.3 Inventory Report
@app.route("/reports/inventory")
@admin_required
def inventory_report():
    current_stock = []
    low_stock = []
    out_of_stock = []
    
    total_inventory_value = 0
    
    for prod_id, prod in products.items():
        stock_value = prod['price'] * prod['quantity']
        total_inventory_value += stock_value
        
        item = {
            'id': prod_id,
            'name': prod['name'],
            'quantity': prod['quantity'],
            'price': f"₱{prod['price']:,.2f}",
            'value': f"₱{stock_value:,.2f}"
        }
        
        current_stock.append(item)
        
        if prod['quantity'] == 0:
            out_of_stock.append(item)
        elif prod['quantity'] < 20:
            low_stock.append(item)
    
    report = {
        'total_items': sum(p['quantity'] for p in products.values()),
        'total_value': f"₱{total_inventory_value:,.2f}",
        'current_stock': current_stock,
        'low_stock': low_stock,
        'out_of_stock': out_of_stock
    }
    
    return render_template('inventory_report.html', report=report)

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)