from flask import Flask, jsonify, abort

app = Flask(__name__)

# ── In-memory data ──────────────────────────────────────────────────────────
CUSTOMERS = {
    1: {"id": 1, "name": "Alice Johnson", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob Smith",    "email": "bob@example.com"},
    3: {"id": 3, "name": "Carol White",  "email": "carol@example.com"},
}

ORDERS = {
    101: {"order_id": 101, "customer_id": 1, "item": "Laptop",     "status": "shipped",   "amount": 1200.00},
    102: {"order_id": 102, "customer_id": 1, "item": "Mouse",      "status": "delivered", "amount": 25.00},
    103: {"order_id": 103, "customer_id": 2, "item": "Keyboard",   "status": "pending",   "amount": 75.00},
    104: {"order_id": 104, "customer_id": 3, "item": "Monitor",    "status": "processing","amount": 300.00},
}
# ────────────────────────────────────────────────────────────────────────────


@app.route("/")
def index():
    return jsonify({
        "service": "Customer Service",
        "version": "1.0",
        "endpoints": [
            "GET /customers",
            "GET /customers/<customer_id>",
            "GET /customers/<customer_id>/orders",
        ]
    })


@app.route("/customers", methods=["GET"])
def get_all_customers():
    """Return list of all customers."""
    return jsonify({"customers": list(CUSTOMERS.values())}), 200


@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    """Return a single customer by ID."""
    customer = CUSTOMERS.get(customer_id)
    if not customer:
        abort(404, description=f"Customer {customer_id} not found")
    return jsonify(customer), 200


@app.route("/customers/<int:customer_id>/orders", methods=["GET"])
def get_customer_orders(customer_id):
    """Fetch all orders belonging to a customer."""
    if customer_id not in CUSTOMERS:
        abort(404, description=f"Customer {customer_id} not found")

    customer_orders = [
        order for order in ORDERS.values()
        if order["customer_id"] == customer_id
    ]

    return jsonify({
        "customer_id": customer_id,
        "customer_name": CUSTOMERS[customer_id]["name"],
        "orders": customer_orders,
        "total_orders": len(customer_orders),
    }), 200


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not Found", "message": str(e.description)}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)