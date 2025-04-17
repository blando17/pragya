# pragya
Let’s walk through your code line by line and then give a summary at the end.

⸻

🔧 Imports

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

These are the required libraries:
	•	cv2: for capturing and processing video (OpenCV).
	•	time: to handle delays and timestamps.
	•	mediapipe: to detect hand landmarks.
	•	pyttsx3: for text-to-speech.
	•	random: for random computer moves in Rock Paper Scissors.
	•	sys: to exit the program.
	•	json: to read a local knowledge base.
	•	webbrowser: to open websites via voice commands.
	•	speech_recognition: to capture and recognize voice.
	•	datetime: to fetch time/date/day info.

⸻

Load Knowledge Base

with open("knowledge_base.json", "r") as f:
    knowledge = json.load(f)

Loads pre-defined question-answer pairs (like a mini chatbot knowledge set) from a local JSON file.

⸻

 Engine Setup

recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 180)

	•	recognizer: sets up voice input.
	•	engine: initializes text-to-speech.
	•	rate: controls speech speed.

⸻

🗣 Speak Function

def speak(text):
    engine.say(text)
    engine.runAndWait()

Speaks any provided text using pyttsx3.

⸻

 Gesture Detection (Rock Paper Scissors)✊✋✌️

Detect Hand Gesture

def detect_gesture(hand_landmarks):
    ...

	•	Uses MediaPipe hand landmarks.
	•	Detects finger positions to classify gesture as:
	•	Rock: all fingers down
	•	Paper: all fingers up
	•	Scissors: index and middle up
	•	Returns "rock", "paper", "scissors" or "none"

Get Winner

def get_winner(user, comp):
    ...

Compares user and computer gestures to decide winner.

Play Game

def play_rps():
    ...

	1.	Uses webcam + MediaPipe to detect gestures.
	2.	Every 5 seconds, compares user’s gesture vs random computer move.
	3.	Speaks out result and keeps score.
	4.	Ends on pressing Q.

⸻

 Command Processor

def processCommand(c):
    ...

Processes voice commands such as:
	•	Replies to known questions from JSON knowledge base.
	•	Opens websites like Google, YouTube, etc.
	•	Tries to play music from an external musiclibrary (optional).
	•	Stops the assistant.
	•	Tells time, date, day.
	•	Launches Rock Paper Scissors.
	•	Responds with fallback if command is unknown.

⸻

 Main Loop

if __name__ == "__main__":
    ...

This is the core loop of the assistant:
	1.	Speaks “Initializing Praggya”.
	2.	Listens continuously using the microphone.
	3.	Activates when it hears “Pragya”.
	4.	Then listens for a command and processes it.

⸻

⚡ Summary

This script is your all-in-one voice assistant + gesture game system. Here’s what it does:
	•	Listens for the wake word “Pragya”.
	•	Replies to known Q&A from a local JSON knowledge base.
	•	Can open popular websites on command.
	•	Recognizes spoken commands like time/date or music.
	•	Launches a Rock Paper Scissors game using webcam + hand gestures (via MediaPipe).
	•	Provides spoken feedback via text-to-speech.

