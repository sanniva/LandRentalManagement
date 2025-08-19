from datetime import datetime
import os

INVOICE_FILE = "rent_invoice.txt"


def generate_invoice(customer_name, contact_number, current_datetime, rented_lands, land_data):

    """Generate a rental invoice for the customer."""
    
    with open("rent_land.txt", "w") as file:
        file.write("\n")
        file.write("\t  \t \t   Techno Property Nepal\n")
        file.write("\n")
        file.write("\t  \t  Kamalpokhari ,Kathmandu     |    Contact no:9841111111\n")
        file.write("--------------------------------------------------------------------------------------------------------------------\n")
        file.write("Customer Details\n")
        file.write("--------------------------------------------------------------------------------------------------------------------\n")
        file.write(f"Name of the customer : {customer_name}\n")
        file.write(f"Contact Number: {contact_number}\n")
        file.write(f"Date and Time: {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write("--------------------------------------------------------------------------------------------------------------------\n")
        file.write("Purchase Details\n")
        file.write("--------------------------------------------------------------------------------------------------------------------\n")
        file.write("Kitta \t City\t          Direction \t     Anna  \t      Price \t         Month  \tTotal\n")
        file.write("--------------------------------------------------------------------------------------------------------------------\n")
        total_rental_cost = 0

        # Writing rented land details
        for desired_land, desired_month, _, _ in rented_lands:
            city, direction, anna, price, _ = land_data[desired_land]
            total_cost = int(price) * desired_month
            total_rental_cost += total_cost
            file.write(f"{desired_land}\t{city}       \t{direction}       \t     {anna}        \t       {price}       \t   {desired_month}     \t {total_cost}\n")
        
        file.write("--------------------------------------------------------------------------------------------------------------------\n")
        file.write(f"\nGrand Total Rental Cost: {total_rental_cost}\n")

    print("Rental invoice generated successfully!")

def generate_return_invoice(customer_name, return_date, returned_lands_invoice, total_fine,grand_total):

    """Generate a return invoice for the customer."""
    
    with open("return_invoice.txt", "w") as file:
        file.write("\n")
        file.write("\t  \t \t   Techno Property Nepal\n")
        file.write("\n")
        file.write("\t  \t  Kamalpokhari ,Kathmandu    |    Contact no:9841111111\n")
        file.write("--------------------------------------------------------------------------------------------------------------------\n")
        file.write("\nReturn Invoice:\n")
        file.write("*******************\n")
        
       
        file.write("Customer Details\n")
        file.write("--------------------------------------------------------------------------------------------------------------------\n")
        file.write(f"Name of the customer : {customer_name}\n")
        file.write(f"Date and Time: {return_date.strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write("--------------------------------------------------------------------------------------------------------------------\n")
        file.write("Purchase Details\n")
        file.write("--------------------------------------------------------------------------------------------------------------------\n")
        file.write("Kitta \t City\t          Direction \t     Anna  \t      Price \t         Month  \tTotal\n")
        file.write("--------------------------------------------------------------------------------------------------------------------\n")

        # Writing returned land invoice details
        for invoice in returned_lands_invoice:
            kitta, city, direction, anna, price, rented_month, total_cost_kitta, fine_amount = invoice
            file.write(f"{kitta}\t{city}     \t  {direction}       \t      {anna}        \t       {price}       \t    {rented_month}          \t{total_cost_kitta}\n")
        file.write("--------------------------------------------------------------------------------------------------------------------\n")
        file.write(f"\nGrand Total Rental Cost: {grand_total}\n")
    print("Return invoice(s) generated successfully!")


def update_land_availability(land_kitta, availability):
    """Update the availability of a land."""

    file_name = "landdata.txt"
    temp_file_name = "temp_land_data.txt"

    # Opens the original file to read and temporary file to write
    with open(file_name, 'r') as file, open(temp_file_name, 'w') as temp_file:
        for line in file:
            data = line.strip().split(', ')
            if data[0] == land_kitta:
                data[-1] = availability
                line = ', '.join(data) + '\n'
            temp_file.write(line)
    
    # Replace the original file with the temporary file
    import os
    os.replace(temp_file_name, file_name)
