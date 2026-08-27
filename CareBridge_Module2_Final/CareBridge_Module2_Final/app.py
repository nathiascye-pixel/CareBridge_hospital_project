from flask import Flask, render_template, request
from datetime import datetime, timedelta
from pathlib import Path
import json
import re

app = Flask(__name__)

DATA_FILE = Path(__file__).with_name("data.json")
PATIENT_ID_PATTERN = re.compile(r"^P\d{3}$")


def load_data():
    if not DATA_FILE.exists():
        return {
            "patients": [],
            "appointments": [],
            "triage_records": [],
            "billing_records": []
        }

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        data = {}

    return {
        "patients": data.get("patients", []),
        "appointments": data.get("appointments", []),
        "triage_records": data.get("triage_records", []),
        "billing_records": data.get("billing_records", [])
    }


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def get_patient(patients, patient_id):
    return next(
        (patient for patient in patients if patient["patient_id"] == patient_id),
        None
    )


def patients_without_appointments(data):
    booked_ids = {appointment["patient_id"] for appointment in data["appointments"]}
    return [
        patient for patient in data["patients"]
        if patient["patient_id"] not in booked_ids
    ]


def patients_with_appointments(data):
    booked_ids = {appointment["patient_id"] for appointment in data["appointments"]}
    return [
        patient for patient in data["patients"]
        if patient["patient_id"] in booked_ids
    ]


def build_time_slots():
    """Create 15-minute appointment slots from 08:00 to 18:00."""
    slots = []
    hour = 8
    minute = 0

    while hour < 18:
        slots.append(f"{hour:02d}:{minute:02d}")
        minute += 15

        if minute == 60:
            minute = 0
            hour += 1

    return slots


@app.route("/")
def home():
    data = load_data()
    waiting_count = len(patients_without_appointments(data))
    ready_count = len(patients_with_appointments(data))

    return render_template(
        "index.html",
        patient_count=len(data["patients"]),
        appointment_count=len(data["appointments"]),
        waiting_count=waiting_count,
        ready_count=ready_count
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    data = load_data()
    message = None
    error = None
    new_patient = None

    if request.method == "POST":
        patient_id = request.form.get("patient_id", "").strip().upper()
        name = request.form.get("name", "").strip()
        age_text = request.form.get("age", "").strip()
        confirm = request.form.get("confirm")

        try:
            age = int(age_text)
        except ValueError:
            age = -1

        existing_ids = {
            patient["patient_id"].upper()
            for patient in data["patients"]
        }

        if not PATIENT_ID_PATTERN.fullmatch(patient_id):
            error = "Patient ID must use the format P000: the letter P followed by exactly 3 digits."
        elif patient_id in existing_ids:
            error = f"{patient_id} is already registered. Please use a different Patient ID."
        elif name == "":
            error = "Please enter the patient's name."
        elif age <= 0 or age > 150:
            error = "Age must be a whole number from 1 to 150."
        elif confirm != "yes":
            error = "Please confirm that the patient information is correct."
        else:
            new_patient = {
                "name": name,
                "patient_id": patient_id,
                "age": age
            }

            data["patients"].append(new_patient)
            save_data(data)
            message = (
                f"{patient_id} - {name} registered successfully. "
                "The patient can now book an appointment."
            )

    return render_template(
        "register.html",
        message=message,
        error=error,
        new_patient=new_patient
    )


@app.route("/appointment", methods=["GET", "POST"])
def appointment():
    data = load_data()
    message = None
    error = None
    booking = None

    today = datetime.now().date()
    cutoff = today + timedelta(days=7)
    time_slots = build_time_slots()

    if request.method == "POST":
        patient_id = request.form.get("patient_id", "").strip()
        department = request.form.get("department", "").strip()
        appointment_date_text = request.form.get("appointment_date", "").strip()
        appointment_time = request.form.get("appointment_time", "").strip()

        available_ids = {
            patient["patient_id"]
            for patient in patients_without_appointments(data)
        }

        if patient_id not in available_ids:
            error = "Please choose a registered patient who does not already have an appointment."
        elif department not in ["GP", "Specialist"]:
            error = "Please choose either GP or Specialist."
        elif appointment_time not in time_slots:
            error = "Please choose one of the available 15-minute appointment slots."
        else:
            try:
                appointment_date = datetime.strptime(
                    appointment_date_text, "%Y-%m-%d"
                ).date()

                if appointment_date < today or appointment_date > cutoff:
                    error = "Appointment date must be from today up to 7 days ahead."
                else:
                    clash = any(
                        item["department"] == department
                        and item["date"] == appointment_date_text
                        and item["time"] == appointment_time
                        for item in data["appointments"]
                    )

                    if clash:
                        error = (
                            f"{appointment_time} on {appointment_date_text} is already booked. "
                            "Please choose another 15-minute slot."
                        )
                    else:
                        patient = get_patient(data["patients"], patient_id)

                        booking = {
                            "patient_id": patient_id,
                            "patient_name": patient["name"],
                            "department": department,
                            "date": appointment_date_text,
                            "time": appointment_time
                        }

                        data["appointments"].append(booking)
                        save_data(data)
                        message = (
                            f"Appointment confirmed for {patient_id} - {patient['name']}."
                        )
            except ValueError:
                error = "Please enter a valid appointment date."

    available_patients = patients_without_appointments(data)

    booked_slots = sorted(
        data["appointments"],
        key=lambda item: (item["date"], item["time"])
    )

    booked_by_department_date = {}
    for item in data["appointments"]:
        key = f'{item["department"]}|{item["date"]}'
        booked_by_department_date.setdefault(key, []).append(item["time"])

    return render_template(
        "appointment.html",
        message=message,
        error=error,
        booking=booking,
        available_patients=available_patients,
        booked_slots=booked_slots,
        booked_by_department_date=booked_by_department_date,
        time_slots=time_slots,
        today=today.isoformat(),
        cutoff=cutoff.isoformat()
    )


@app.route("/triage", methods=["GET", "POST"])
def triage():
    data = load_data()
    result = None
    error = None
    eligible_patients = patients_with_appointments(data)

    if request.method == "POST":
        patient_id = request.form.get("patient_id", "").strip()
        severity_text = request.form.get("severity", "").strip()

        eligible_ids = {patient["patient_id"] for patient in eligible_patients}

        if patient_id not in eligible_ids:
            error = "Please choose a patient who has already booked an appointment."
        elif not severity_text.isdigit():
            error = "Please enter a whole number between 1 and 10."
        else:
            severity = int(severity_text)

            if severity < 1 or severity > 10:
                error = "Severity level must be between 1 and 10."
            else:
                if 1 <= severity <= 4:
                    assigned_room = "Waiting Room"
                elif 5 <= severity <= 7:
                    assigned_room = "Room 1"
                else:
                    assigned_room = "Room 2"

                patient = get_patient(data["patients"], patient_id)

                result = {
                    "patient_id": patient_id,
                    "patient_name": patient["name"],
                    "severity": severity,
                    "assigned_room": assigned_room
                }

                data["triage_records"] = [
                    item for item in data["triage_records"]
                    if item["patient_id"] != patient_id
                ]
                data["triage_records"].append(result)
                save_data(data)

    return render_template(
        "triage.html",
        result=result,
        error=error,
        eligible_patients=eligible_patients
    )


@app.route("/bill", methods=["GET", "POST"])
def bill():
    data = load_data()
    result = None
    error = None
    eligible_patients = patients_with_appointments(data)

    if request.method == "POST":
        patient_id = request.form.get("patient_id", "").strip()
        patient_type = request.form.get("patient_type", "").strip()
        test_text = request.form.get("number_of_tests", "").strip()

        eligible_ids = {patient["patient_id"] for patient in eligible_patients}

        if patient_id not in eligible_ids:
            error = "Please choose a patient who has already booked an appointment."
        elif patient_type not in ["Subsidised", "Private"]:
            error = "Please choose a valid patient type."
        elif not test_text.isdigit():
            error = "Number of lab tests must be a whole number."
        else:
            number_of_tests = int(test_text)
            subtotal = 100 + (number_of_tests * 10)

            if patient_type == "Subsidised":
                total = subtotal * 0.7
            else:
                total = subtotal

            patient = get_patient(data["patients"], patient_id)

            result = {
                "patient_id": patient_id,
                "patient_name": patient["name"],
                "patient_type": patient_type,
                "number_of_tests": number_of_tests,
                "subtotal": subtotal,
                "total": total
            }

            data["billing_records"].append(result)
            save_data(data)

    return render_template(
        "bill.html",
        result=result,
        error=error,
        eligible_patients=eligible_patients
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
