from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

sample_product = {
    "id": "a1b2c3d4-e5f6-7890-ab12-34567890abcd",
    "created_at": "2025-07-25T03:00:00Z",
    "updated_at": "2025-07-25T03:00:00Z",
    "name": "iPhone 15 Pro",
    "slug": "iphone-15-pro",
    "description": "The latest iPhone with advanced features",
    "short_description": "Latest iPhone with Pro camera system",
    "sku": "IPHONE15PRO",
    "brand_id": "b2b2c3d4-e5f6-7890-ab12-34567890abcd",
    "category_ids": ["c1c2c3d4-e5f6-7890-ab12-34567890abcd"],
    "tags": ["smartphone", "apple", "pro"],
    "price": 999.0,
    "compare_at_price": 1099.0,
    "cost_price": 850.0,
    "weight": 0.5,
    "dimensions": {"length": 15.0, "width": 7.5, "height": 0.7},
    "inventory_quantity": 100,
    "inventory_status": "in_stock",
    "low_stock_threshold": 10,
    "track_inventory": True,
    "allow_backorder": False,
    "status": "active",
    "is_featured": True,
    "sort_order": 1,
    "meta_title": "iPhone 15 Pro - Buy Now",
    "meta_description": "Get the new iPhone 15 Pro with advanced camera and A17 Pro chip",
    "attributes": [
        {"attribute_id": "d3d3c3d4-e5f6-7890-ab12-34567890abcd", "value": "128GB"},
        {"attribute_id": "e4e4c3d4-e5f6-7890-ab12-34567890abcd", "value": "Black"}
    ],
    "variants": [
        {
            "id": "v1v1c3d4-e5f6-7890-ab12-34567890abcd",
            "created_at": "2025-07-25T03:00:00Z",
            "updated_at": "2025-07-25T03:00:00Z",
            "product_id": "a1b2c3d4-e5f6-7890-ab12-34567890abcd",
            "sku": "IPHONE15PRO-128GB-BLACK",
            "name": "iPhone 15 Pro 128GB Black",
            "price": 999.0,
            "compare_at_price": 1099.0,
            "cost_price": 850.0,
            "weight": 0.5,
            "dimensions": {"length": 15.0, "width": 7.5, "height": 0.7},
            "inventory_quantity": 50,
            "inventory_status": "in_stock",
            "low_stock_threshold": 10,
            "allow_backorder": False,
            "track_inventory": True,
            "variant_attributes": [
                {"attribute_id": "d3d3c3d4-e5f6-7890-ab12-34567890abcd", "value": "128GB"},
                {"attribute_id": "e4e4c3d4-e5f6-7890-ab12-34567890abcd", "value": "Black"}
            ]
        }
    ],
    "images": [
        {
            "id": "i1i1c3d4-e5f6-7890-ab12-34567890abcd",
            "created_at": "2025-07-25T03:00:00Z",
            "updated_at": "2025-07-25T03:00:00Z",
            "product_id": "a1b2c3d4-e5f6-7890-ab12-34567890abcd",
            "image_url": "https://example.com/images/iphone15pro.jpg",
            "alt_text": "iPhone 15 Pro Black",
            "is_primary": True,
            "sort_order": 0
        }
    ],
    "additional_data": {}
}


def test_create_product():
    response = client.post("/products/", json=sample_product)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_product["name"]


def test_read_products():
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
