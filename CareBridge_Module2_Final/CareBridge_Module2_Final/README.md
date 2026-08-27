# CareBridge Hospital Web Migration - Module 2

## Features
- Patient registration with manually entered IDs in P000 format
- Patient age validation from 1 to 150
- Appointment booking using 15-minute time slots
- GP and Specialist have separate slot availability
- Duplicate appointment slot prevention by department + date + time
- Triage assignment
- Billing calculator
- Patient and appointment data stored in data.json

## Architecture
Browser / HTML / CSS
        ↓
Flask
        ↓
Python backend
        ↓
Validation and business logic
        ↓
data.json
        ↓
Result displayed in browser

## Run the project
Open a terminal in this folder and run:

py -m pip install -r requirements.txt
py app.py

Then open:
http://127.0.0.1:5000

## Project
Programming 1 - Project Part B
Module 2: Web Redesign & AI Refactoring
