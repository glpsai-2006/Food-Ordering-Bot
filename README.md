# 🍽️ FoodBot — AI Food Ordering Chatbot

A production-ready conversational food ordering chatbot built with **Flask**, **NLTK**, and **scikit-learn**. Users can chat naturally or use the interactive menu panel to browse items, add items to their cart, view order totals, and place orders.

---

## 🚀 Features

- 🤖 **NLP Intent Classification**: Powered by a trained scikit-learn neural network (`MLPClassifier`) and NLTK stemming/tokenization.
- 📋 **Interactive Menu Panel**: Category tabs (Pizza, Burger, Pasta, Salad, Fries, Drink, Dessert) with quick quantity adjustments and item additions.
- 🛒 **Real-Time Cart & Checkout**: Live total updates, session cart state, and order summary.
- 🔒 **Production Ready**: Configured for WSGI servers (Gunicorn), environment variable handling (`FLASK_SECRET_KEY`, `PORT`), and safe relative path resolution.

---

## 📁 Project Structure

```
Food Ordering Bot/
├── app.py                  # Flask web server & endpoint routes
├── bot.py                  # CLI chatbot runner & utilities
├── train.py                # Model training script
├── intents.json            # Intent patterns & responses
├── words.pkl               # Vocabulary pickle file
├── classes.pkl             # Intent classes pickle file
├── food_bot_model.pkl      # Trained ML model pickle file
├── templates/
│   └── index.html          # Web UI template
├── Procfile                # WSGI start command for cloud hosting (Render/Heroku)
├── runtime.txt             # Python version specification
├── requirements.txt        # Production dependencies (Flask, NLTK, scikit-learn, Gunicorn)
├── .env.example            # Environment variable template
└── README.md               # Documentation & deployment guide
```

---

## ⚙️ Local Setup & Running

### 1. Clone the repository
```bash
git clone https://github.com/glpsai-2006/Food-Ordering-Bot.git
cd Food-Ordering-Bot
```

### 2. Create and activate a virtual environment
- **Windows:**
  ```cmd
  python -m venv .venv
  .venv\Scripts\activate
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables (Optional for Local Dev)
```bash
export FLASK_SECRET_KEY="your-local-secret-key"
export PORT=5000
```

### 5. Run locally
- **Development Server:**
  ```bash
  python app.py
  ```
  Open your browser and navigate to `http://127.0.0.1:5000`

- **Production WSGI Server (Linux/macOS):**
  ```bash
  gunicorn app:app
  ```

---

## 🌐 Production Deployment Guide (Render)

Deploy your application for **FREE** with automatic HTTPS on **Render** in just a few clicks:

### Step 1: Push Changes to GitHub
Make sure your changes (including `Procfile`, `runtime.txt`, `requirements.txt`, updated `app.py`, and `.pkl` model files) are committed and pushed to your GitHub repository:
```bash
git add .
git commit -m "Configure production readiness and deployment setup"
git push origin main
```

### Step 2: Create a New Web Service on Render
1. Go to [Render Dashboard](https://dashboard.render.com/) and log in (or create a free account).
2. Click **New +** -> **Web Service**.
3. Connect your GitHub account and select your repository: **`glpsai-2006/Food-Ordering-Bot`**.

### Step 3: Configure Deployment Settings
Fill in the deployment settings:
- **Name:** `food-ordering-bot` (or any custom name)
- **Region:** Choose closest region (e.g. Oregon, Frankfurt, Singapore)
- **Branch:** `main`
- **Root Directory:** (leave blank)
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

### Step 4: Add Environment Variables
Under the **Environment Variables** section, click **Add Environment Variable**:
- **Key:** `FLASK_SECRET_KEY`
- **Value:** Generate a random strong string (e.g. `9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c`)

*(Note: Render automatically supplies the `PORT` environment variable.)*

### Step 5: Deploy & Obtain Your Public HTTPS URL
1. Click **Create Web Service**.
2. Render will automatically build, install requirements, load NLTK data, and start Gunicorn.
3. Once the build status turns **Live**, your public HTTPS URL will be displayed at the top left of the dashboard:
   `https://food-ordering-bot.onrender.com` (or your custom service URL).

---

## 🧪 Testing the Deployed Application

Once your public URL is live:
1. **Homepage Test**: Open `https://<your-app-name>.onrender.com/` in your browser. Verify menu items load.
2. **Interactive Menu Test**: Select quantity for a menu item (e.g. 2 Pepperoni Pizzas) and click **Add**. Verify item is added to cart panel on the right.
3. **Chatbot NLP Test**: Type `"I want a burger and a coke"` in the chat box and hit Enter. Verify intent classification response.
4. **View Cart & Checkout**: Click **Checkout** or type `"checkout"`. Verify order summary and delivery confirmation.

---

## 🔐 Environment Variables Summary

| Variable Name | Required | Description | Default |
|---------------|----------|-------------|---------|
| `FLASK_SECRET_KEY` | Yes (Production) | Cryptographic secret for signing Flask session cookies | `foodbot_default_secret_key_123` |
| `PORT` | Auto | Server port assigned by host environment | `5000` |
