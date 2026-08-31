# CareBridge Hospital - Module 2 Simple V9

## Patient flow
1. Register Patient
2. Appointment
3. Billing
4. Triage

## Appointment rules
- Select a patient
- Select GP or Specialist
- Select an appointment date
- No appointment time is used
- Appointment date must be MORE THAN 7 days from the current date
- A date 7 days away or less is invalid

Example:
If today is 31 August:
- 1 September to 7 September = invalid
- 8 September onward = valid

## Other rules
- Patient ID format: P000
- Patient age: 1 to 150
- A registered patient can only have one appointment in this prototype
- Billing and Triage only show patients who have an appointment

## Run
py -m pip install -r requirements.txt
py app.py

Open:
http://127.0.0.1:5000
