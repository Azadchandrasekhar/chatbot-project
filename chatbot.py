import json
import random
import speech_recognition as sr
import pyttsx3
import os
from datetime import datetime

file_path = r"C:\Users\LENOVO\Desktop\AZAD class\CHATBOT PROJECT\INTENTS\Chatbot_intents.json"
habit_file = "habits.json"  # Storing user's input habits

# Load JSON data
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Load habits from file
def load_habits():
    if os.path.exists(habit_file):
        with open(habit_file, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}  # Return empty if file is corrupted
    return {}

# Save habits to file
def save_habits():
    with open(habit_file, "w", encoding="utf-8") as file:
        json.dump(user_habits, file, indent=4)

# Initialize TTS
engine = pyttsx3.init()
engine.setProperty('rate', 200)

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Speak function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Voice input function
def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            return recognizer.recognize_google(audio).lower()
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."
        except sr.RequestError:
            return "Voice recognition service is down."

# Habit storage
user_habits = load_habits()  # Load existing habits
habit_mode = {}  # Track whether a user is in habit mode

# Process habit tracking
def process_habit(user_id, user_input):
    """ Stores habits in JSON format """

    # Allow user to exit habit mode
    if user_input in ["done", "enough", "stop"]:
        habit_mode[user_id] = False
        return "Habit tracker mode exited."

    # Expecting input like 'Exercise 7:00 AM'
    parts = user_input.split(" ", 1)

    if len(parts) < 2:
        return "Please enter a valid habit and time (e.g., 'Reading 9:00 PM')."

    habit, time = parts[0].capitalize(), parts[1]

    if user_id not in user_habits:
        user_habits[user_id] = []  # Initialize user habit list if not found

    user_habits[user_id].append({"Habit": habit, "Time": time})
    
    save_habits()  # Save immediately

    return f"Saved: {habit} at {time}."

# Show saved habits
def show_habits(user_id):
    """Displays user's saved habits in correct chronological order."""
    if user_id not in user_habits or len(user_habits[user_id]) == 0:
        return "No habits recorded yet."

    formatted_habits = []
    
    for h in user_habits[user_id]:
        try:
            # Ensure time is in correct format
            time_obj = datetime.strptime(h["Time"], "%I:%M %p")
            formatted_time = time_obj.strftime("%I:%M %p")
            
            formatted_habits.append({"Habit": h["Habit"].capitalize(), "Time": formatted_time, "TimeObj": time_obj})
        except ValueError:
            print(f"Warning: Skipping invalid time format '{h['Time']}' in habits.") # Handle invalid time formats
            continue 

    if not formatted_habits:
        return "No valid habits recorded yet."
        
    # Sort by time
    sorted_habits = sorted(formatted_habits, key=lambda h: h["TimeObj"])

    habit_list = "\n".join([f"{h['Habit']} at {h['Time']}" for h in sorted_habits])
    return f"Your saved habits:\n{habit_list}"


# Find the best matching intent
def match_intent(user_input, intents):
    user_words = set(user_input.lower().split())  
    best_match = None
    best_score = 0.0

    for intent in intents:
        for pattern in intent["patterns"]:
            pattern_words = set(pattern.lower().split())  
            common_words = user_words & pattern_words  

            score = len(common_words) / len(pattern_words) if len(pattern_words) > 0 else 0  

            if score > best_score and score > 0.3:  # Only match if at least 30% words match
                best_score = score
                best_match = intent
    
    return best_match

# Get chatbot response
def get_response(user_id, user_input, intents, context):
    # Handle "more" request
    if user_input == "more":
        if "last_intent" in context and context["last_intent"]:
            matched_intent = next((i for i in intents if i["tag"] == context["last_intent"]), None)
            if matched_intent:
                unused_responses = [r for r in matched_intent["responses"] if r not in context["used_responses"]]
                if unused_responses:
                    response = random.choice(unused_responses)
                    context["used_responses"].append(response)
                    return response
                else:
                    return "I have already provided all information I have."
        return "There's nothing more to add."

    # Check if user is in habit mode
    if habit_mode.get(user_id, False):
        return process_habit(user_id, user_input)

    # If user types "habit", enable habit mode
    if user_input == "habit":
        habit_mode[user_id] = True
        return "Ok I guess I can help you maintain good habits for you, I will provide a habit tracker.\nPlease enter your habit and the time (e.g., 'Exercise 7:00 AM'). Please use 'HH:MM AM/PM'. \nType 'done','stop' when you're finished."

    if user_input == "show habits":
        return show_habits(user_id)

    matched_intent = match_intent(user_input, intents)
    
    if not matched_intent:
        return "I'm not sure what you mean. Could you clarify?"

    response = random.choice(matched_intent["responses"])  
    context["last_intent"] = matched_intent["tag"]
    context["used_responses"] = [response]  

    return response

# Chat function
def chat():
    intents = load_json(file_path)["intents"]
    context = {"last_intent": None, "used_responses": []}  

    user_name = input("Dr.Chatbot: Hey there! What's your name? \nYou: ").strip().capitalize()
    print(f"Dr.Chatbot: Nice to meet you, {user_name}! You can type or say 'voice' to talk. \nSay 'bye' to exit when you are finished. \nIf you want to access HABIT TRACKER, just type 'habit' or 'show habits' to see your habits.\n")
    speak(f"Nice to meet you, {user_name}! You can type or say 'voice' to talk. Say 'bye' to exit when you are finished. If you want to access HABIT TRACKER, just type 'habit' or 'show habits' to see your habits.")

    user_id = user_name  # Using name as a unique identifier

    while True:
        user_input = input(f"{user_name}: ").strip().lower()

        if user_input == "voice":
            print("Switching to voice mode. Say Something...")
            speak("Switching to voice mode. Say Something...")
            user_input = listen()

        if not user_input:
            continue

        if user_input in ["bye", "goodbye", "exit"]:
            print("Dr.Chatbot: Goodbye! Have a great day.")
            speak("Goodbye! Have a great day.")
            break

        response = get_response(user_id, user_input, intents, context)

        print(f"Dr.Chatbot: {response}")
        speak(response)

# Run chatbot
if __name__ == "__main__":
    chat()