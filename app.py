from flask import Flask, render_template, request, jsonify, session
import json
import os
import pickle
import random
import re
import nltk
from nltk.stem import LancasterStemmer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def init_nltk():
    for resource in ['punkt', 'punkt_tab']:
        try:
            nltk.data.find(f'tokenizers/{resource}')
        except LookupError:
            try:
                nltk.download(resource, quiet=True)
            except Exception as e:
                print(f"Warning: Failed to download NLTK resource {resource}: {e}")

init_nltk()

stemmer = LancasterStemmer()

with open(os.path.join(BASE_DIR, "intents.json"), encoding="utf-8") as f:
    intents = json.load(f)

words = pickle.load(open(os.path.join(BASE_DIR, "words.pkl"), "rb"))
model = pickle.load(open(os.path.join(BASE_DIR, "food_bot_model.pkl"), "rb"))

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "foodbot_default_secret_key_123")

MENU = {
    "pizza": {
        "emoji": "🍕",
        "varieties": {
            "Margherita": 11, "Pepperoni": 13, "BBQ Chicken": 14, "Veggie": 12
        }
    },
    "burger": {
        "emoji": "🍔",
        "varieties": {
            "Classic": 8, "Cheeseburger": 9, "Chicken Burger": 10, "Veggie Burger": 8
        }
    },
    "pasta": {
        "emoji": "🍝",
        "varieties": {
            "Alfredo": 10, "Carbonara": 11, "Penne Arrabbiata": 9, "Spaghetti Bolognese": 12
        }
    },
    "salad": {
        "emoji": "🥗",
        "varieties": {
            "Caesar": 7, "Greek": 7, "Garden": 6, "Pasta Salad": 8
        }
    },
    "fries": {
        "emoji": "🍟",
        "varieties": {
            "Regular": 4, "Curly": 5, "Cheese Fries": 6, "Sweet Potato": 5
        }
    },
    "drink": {
        "emoji": "🥤",
        "varieties": {
            "Coke": 3, "Pepsi": 3, "Orange Juice": 4, "Lemonade": 4, "Milkshake": 5
        }
    },
    "dessert": {
        "emoji": "🍰",
        "varieties": {
            "Chocolate Cake": 6, "Ice Cream": 5, "Brownie": 4, "Cheesecake": 7
        }
    }
}

WORD_TO_NUM = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
}

VARIETY_MAP = {}
for category, data in MENU.items():
    for variety in data["varieties"]:
        VARIETY_MAP[variety.lower()] = (category, variety)

def get_quantity(text):
    text = text.lower()
    for word, num in WORD_TO_NUM.items():
        if word in text:
            return num
    match = re.search(r'\b(\d+)\b', text)
    return int(match.group(1)) if match else 1

def get_variety_from_text(text):
    text_lower = text.lower()
    for key, (category, variety) in VARIETY_MAP.items():
        if key in text_lower:
            return category, variety
    return None, None

def bag_of_words(sentence):
    tokens = nltk.word_tokenize(sentence)
    stemmed = [stemmer.stem(w.lower()) for w in tokens]
    return [1 if w in stemmed else 0 for w in words]

def predict_intent(sentence):
    bow = [bag_of_words(sentence)]
    proba = model.predict_proba(bow)[0]
    max_prob = max(proba)
    if max_prob < 0.4:
        return None
    return model.classes_[proba.argmax()]

def get_response(tag):
    for intent in intents["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])
    return "I'm not sure I understand. Could you rephrase?"

def show_cart(cart):
    if not cart:
        return "🛒 Your cart is empty."
    lines = ["🛒 Your Order:"]
    total = 0
    for entry in cart:
        emoji = MENU[entry["category"]]["emoji"]
        price = entry["price"] * entry["qty"]
        lines.append(f"  {emoji} {entry['qty']}x {entry['variety']} {entry['category'].capitalize()} — ${price}")
        total += price
    lines.append(f"\n  💰 Total: ${total}")
    return "\n".join(lines)

def checkout(cart):
    if not cart:
        return "Your cart is empty! Please add items before checking out."
    total = sum(e["price"] * e["qty"] for e in cart)
    summary = ", ".join(f"{e['qty']}x {e['variety']} {e['category'].capitalize()}" for e in cart)
    cart.clear()
    return f"✅ Order placed!\nItems: {summary}\nTotal: ${total}\nEstimated delivery: 30-45 mins 🚀"

def add_to_cart(cart, category, variety, qty):
    price = MENU[category]["varieties"][variety]
    for entry in cart:
        if entry["category"] == category and entry["variety"] == variety:
            entry["qty"] += qty
            return
    cart.append({"category": category, "variety": variety, "price": price, "qty": qty})

@app.route("/")
def index():
    session["cart"] = []
    return render_template("index.html", menu=MENU)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "").strip()
    cart = session.get("cart", [])

    # Handle direct add from menu UI
    if data.get("direct_add"):
        category = data.get("category")
        variety = data.get("variety")
        qty = int(data.get("qty", 1))
        if category in MENU and variety in MENU[category]["varieties"]:
            add_to_cart(cart, category, variety, qty)
            session["cart"] = cart
            emoji = MENU[category]["emoji"]
            price = MENU[category]["varieties"][variety]
            return jsonify({"response": f"{emoji} {qty}x {variety} {category.capitalize()} added to cart! (${price * qty})\nAnything else?"})

    if not user_input:
        return jsonify({"response": "Please type something!"})

    tag = predict_intent(user_input)
    qty = get_quantity(user_input)
    variety_category, variety_name = get_variety_from_text(user_input)

    if not tag:
        response = "Sorry, I didn't understand. Try asking for the menu or placing an order!"
    elif tag == "view_cart":
        response = show_cart(cart)
    elif tag == "checkout":
        response = checkout(cart)
        session["cart"] = []
        return jsonify({"response": response})
    elif tag == "cancel":
        session["cart"] = []
        response = get_response(tag)
    elif tag.startswith("order_") and tag != "order":
        category = tag.replace("order_", "")
        if category in MENU:
            if variety_category == category and variety_name:
                add_to_cart(cart, category, variety_name, qty)
                emoji = MENU[category]["emoji"]
                price = MENU[category]["varieties"][variety_name]
                response = f"{emoji} {qty}x {variety_name} {category.capitalize()} added! (${price * qty})\nAnything else?"
            else:
                default_variety = list(MENU[category]["varieties"].keys())[0]
                add_to_cart(cart, category, default_variety, qty)
                emoji = MENU[category]["emoji"]
                price = MENU[category]["varieties"][default_variety]
                response = f"{emoji} {qty}x {default_variety} {category.capitalize()} added! (${price * qty})\nTip: You can specify a variety like 'Pepperoni Pizza' or pick from the menu panel!"
        else:
            response = get_response(tag)
    else:
        response = get_response(tag)

    session["cart"] = cart
    return jsonify({"response": response})

@app.route("/cart", methods=["GET"])
def get_cart():
    cart = session.get("cart", [])
    total = sum(e["price"] * e["qty"] for e in cart)
    return jsonify({"cart": cart, "total": total})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
