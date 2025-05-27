# inventory-api/main.py
from flask import Flask, request, jsonify
import os
import psycopg2
import psycopg2.extras
from datetime import datetime

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'localhost'),
        port=os.getenv('POSTGRES_PORT', '5432'),
        dbname=os.getenv('POSTGRES_DB', 'inventory_db'),
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', 'postgres')
    )
    conn.autocommit = True
    return conn

# Initialize database
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create inventory table with id as primary key, allowing multiple entries per SKU
    cur.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id SERIAL PRIMARY KEY,
            sku VARCHAR(50) NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create an index on SKU for faster lookups
    cur.execute('''
        CREATE INDEX IF NOT EXISTS idx_inventory_sku ON inventory(sku)
    ''')
    
    cur.close()
    conn.close()

# API endpoint 1: Add inventory for a SKU
@app.route('/inventory', methods=['POST'])
def add_inventory():
    data = request.get_json()
    
    # Validate required fields
    if not all(k in data for k in ['sku', 'quantity']):
        return jsonify({"error": "SKU and quantity are required"}), 400
    
    sku = data['sku']
    quantity = int(data['quantity'])
    
    # Validate quantity is positive
    if quantity <= 0:
        return jsonify({"error": "Quantity must be positive"}), 400
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # Insert a new inventory entry for this SKU
    cur.execute('''
        INSERT INTO inventory (sku, quantity, created_at)
        VALUES (%s, %s, CURRENT_TIMESTAMP)
        RETURNING id, sku, quantity, created_at
    ''', (sku, quantity))
    
    result = dict(cur.fetchone())

    
    cur.close()
    conn.close()
    
    return jsonify({
        "id": result['id'],
        "sku": result['sku'],
        "quantity_added": result['quantity'],
        "created_at": result['created_at'].isoformat()
    }), 201

# API endpoint 2: Get total inventory for a specific SKU
@app.route('/', methods=['GET'])
def health_check():
    try:
        # Test database connection
        conn = get_db_connection()
        conn.close()
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return jsonify({
        "status": "ok",
        "service": "inventory-api",
        "database": db_status,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/inventory/<sku>', methods=['GET'])
def get_inventory(sku):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # Sum all quantities for this SKU
    cur.execute('''
        SELECT SUM(quantity) as total_quantity,
               MAX(created_at) as last_updated
        FROM inventory
        WHERE sku = %s
    ''', (sku,))
    
    result = cur.fetchone()
    
    # Check if any entries exist for this SKU
    cur.execute('SELECT COUNT(*) as count FROM inventory WHERE sku = %s', (sku,))
    count = cur.fetchone()['count']
    
    cur.close()
    conn.close()
    
    if count == 0:
        return jsonify({"error": "SKU not found", "sku": sku, "total_quantity": 0}), 404
    
    return jsonify({
        "sku": sku,
        "total_quantity": result['total_quantity'],
        "last_updated": result['last_updated'].isoformat() if result['last_updated'] else None,
        "entry_count": count
    })

# API endpoint 3: Get all SKUs with their total stock counts
@app.route('/inventory', methods=['GET'])
def get_all_inventory():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # Get sum of quantities grouped by SKU
    cur.execute('''
        SELECT sku, SUM(quantity) as total_quantity
        FROM inventory
        GROUP BY sku
        ORDER BY sku
    ''')
    
    results = cur.fetchall()
    inventory_list = [{"sku": row['sku'], "total_quantity": row['total_quantity']} for row in results]
    
    cur.close()
    conn.close()
    
    return jsonify({
        "inventory_count": len(inventory_list),
        "inventory": inventory_list
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')
