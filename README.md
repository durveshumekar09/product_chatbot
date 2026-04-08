# Product Recommendation Chatbot

A simple web chatbot built with Flask. It recommends laptops and phones based on user budget and category.

---

## Features
- Clean chat interface
- Supports two product categories: phone and laptop
- Recommends products within user-defined budget
- Option to explore more suggestions

---

## Approach
- Flask backend handles chat logic and session state
- Frontend HTML simulates a chat interface
- Conversation flow:
  1. Bot greets user and asks for product category
  2. User enters category (phone/laptop)
  3. Bot asks for budget
  4. Bot recommends products within budget
  5. User can ask for more suggestions or end chat
- Session state ensures smooth conversation and tracks user choices

---

## Setup Instructions

1. **Create Project Folder**  
   ```bash
   mkdir chatbot_app
   cd chatbot_app

2. Install dependencies 
  - pip install flask flask-cors
3. Run the App
  - python app.py
4.Open in Browser
Go to: http://127.0.0.1:5000/
Start chatting with the bot

## Please refer action.png to see chatbot in action
   
