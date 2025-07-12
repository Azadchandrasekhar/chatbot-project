# 🤖 Chatbot Project

A rule-based and NLP-enhanced chatbot focused on supporting mental and physical health through conversational AI.

---

## 🧠 Project Goal

To develop a responsive chatbot that can:
- Identify patterns in user input using traditional AI (pattern matching).
- Provide fallback responses using basic NLP techniques.
- Track user habits and routines via a built-in habit tracker.
- Switch between text and voice input/output.
- Adapt tone and behavior based on the type of query (health, habits, etc.).

---

## 📁 Project Structure

- `chatbot.py` – Main chatbot logic.
- `patterns.json` – Stores input patterns and corresponding responses.
- `habit_tracker.py` – Module to record and manage user habits.
- `speech.py` – Optional voice input/output handling.
- `utils/` – Helper functions and reusable logic.
- `README.md` – You’re reading it!

---

## 🧩 Features

- Pattern-based response system
- NLP fallback for unknown queries
- Habit tracker: collects and logs daily/weekly habits
- Voice input/output (optional)
- Custom name addressing (e.g., “Hello Azad!”)
- Follow-up questions for better responses

---

## 💡 How It Works

1. User enters a message (via text or voice).
2. Chatbot checks for pattern matches.
3. If unclear, it uses NLP (basic similarity or keyword extraction).
4. For certain inputs (like "habit"), it activates the tracker:
   - _"Ok I guess I can help you maintain good habits for you, I will provide a habit tracker."_
   - Asks for habits and time, stores them in a structured format.
5. For requests like exercises, it responds and then asks:
   - _“Do you want more information?”_

---

## 🛠 Technologies Used

- Python
- Regular Expressions
- NLTK / spaCy (for fallback NLP)
- JSON (for storing patterns)
- SQLite / CSV (for storing habits)
- pyttsx3 / SpeechRecognition (for voice interface)

---

## ▶️ How to Run

```bash
python chatbot.py
