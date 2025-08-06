# product_utils.py

def parse_price(price_str):
    if not price_str:
        return float('inf')
    return float(price_str.replace('$', '').replace(',', '').strip())

def parse_rating(rating_str):
    try:
        return float(rating_str)
    except:
        return 0.0

def cheapest_products(products):
    return sorted(products, key=lambda p: parse_price(p.get('price')))

def popular_products(products):
    return sorted(
        products,
        key=lambda p: int(p.get('number_of_ratings', '0').replace('(', '').replace(')', '')),
        reverse=True
    )[:50]

def sort_products(products):
    # Filter out products with rating <= 3.5 or missing ratings
    filtered = [
        p for p in products 
        if p.get('rating') and parse_rating(p['rating']) > 3.5
    ]

    # Sort the remaining products by price (ascending)
    return sorted(filtered, key=lambda p: parse_price(p.get('price')))
