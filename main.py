import cv2
import time
import mediapipe as mp
import pyttsx3
import random
import sys
import json
import webbrowser
import speech_recognition as sr
from datetime import datetime


# Load knowledge base
with open("knowledge_base.json", "r") as f:
    knowledge = json.load(f)

# Initialize engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 180)

# Speak function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# ----------- Rock Paper Scissors Logic -----------
def detect_gesture(hand_landmarks):
    finger_up = []
    landmarks = hand_landmarks.landmark
    tips_ids = [8, 12, 16, 20]

    for tip in tips_ids:
        if landmarks[tip].y < landmarks[tip - 2].y:
            finger_up.append(1)
        else:
            finger_up.append(0)

    thumb = 1 if landmarks[4].x > landmarks[3].x else 0

    if finger_up == [0, 0, 0, 0] and thumb == 0:
        return "rock"
    elif finger_up == [1, 1, 1, 1] and thumb == 1:
        return "paper"
    elif finger_up == [1, 1, 0, 0]:
        return "scissors"
    else:
        return "none"

def get_winner(user, comp):
    if user == comp:
        return "draw"
    elif (user == "rock" and comp == "scissors") or \
         (user == "paper" and comp == "rock") or \
         (user == "scissors" and comp == "paper"):
        return "user"
    else:
        return "Praggya"

def play_rps():
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
    cap = cv2.VideoCapture(0)

    user_score = 0
    Praggya_score = 0
    prev_move_time = 0
    game_on = True

    speak("Game started. Press Q to quit anytime.")
    print("Game started. Press Q to quit anytime.")

    while cap.isOpened():
        success, image = cap.read()
        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = hands.process(image_rgb)
        key = cv2.waitKey(5) & 0xFF

        if key == ord('q'):
            speak(f"Game ended. Final score: You {user_score}, Praggya {Praggya_score}")
            print(f"Game ended. Final score: You {user_score}, Praggya {Praggya_score}")
            break

        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                gesture = detect_gesture(handLms)
                if gesture != "none":
                    current_time = time.time()
                    if current_time - prev_move_time > 5:
                        comp_move = random.choice(["rock", "paper", "scissors"])
                        winner = get_winner(gesture, comp_move)

                        if winner == "user":
                            user_score += 1
                            speak(f"You showed {gesture}. Praggya chose {comp_move}. You win!")
                        elif winner == "Praggya":
                            Praggya_score += 1
                            speak(f"You showed {gesture}. Praggya chose {comp_move}. You lose!")
                        else:
                            speak(f"You both chose {gesture}. It's a draw.")
                        prev_move_time = current_time

                mp_drawing.draw_landmarks(image, handLms, mp_hands.HAND_CONNECTIONS)

        cv2.putText(image, f"User: {user_score}", (10, 60), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 255, 0), 2)
        cv2.putText(image, f"Praggya: {Praggya_score}", (10, 200), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 0, 255), 2)
        cv2.imshow("Rock Paper Scissors", image)

    cap.release()
    cv2.destroyAllWindows()

# ----------- Praggya Command Processor -----------
def processCommand(c):
    command = c.lower()
    
    if command in knowledge:
        speak(knowledge[command])
        print(knowledge[command])
    elif "open" in command:
        sites = {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "stack overflow": "https://www.stackoverflow.com",
            "wikipedia": "https://www.wikipedia.org",
            "amazon": "https://www.amazon.com",
            "facebook": "https://www.facebook.com",
            "instagram": "https://www.instagram.com",
            "linkedin": "https://www.linkedin.com"
        }
        for site in sites:
            if site in command:
                webbrowser.open(sites[site])
                return
    elif command.startswith("play"):
        try:
            import musiclibrary
            song = command.split(" ")[1]
            link = musiclibrary.music.get(song)
            if link:
                webbrowser.open(link)
            else:
                speak("Sorry, song not found.")
        except:
            speak("Music library module missing.")
    elif "stop listening" in command:
        speak("Okay, shutting down. Goodbye!")
        print("Okay, shutting down. Goodbye!")
        sys.exit()
    elif "what is the time" in command:
        speak("The current time is " + datetime.now().strftime("%I:%M %p"))
        print("The current time is " + datetime.now().strftime("%I:%M %p"))
    elif "what is the date" in command:
        speak("Today's date is " + datetime.now().strftime("%B %d, %Y"))
        print("Today's date is " + datetime.now().strftime("%B %d, %Y"))
    elif "what day is it" in command:
        speak("Today is " + datetime.now().strftime("%A"))
        print("Today is " + datetime.now().strftime("%A"))
    elif "let's play" in command:
        speak("Launching Rock Paper Scissors game.")
        print("Launching Rock Paper Scissors game.")
        play_rps()
    else:
        speak("I didn't understand that command.")
        print("I didn't understand that command.")

# ----------- Main Loop -----------
if __name__ == "__main__":
    speak("Initializing Praggya.....")
    print("Initializing Praggya.....")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening.....")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
                word = recognizer.recognize_google(audio)
                if word.lower() == "pragya":
                    speak("Yes Sir, how may I help you?")
                    with sr.Microphone() as source:
                        print("Praggya Active....")
                        audio = recognizer.listen(source)
                        command = recognizer.recognize_google(audio)
                        processCommand(command)
        except Exception as e:
            print(f"Error: {e}")