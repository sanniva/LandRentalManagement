from read import read_data_from_file
from datetime import datetime
from write import generate_invoice, generate_return_invoice, update_land_availability

def generate_bill(land_data, rented_lands):

    """Calculate the total rental cost for the rented lands."""
    
    total_cost = 0
    for desired_land, desired_month, _, _ in rented_lands:
        city, direction, anna, price, _ = land_data[desired_land]
        total_cost += int(price) * desired_month
    print("Total Cost:", total_cost)
    return total_cost

def print_available_lands(land_data):

    """ Print the details of available lands."""
    
    print("\nAvailable Lands:")
    print("\n")
    print("Kitta \t City\t\tDirection \t     Anna  \t      Price  \tAvailability")
    print("-------------------------------------------------------------------------------------------------------------------------")
    available_lands = []

    for kitta, values in sorted(land_data.items()):
        city, direction, anna, price, availability = values
        if availability == "Available":
            available_lands.append({"kitta_number": kitta, "city": city, "direction": direction, "anna": anna, "price": price})
            print(kitta + "\t" + city + "      \t" + direction + "  \t     " + anna + "     \t       " + price + "  \t  " + availability)
        else:
            print(f"Sorry, kitta number {kitta} is not available")
    return available_lands  # Return the list of available lands

def rent_land():
    
    """Rent a land based on user input and generate invoices."""
    
    current_datetime = datetime.now()
    land_data = read_data_from_file("land_data.txt")
    available_lands = print_available_lands(land_data)

    total_rental_cost = 0  # Track the total rental cost for all lands rented
    rented_lands = []

    while True:
        try:
            print("\n")
            customer_name = input("Enter your name: ")
            if not customer_name.isalpha():
                print("Invalid input. Please enter alphabetic characters only.")
                continue
            desired_land = input("\nEnter the desired land Kitta number: ")
            desired_month_str = input("Enter the desired number of months: ")
            contact_number = input("Enter your contact number: ")

            if desired_land not in land_data:
                print("Invalid land Kitta number. Please try again.")
                continue

            city, direction, anna, price, availability = land_data[desired_land]

            if availability != "Available":
                print("The desired land is not available. Please choose another land.")
                continue

            if not desired_month_str.isdigit() or int(desired_month_str) <= 0 or int(desired_month_str) > 12:
                print("Number of months must be a positive integer less than or equal to 12.  Please try again.")
                continue
            desired_month = int(desired_month_str)

            if not contact_number.isdigit():
                print("Invalid contact number format. Please enter a valid contact number.")
                continue

            if (desired_land, customer_name) in [(land[0], land[3]) for land in rented_lands]:
                print("You have already rented this land. Please choose another land.")
                continue
            
            # Update availability of rented land to "Not Available"
            update_land_availability(desired_land, "Not Available")

            rented_lands.append((desired_land, desired_month, contact_number, customer_name))

            another_land = input("Do you want to rent another land? (yes/no): ")
            if another_land.lower() == "no":
                break

        except Exception as e:
            print("Error occurred:", e)

    total_rental_cost = generate_bill(land_data, rented_lands)

    generate_invoice(customer_name, contact_number, current_datetime, rented_lands, land_data)

    print("\n")
    print("\t  \t \t   Techno Property Nepal")
    print("\n")
    print("\t  \t  Kamalpokhari ,Kathmandu     |    Contact no:9841111111")
    print("--------------------------------------------------------------------------------------------------------------------")
    print("Customer Details")
    print("--------------------------------------------------------------------------------------------------------------------")
    print("Name of the customer :", customer_name)
    print("Contact Number:", contact_number)
    print("Date and Time:", current_datetime.strftime("%Y-%m-%d %H:%M:%S"))
    print("--------------------------------------------------------------------------------------------------------------------")
    print("Purchase Details")
    print("--------------------------------------------------------------------------------------------------------------------")
    print("Kitta \t City\t               Direction \t        Anna  \tPrice   \t Month  \tTotal\n")
    print("--------------------------------------------------------------------------------------------------------------------")
    for desired_land, desired_month, _, _ in rented_lands:
        city, direction, anna, price, _ = land_data[desired_land]
        total_cost = int(price) * desired_month
        print(f"{desired_land}\t{city}     \t   {direction}    \t     {anna}      \t    {price}    \t{desired_month}\t{total_cost}\n")
    print("--------------------------------------------------------------------------------------------------------------------")


    # Display the grand total
    print("\nGrand Total Rental Cost:", total_rental_cost)
    
def calculate_fine(rent_start_date, return_date, total_cost, rented_month):

    """ Calculate fine for late return."""

    # Calculate the total number of months rented
    total_months_rented = (return_date.year - rent_start_date.year) * 12 + return_date.month - rent_start_date.month

    # Check if the rented period exceeds the provided number of rented months
    if total_months_rented > rented_month:
        # Calculate the number of months exceeded
        months_exceeded = total_months_rented - rented_month
        # Calculate the fine (10% of the total cost per month)
        fine_amount = int(total_cost * 0.1 * months_exceeded)
        return fine_amount
    else:
        return 0

def return_land():
    current_datetime = datetime.now()
    land_data = read_data_from_file("land_data.txt")
    return_invoices = []

    while True:
        while True:
            desired_lands_input = input("\nEnter the kitta number(s) of the land(s) being returned (separated by commas or spaces): ")
            desired_lands = [kitta.strip() for kitta in desired_lands_input.replace(',', ' ').split()]

            invalid_kittas = [kitta for kitta in desired_lands if kitta not in land_data]
            if invalid_kittas:
                print("Invalid land kitta number(s):", ", ".join(invalid_kittas))
                continue

            all_available = all(land_data[kitta][-1] == "Available" for kitta in desired_lands)
            if all_available:
                print("All the selected lands are already available. No return needed.")
                continue
            else:
                break

        customer_name = input("Enter your name: ")

        # Prompt user for the number of months the land was rented
        while True:
            rented_month_str = input("Enter the number of months the land was rented: ")
            if not  rented_month_str.isdigit() or int( rented_month_str) <= 0 or int( rented_month_str) > 12:
                print("Number of months must be a positive integer less than or equal to 12. Please try again.")
            else:
                rented_month = int(rented_month_str)
                break

        rent_start_date_str = input("Enter the rent start date (YYYY-MM-DD): ")
        
        try:
            rent_start_date = datetime.strptime(rent_start_date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
            return

        return_date = datetime.now()

        total_cost = 0
        total_fine = 0
        returned_lands_invoice = []

        for kitta in desired_lands:
            city, direction, anna, price, availability = land_data[kitta]
            
            # Calculate rent duration in months
            rent_duration_years = return_date.year - rent_start_date.year
            rent_duration_months = return_date.month - rent_start_date.month
            total_rent_months = rent_duration_years * 12 + rent_duration_months

            if total_rent_months < rented_month:
                print(f"Invalid number of months rented for kitta {kitta}. The provided number of months is greater than the actual rental duration.")
                continue

            total_cost_kitta = int(price) * rented_month
            
            # Checks for late return and calculate fine if applicable
            fine_amount = calculate_fine(rent_start_date, return_date, total_cost_kitta, rented_month)
            total_fine += fine_amount

            # Update availability of returned land
            update_land_availability(kitta, "Available")

            total_cost += total_cost_kitta


            # Prepare invoice details for this returned land
            returned_lands_invoice.append((kitta, city, direction, anna, price, rented_month, total_cost_kitta, fine_amount))

        # Calculate grand total including fine
        grand_total = total_cost + total_fine

        # Store the invoice details for all returned lands
        return_invoices.append((customer_name, return_date, returned_lands_invoice))

        another_return = input("Do you want to return another land? (yes/no): ")
        if another_return.lower() != 'yes':
            break

   # Generate and save return invoices to file
    for customer_name, return_date, returned_lands_invoice in return_invoices:
        generate_return_invoice(customer_name, return_date, returned_lands_invoice,total_fine, grand_total)

    


    # Print all return invoices together
    print("Return invoice(s) generated successfully:")
    print("\n")
    print("\t  \t \t   Techno Property Nepal")
    print("\n")
    print("\t  \t  Kamalpokhari ,Kathmandu    |    Contact no:9841111111")
    print("--------------------------------------------------------------------------------------------------------------------")
    print("\nReturn Invoice:")
    print("*******************")
    
    for customer_name, return_date, returned_lands_invoice in return_invoices:
        print("Customer Details")
        print("--------------------------------------------------------------------------------------------------------------------")
        print("Name of the customer :", customer_name)
        print("Date and Time:", return_date.strftime("%Y-%m-%d %H:%M:%S"))
        print("Fine Amount :", fine_amount)
        print("--------------------------------------------------------------------------------------------------------------------")
        print("Purchase Details")
        print("--------------------------------------------------------------------------------------------------------------------")
        print("Kitta \t City\t          Direction \t     Anna  \t      Price \t         Month  \tTotal\n")
        print("--------------------------------------------------------------------------------------------------------------------")
        for invoice in returned_lands_invoice:
            kitta, city, direction, anna, price, rented_month, total_cost_kitta, fine_amount = invoice
            print(f"{kitta}\t{city}     \t {direction}    \t     {anna}  \t   {price}    \t{rented_month}   \t{total_cost_kitta}\n")
        print("--------------------------------------------------------------------------------------------------------------------")
        print("Grand Total Cost (including fine):", grand_total)
