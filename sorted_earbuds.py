import json
from product_utils import sort_products, popular_products, cheapest_products

# Load your JSON data
with open('jbhifi_tws_earbuds.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# Sort by price
sorted_by_price = cheapest_products(raw_data)
with open('cheapest_jbhifi_tws_earbuds_sorted.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_by_price, f, indent=4, ensure_ascii=False)
print("✅ Saved sorted earbuds by price (low to high)")

# Get top 50 popular products by number of ratings
top_popular = popular_products(raw_data)
with open('popular_jbhifi_tws_earbuds_sorted.json', 'w', encoding='utf-8') as f:
    json.dump(top_popular, f, indent=4, ensure_ascii=False)
print("✅ Saved top 50 popular products")

good_value = sort_products(raw_data)
with open('great_value_jbhifi_tws_earbuds_sorted.json', 'w', encoding='utf-8') as f:
    json.dump(good_value, f, indent=4, ensure_ascii=False)
print("✅ Saved products with great value")