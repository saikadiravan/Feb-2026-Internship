from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

# ══ PYDANTIC MODEL ═══════════════════════════════════════


class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=100)
    delivery_address: str = Field(..., min_length=10)
   
class CustomerFeedback(BaseModel):
    customer_name: str = Field(..., min_length=2)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: str | None = Field(None, max_length=300)
   
class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1, le=50)
   
class BulkOrder(BaseModel):
    company_name: str = Field(..., min_length=2)
    contact_email: str = Field(..., min_length=5)
    items: list[OrderItem] = Field(..., min_items=1)


# ══ DATA (Temporary Database) ════════════════════════════


products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499, 'category': 'Electronics', 'in_stock': True},
    {'id': 2, 'name': 'Notebook', 'price': 99, 'category': 'Stationery', 'in_stock': True},
    {'id': 3, 'name': 'USB Hub', 'price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set', 'price': 49, 'category': 'Stationery', 'in_stock': True},
   
]

orders = []
feedback = []
order_counter = 1

# ══ HELPER FUNCTIONS ═════════════════════════════════════


def find_product(product_id: int):
    """Search product by ID"""
    for p in products:
        if p['id'] == product_id:
            return p
    return None

def calculate_total(product: dict, quantity: int) -> int:
    """Calculate total price"""
    return product['price'] * quantity

def filter_products_logic(category=None, min_price=None, max_price=None, in_stock=None):
    """Apply filters and return products"""
    result = products

    # Category filter
    if category is not None:
        result = [p for p in result if p['category'] == category]

    # Minimum price filter
    if min_price is not None:
        result = [p for p in result if p['price'] >= min_price]

    # Maximum price filter
    if max_price is not None:
        result = [p for p in result if p['price'] <= max_price]

    # Stock filter
    if in_stock is not None:
        result = [p for p in result if p['in_stock'] == in_stock]

    return result

# ══ ENDPOINTS ════════════════════════════════════════════

# Home
@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}


# Get all products
@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}


# Filter products
@app.get('/products/filter')
def filter_products(
    category: str = Query(None, description="Electronics or Stationery"),
    min_price: int = Query(None, description="Minimum price filter"),
    max_price: int = Query(None),
    in_stock: bool = Query(None)
):
    result = filter_products_logic(category, min_price, max_price, in_stock)
    return {'filtered_products': result, 'count': len(result)}


# Compare two products
@app.get('/products/compare')
def compare_products(
    product_id_1: int = Query(...),
    product_id_2: int = Query(...)
):
    p1 = find_product(product_id_1)
    p2 = find_product(product_id_2)

    if not p1:
        return {'error': f'Product {product_id_1} not found'}

    if not p2:
        return {'error': f'Product {product_id_2} not found'}

    cheaper = p1 if p1['price'] < p2['price'] else p2

    return {
        'product_1': p1,
        'product_2': p2,
        'better_value': cheaper['name'],
        'price_diff': abs(p1['price'] - p2['price'])
    }

@app.get('/products/summary')
def product_summary():

    total_products = len(products)
    in_stock_count = len([p for p in products if p['in_stock']])
    out_of_stock_count = len([p for p in products if not p['in_stock']])
    most_expensive_product = max(products, key=lambda p: p['price'])
    cheapest_product = min(products, key=lambda p: p['price'])
    categories = list(set([p['category'] for p in products]))

    return {
        "total_products": total_products,
        "in_stock_count": in_stock_count,
        "out_of_stock_count": out_of_stock_count,
        "most_expensive": {
            "name": most_expensive_product["name"],
            "price": most_expensive_product["price"]
        },
        "cheapest": {
            "name": cheapest_product["name"],
            "price": cheapest_product["price"]
        },
        "categories": categories
    }

# Get product by ID
@app.get('/products/{product_id}')
def get_product(product_id: int):
    product = find_product(product_id)
    if not product:
        return {'error': 'Product not found'}

    return {'product': product}

# Get price of a product
@app.get('/products/{product_id}/price')
def get_product_price(product_id: int):
    product = find_product(product_id)
    if not product:
        return {"error": "Product not found"}

    return {
        "name": product["name"],
        "price": product["price"]
    }
   
# Place order
@app.post('/orders')
def place_order(order_data: OrderRequest):

    global order_counter
    product = find_product(order_data.product_id)
    if not product:
        return {'error': 'Product not found'}

    if not product['in_stock']:
        return {'error': f"{product['name']} is out of stock"}

    total = calculate_total(product, order_data.quantity)

    order = {
        'order_id': order_counter,
        'customer_name': order_data.customer_name,
        'product': product['name'],
        'quantity': order_data.quantity,
        'delivery_address': order_data.delivery_address,
        'total_price': total,
        'status': 'confirmed'
    }

    orders.append(order)
    order_counter += 1
    return {'message': 'Order placed successfully', 'order': order}

@app.post('/feedback')
def submit_feedback(feedback_data: CustomerFeedback):

    feedback_entry = {
        "customer_name": feedback_data.customer_name,
        "product_id": feedback_data.product_id,
        "rating": feedback_data.rating,
        "comment": feedback_data.comment
    }

    feedback.append(feedback_entry)

    return {
        "message": "Feedback submitted successfully",
        "feedback": feedback_entry,
        "total_feedback": len(feedback)
    }

@app.post('/orders/bulk')
def place_bulk_order(order: BulkOrder):

    confirmed = []
    failed = []
    grand_total = 0

    for item in order.items:

        product = find_product(item.product_id)

        if not product:
            failed.append({
                "product_id": item.product_id,
                "reason": "Product not found"
            })
            continue

        if not product["in_stock"]:
            failed.append({
                "product_id": item.product_id,
                "reason": f"{product['name']} is out of stock"
            })
            continue

        subtotal = product["price"] * item.quantity
        grand_total += subtotal

        confirmed.append({
            "product": product["name"],
            "qty": item.quantity,
            "subtotal": subtotal
        })

    return {
        "company": order.company_name,
        "confirmed": confirmed,
        "failed": failed,
        "grand_total": grand_total
    }

# Get all orders
@app.get('/orders')
def get_all_orders():
    return {'orders': orders, 'total_orders': len(orders)}

