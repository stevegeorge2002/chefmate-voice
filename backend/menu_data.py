"""
ChefMate Voice - Menu Database
Restaurant menu with cooking times and ingredients
"""

MENU = {
    # Appetizers
    "caesar_salad": {
        "name": "Caesar Salad",
        "category": "appetizer",
        "cook_time_minutes": 5,
        "ingredients": ["romaine", "parmesan", "croutons", "caesar_dressing"],
        "allergens": ["dairy", "gluten"],
        "price": 12.00
    },
    "garlic_bread": {
        "name": "Garlic Bread",
        "category": "appetizer",
        "cook_time_minutes": 8,
        "ingredients": ["bread", "garlic", "butter", "parsley"],
        "allergens": ["gluten", "dairy"],
        "price": 8.00
    },
    "bruschetta": {
        "name": "Bruschetta",
        "category": "appetizer",
        "cook_time_minutes": 6,
        "ingredients": ["tomato", "basil", "bread", "olive_oil"],
        "allergens": ["gluten"],
        "price": 10.00
    },
    
    # Mains
    "steak_medium_rare": {
        "name": "Steak Medium-Rare",
        "category": "main",
        "cook_time_minutes": 12,
        "ingredients": ["ribeye", "salt", "pepper", "butter"],
        "allergens": ["dairy"],
        "price": 38.00
    },
    "steak_medium": {
        "name": "Steak Medium",
        "category": "main",
        "cook_time_minutes": 15,
        "ingredients": ["ribeye", "salt", "pepper", "butter"],
        "allergens": ["dairy"],
        "price": 38.00
    },
    "steak_well_done": {
        "name": "Steak Well-Done",
        "category": "main",
        "cook_time_minutes": 18,
        "ingredients": ["ribeye", "salt", "pepper", "butter"],
        "allergens": ["dairy"],
        "price": 38.00
    },
    "salmon": {
        "name": "Grilled Salmon",
        "category": "main",
        "cook_time_minutes": 14,
        "ingredients": ["salmon", "lemon", "herbs", "olive_oil"],
        "allergens": ["fish"],
        "price": 32.00
    },
    "pasta_carbonara": {
        "name": "Pasta Carbonara",
        "category": "main",
        "cook_time_minutes": 10,
        "ingredients": ["pasta", "eggs", "bacon", "parmesan", "cream"],
        "allergens": ["gluten", "dairy", "eggs"],
        "price": 24.00
    },
    "chicken_marsala": {
        "name": "Chicken Marsala",
        "category": "main",
        "cook_time_minutes": 16,
        "ingredients": ["chicken", "mushrooms", "marsala_wine", "butter"],
        "allergens": ["dairy", "alcohol"],
        "price": 28.00
    },
    
    # Sides
    "mashed_potatoes": {
        "name": "Mashed Potatoes",
        "category": "side",
        "cook_time_minutes": 8,
        "ingredients": ["potatoes", "butter", "cream", "salt"],
        "allergens": ["dairy"],
        "price": 8.00
    },
    "grilled_vegetables": {
        "name": "Grilled Vegetables",
        "category": "side",
        "cook_time_minutes": 10,
        "ingredients": ["zucchini", "bell_pepper", "onion", "olive_oil"],
        "allergens": [],
        "price": 9.00
    }
}

# Kitchen slang translations
KITCHEN_SLANG = {
    "fire": "start_cooking",
    "86": "sold_out",
    "in_the_weeds": "overwhelmed",
    "on_the_fly": "urgent_rush_order",
    "all_day": "total_count",
    "behind": "running_late",
    "pickup": "order_ready",
    "plated": "finished"
}

# Cooking temperature standards
TEMP_STANDARDS = {
    "rare": "120-125°F",
    "medium_rare": "130-135°F",
    "medium": "135-145°F",
    "medium_well": "145-155°F",
    "well_done": "155-165°F"
}