from datetime import datetime, timedelta

def book_appointment():
    # 1. Initialize System Date
    current_date = datetime.now()
    cutoff_date = current_date + timedelta(days=7)

    # 2. Department Input Loop
    department_name = input("Enter department (GP or Specialist): ").strip()

    while department_name not in ["GP", "Specialist"]:
        print("Invalid Department staff please try again")
        department_name = input("Enter department (GP or Specialist): ").strip()

    # 3. Appointment Date Input Loop
    appointment_date_input = input("Enter preferred appointment date (YYYY-MM-DD): ").strip()

    # Helper function to check if the date format is valid and > 7 days away
    def is_valid_date(date_str):
        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
            return parsed_date > cutoff_date
        except ValueError:
            return False

    # Loop until input passes validation
    while not is_valid_date(appointment_date_input):
        print("Invalid Date please try again")
        appointment_date_input = input("Enter preferred appointment date (YYYY-MM-DD): ").strip()

    # 4. Booking Confirmation
    print("Booking is confirmed")

# Run the program
book_appointment()