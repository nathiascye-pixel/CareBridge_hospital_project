def assign_triage_room():
    valid_input = False

    while not valid_input:
        severity_input = input("Enter severity of condition (1 to 10): ")

        if severity_input.isdigit():
            severity = int(severity_input)
            if 1 <= severity <= 10:
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


# Run the function
assign_triage_room()