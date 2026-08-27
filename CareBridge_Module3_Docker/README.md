# CareBridge Hospital Web Migration - V4

## Main workflow

Register Patient
→ Book Appointment
→ Triage + Billing

## V4 changes

### Manual Patient ID
The user types the Patient ID.

Valid examples:
- P000
- P001
- P125
- P999

Rules:
- Must begin with P
- Must contain exactly 3 digits after P
- Duplicate Patient IDs are rejected

### Appointment slots
Appointments are scheduled in 15-minute slots.

Slots:
08:00
08:15
08:30
08:45
...
17:45

Two patients cannot use the same date + exact time.
Different times on the same date are allowed.

The appointment page dynamically disables already booked times for the selected date.

### Data
Patient and appointment data is saved in data.json.

## Run locally

py -m pip install -r requirements.txt
py app.py

Open:
http://127.0.0.1:5000

## Docker

docker build -t carebridge .
docker run --name carebridge-container -p 5000:5000 carebridge

Open:
http://127.0.0.1:5000


## V5 changes

- Patient age must be from 1 to 150.
- Appointment clashes are department-specific.
- Example:
  - GP, 10:15 can be booked.
  - Specialist, 10:15 can also be booked.
  - Another GP at 10:15 on the same date is blocked.
