import json
import pickle
import nltk
from nltk.stem import LancasterStemmer
from sklearn.neural_network import MLPClassifier

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

stemmer = LancasterStemmer()

with open("intents.json", encoding="utf-8") as f:
    intents = json.load(f)

words, classes, documents = [], [], []
ignore = ["?", "!", ".", ","]

for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        tokens = nltk.word_tokenize(pattern)
        words.extend(tokens)
        documents.append((tokens, intent["tag"]))
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

words = sorted(set(stemmer.stem(w.lower()) for w in words if w not in ignore))
classes = sorted(classes)

pickle.dump(words, open("words.pkl", "wb"))
pickle.dump(classes, open("classes.pkl", "wb"))

X, y = [], []
for doc_words, tag in documents:
    stemmed = [stemmer.stem(w.lower()) for w in doc_words]
    bag = [1 if w in stemmed else 0 for w in words]
    X.append(bag)
    y.append(tag)

model = MLPClassifier(hidden_layer_sizes=(128, 64), max_iter=500, random_state=42)
model.fit(X, y)

pickle.dump(model, open("food_bot_model.pkl", "wb"))
print("✅ Model trained and saved successfully!")
