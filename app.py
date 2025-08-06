from flask import Flask, render_template, request, jsonify
import csv, os

app = Flask(__name__)

CSV_FILE = os.path.join("data", "flashcards.csv")

def read_flashcards():
    flashcards = {}
    if not os.path.exists(CSV_FILE):
        return flashcards
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            deck = row["deck"]
            if deck not in flashcards:
                flashcards[deck] = {
                    "category": row["category"],
                    "cards": []
                }
            flashcards[deck]["cards"].append({
                "question": row["question"],
                "answer": row["answer"]
            })
    return flashcards

def write_flashcard(deck, category, question, answer):
    with open(CSV_FILE, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([deck, category, question, answer])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/flashcards")
def get_flashcards():
    return jsonify(read_flashcards())

@app.route("/api/add_flashcard", methods=["POST"])
def add_flashcard():
    data = request.get_json()
    deck = data.get("deck", "")
    category = data.get("category", "")
    question = data.get("question", "")
    answer = data.get("answer", "")
    if deck and question and answer:
        write_flashcard(deck, category, question, answer)
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400

if __name__ == "__main__":
    app.run(debug=True)
