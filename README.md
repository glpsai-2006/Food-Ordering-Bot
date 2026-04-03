# 🍽️ FoodBot — AI Food Ordering Chatbot

A conversational food ordering chatbot built with **Flask**, **NLTK**, and **scikit-learn**. Users can chat naturally or use the interactive menu panel to browse items, add to cart, and place orders.

---

## 🚀 Features

- 🤖 NLP-powered chatbot using a trained intent classification model
- 📋 Interactive menu panel with category tabs and quantity controls
- 🛒 Real-time cart with live total updates
- ✅ Order checkout with order summary
- ⚡ Quick-action buttons for common commands
- 🌐 Web-based UI built with Flask + vanilla JS

---

## 🍕 Menu Categories

| Category | Varieties |
|----------|-----------|
| 🍕 Pizza | Margherita, Pepperoni, BBQ Chicken, Veggie |
| 🍔 Burger | Classic, Cheeseburger, Chicken Burger, Veggie Burger |
| 🍝 Pasta | Alfredo, Carbonara, Penne Arrabbiata, Spaghetti Bolognese |
| 🥗 Salad | Caesar, Greek, Garden, Pasta Salad |
| 🍟 Fries | Regular, Curly, Cheese Fries, Sweet Potato |
| 🥤 Drink | Coke, Pepsi, Orange Juice, Lemonade, Milkshake |
| 🍰 Dessert | Chocolate Cake, Ice Cream, Brownie, Cheesecake |

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **NLP:** NLTK (LancasterStemmer, tokenization)
- **ML Model:** scikit-learn (intent classification)
- **Frontend:** HTML, CSS, JavaScript (vanilla)
- **Session Management:** Flask sessions

---

## 📁 Project Structure

```
Food Ordering Bot/
├── templates/
│   └── index.html          # Frontend UI
├── app.py                  # Flask app & chatbot logic
├── train.py                # Model training script
├── bot.py                  # Bot utilities
├── intents.json            # Intent patterns & responses
├── words.pkl               # Vocabulary pickle
├── classes.pkl             # Intent classes pickle
├── food_bot_model.pkl      # Trained ML model
├── requirements.txt        # Python dependencies
└── README.md
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/glpsai-2006/Food-Ordering-Bot.git
   cd Food-Ordering-Bot
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the model** *(skip if `food_bot_model.pkl` already exists)*
   ```bash
   python train.py
   ```

5. **Run the app**
   ```bash
   python app.py
   ```

6. Open your browser and go to `http://127.0.0.1:5000`

---

## 💬 How to Use

- **Chat naturally:** Type things like `"I want 2 pepperoni pizzas and a coke"`
- **Use the menu panel:** Browse categories, set quantity, and click **Add**
- **Quick buttons:** Use the shortcut buttons for Menu, Cart, Checkout, Cancel
- **View cart:** Type `"View cart"` or click the 🛒 Cart button
- **Checkout:** Type `"Checkout"` or click ✅ Place Order

---

## 📦 Dependencies

```
flask
nltk
scikit-learn
```

---

## 🙌 Author

**glpsai-2006** — [GitHub](https://github.com/glpsai-2006)
