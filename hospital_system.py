from datetime import datetime, timedelta


# ---------------------------------------------------------
# Constants (fixed values used across the system)
# ---------------------------------------------------------
PATIENT_ID_LENGTH = 4           # Expected length of a valid Patient ID
VALID_DEPARTMENTS = ["GP", "Specialist"]
MIN_DAYS_AHEAD = 7              # Appointments must be booked more than 7 days ahead
DATE_FORMAT = "%Y-%m-%d"

BASE_CONSULTATION_FEE = 100     # Flat consultation fee
LAB_TEST_RATE = 10              # Cost per lab test
SUBSIDISED_DISCOUNT = 0.70      # Subsidised patients pay 70% of subtotal

MIN_SEVERITY = 1
MAX_SEVERITY = 10


# ---------------------------------------------------------
# 1. Patient Registration
# ---------------------------------------------------------
def register_patient():
    print("Enter patient's details")

    while True:
        name = input("Enter name: ")
        patient_id = input("Enter Patient ID: ")

        try:
            age = int(input("Enter age: "))
        except ValueError:
            print("Invalid input. Age must be a number.")
            continue

        if name == "":
            print("Invalid input. Name cannot be blank.")
        elif age <= 0:
            print("Invalid input. Age must be a positive number.")
        elif not (patient_id.isdigit() and len(patient_id) == PATIENT_ID_LENGTH):
            print(f"Invalid input. Patient ID must be exactly {PATIENT_ID_LENGTH} digits.")
        else:
            break

    print("Please confirm patient information")
    print("Name:", name)
    print("Age:", age)
    print("Patient ID:", patient_id)

    confirm = input("Confirm information? (yes/no): ")

    if confirm.lower() == "yes":
        print("Patient registered successfully")
    else:
        register_patient()


# ---------------------------------------------------------
# 2. Book Appointment
# ---------------------------------------------------------
def book_appointment():
    # 1. Initialize System Date
    current_date = datetime.now()
    cutoff_date = current_date + timedelta(days=MIN_DAYS_AHEAD)

    # 2. Department Input Loop
    department_name = input("Enter department (GP or Specialist): ").strip()

    while department_name not in VALID_DEPARTMENTS:
        print("Invalid Department staff please try again")
        department_name = input("Enter department (GP or Specialist): ").strip()

    # 3. Appointment Date Input Loop
    appointment_date_input = input("Enter preferred appointment date (YYYY-MM-DD): ").strip()

    # Helper function to check if the date format is valid and > 7 days away
    def is_valid_date(date_str):
        try:
            parsed_date = datetime.strptime(date_str, DATE_FORMAT)
            return parsed_date > cutoff_date
        except ValueError:
            return False

    # Loop until input passes validation
    while not is_valid_date(appointment_date_input):
        print("Invalid Date please try again")
        appointment_date_input = input("Enter preferred appointment date (YYYY-MM-DD): ").strip()

    # 4. Booking Confirmation
    print("Booking is confirmed")


# ---------------------------------------------------------
# 3. Calculate Bill
# ---------------------------------------------------------
def CalculateBill():
    # Input and validate Patient Type
    while True:
        PatientType = input("Enter Patient Type (Subsidised or Private): ")

        if PatientType == "Subsidised" or PatientType == "Private":
            break
        else:
            print("Invalid. Try again.")

    # Input and validate Number of Tests
    while True:
        NumberOfTest = input("Enter Number of Lab Tests: ")

        if NumberOfTest.isdigit():
            NumberOfTest = int(NumberOfTest)
            break
        else:
            print("Invalid. Try again.")

    # Calculate subtotal
    Subtotal = BASE_CONSULTATION_FEE + (NumberOfTest * LAB_TEST_RATE)

    # Calculate total
    if PatientType == "Subsidised":
        Total = Subtotal * SUBSIDISED_DISCOUNT
    else:
        Total = Subtotal

    # Display result
    print("Patient Type:", PatientType)
    print("Total Amount to Pay: $", format(Total, ".2f"))


# ---------------------------------------------------------
# 4. Assign Triage Room
# ---------------------------------------------------------
def assign_triage_room():
    valid_input = False

    while not valid_input:
        severity_input = input("Enter severity of condition (1 to 10): ")

        if severity_input.isdigit():
            severity = int(severity_input)
            if MIN_SEVERITY <= severity <= MAX_SEVERITY:
                valid_input = True
            else:
                print(
                    "Error: Invalid input. Please enter a whole number between 1 and 10."
                )
        else:
            print(
                "Error: Invalid input. Please enter a whole number between 1 and 10."
            )

    if 1 <= severity <= 4:
        assigned_room = "Waiting Room"
    elif 5 <= severity <= 7:
        assigned_room = "Room 1"
    elif 8 <= severity <= 10:
        assigned_room = "Room 2"

    print("\n--- Triage Summary ---")
    print(f"Severity Level: {severity}")
    print(f"Assigned Location: {assigned_room}")


# ---------------------------------------------------------
# Main Menu
# ---------------------------------------------------------
def main_menu():
    while True:
        print("\n===== Hospital System Menu =====")
        print("1. Register Patient")
        print("2. Book Appointment")
        print("3. Calculate Bill")
        print("4. Assign Triage Room")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            register_patient()
        elif choice == "2":
            book_appointment()
        elif choice == "3":
            CalculateBill()
        elif choice == "4":
            assign_triage_room()
        elif choice == "5":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


# Run the program
if __name__ == "__main__":
    main_menu()
