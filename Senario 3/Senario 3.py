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
    Subtotal = 100 + (NumberOfTest * 10)

    # Calculate total
    if PatientType == "Subsidised":
        Total = Subtotal * 0.7
    else:
        Total = Subtotal

    # Display result
    print("Patient Type:", PatientType)
    print("Total Amount to Pay: $", format(Total, ".2f"))


CalculateBill()