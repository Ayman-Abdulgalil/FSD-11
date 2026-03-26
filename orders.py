from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# ── In-memory data ──────────────────────────────────────────────────────────
ORDERS = {
    101: {"order_id": 101, "customer_id": 1, "item": "Laptop",   "status": "shipped",    "amount": 1200.00},
    102: {"order_id": 102, "customer_id": 1, "item": "Mouse",    "status": "delivered",  "amount": 25.00},
    103: {"order_id": 103, "customer_id": 2, "item": "Keyboard", "status": "pending",    "amount": 75.00},
    104: {"order_id": 104, "customer_id": 3, "item": "Monitor",  "status": "processing", "amount": 300.00},
}

VALID_STATUSES = {"pending", "processing", "shipped", "delivered", "cancelled"}
# ────────────────────────────────────────────────────────────────────────────


@app.route("/")
def index():
    return jsonify({
        "service": "Order Service",
        "version": "1.0",
        "endpoints": [
            "GET  /orders",
            "GET  /orders/<order_id>",
            "PUT  /orders/<order_id>/status",
        ],
        "valid_statuses": sorted(VALID_STATUSES),
    })


@app.route("/orders", methods=["GET"])
def get_all_orders():
    """Return all orders."""
    return jsonify({"orders": list(ORDERS.values()), "total": len(ORDERS)}), 200


@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    """Return a single order by ID."""
    order = ORDERS.get(order_id)
    if not order:
        abort(404, description=f"Order {order_id} not found")
    return jsonify(order), 200


@app.route("/orders/<int:order_id>/status", methods=["PUT"])
def update_order_status(order_id):
    """
    Update the status of an order.

    Request body (JSON):
        { "status": "shipped" }
    """
    order = ORDERS.get(order_id)
    if not order:
        abort(404, description=f"Order {order_id} not found")

    body = request.get_json(silent=True)
    if not body or "status" not in body:
        abort(400, description='Request body must contain { "status": "<value>" }')

    new_status = body["status"].strip().lower()
    if new_status not in VALID_STATUSES:
        abort(400, description=(
            f"Invalid status '{new_status}'. "
            f"Choose from: {sorted(VALID_STATUSES)}"
        ))

    old_status = order["status"]
    ORDERS[order_id]["status"] = new_status

    return jsonify({
        "message": "Order status updated successfully",
        "order_id": order_id,
        "old_status": old_status,
        "new_status": new_status,
        "order": ORDERS[order_id],
    }), 200


@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad Request", "message": str(e.description)}), 400


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not Found", "message": str(e.description)}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)