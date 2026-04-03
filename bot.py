import json
import pickle
import random
import nltk
from nltk.stem import LancasterStemmer

stemmer = LancasterStemmer()

with open("intents.json", encoding="utf-8") as f:
    intents = json.load(f)

words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))
model = pickle.load(open("food_bot_model.pkl", "rb"))

MENU_PRICES = {
    "pizza": 12, "burger": 8, "pasta": 10,
    "salad": 7, "fries": 4, "drink": 3
}

cart = []

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

def show_cart():
    if not cart:
        return "🛒 Your cart is empty."
    lines = ["🛒 Your Order:"]
    total = 0
    for item in cart:
        price = MENU_PRICES.get(item, 0)
        lines.append(f"  - {item.capitalize()} ${price}")
        total += price
    lines.append(f"  Total: ${total}")
    return "\n".join(lines)

def checkout():
    if not cart:
        return "Your cart is empty! Please add items before checking out."
    total = sum(MENU_PRICES.get(item, 0) for item in cart)
    order_summary = ", ".join(i.capitalize() for i in cart)
    cart.clear()
    return f"✅ Order placed!\nItems: {order_summary}\nTotal: ${total}\nEstimated delivery: 30-45 mins 🚀"

def chat(user_input):
    tag = predict_intent(user_input)

    if not tag:
        return "Sorry, I didn't understand that. Try asking for the menu or placing an order!"

    if tag == "view_cart":
        return show_cart()
    if tag == "checkout":
        return checkout()
    if tag == "cancel":
        cart.clear()
        return get_response(tag)

    if tag.startswith("order_") and tag != "order":
        item = tag.replace("order_", "")
        cart.append(item)

    return get_response(tag)


if __name__ == "__main__":
    print("🍽️  Welcome to FoodBot! Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ["quit", "exit"]:
            print("FoodBot: Goodbye! 👋")
            break
        response = chat(user_input)
        print(f"FoodBot: {response}\n")
