from read import read_data_from_file
import operation

def main():
    """Main function to run the program."""

    main_loop = True
    land_data = read_data_from_file("land_data.txt")
    
    while main_loop:
        # Display main menu
        print("\n")
        print("\t\t\tTechno Property Nepal")
        print("\n")
        print("\t\tKamalpokhari, Kathmandu   |    Contact no: 9841111111")
        print("-----------------------------------------------------------------------------------------------------------------------")
        print("\n\t\t\tWelcome to TechnoPropertyNepal!")
        print("\n")
        print("Kitta \t City\t\tDirection \t     Anna  \t      Price  \tAvailability")
        print("--------------------------------------------------------------------------------------------------------------------")
        
        # Display land data
        for kitta, values in sorted(land_data.items()):
            if len(values) == 5:
                city, direction, anna, price, availability = values
                print(kitta + "\t" + city + "      \t" + direction + "  \t     " + anna + "     \t       " + price + "  \t  " + availability)
            else:
                print(f"Invalid data format for kitta number {kitta}")
        
        # Show options
        print("\nSelect the option:\n")
        print("1. Rent a land")
        print("2. Return a land")
        print("3. Exit\n")
        
        user_input = input("Select an option: ")

        if user_input == '1':
            # Rent loop
            rent_another = 'yes'
            while rent_another.lower() == 'yes':
                operation.rent_land()  # Rent a single land
                rent_another = input("Do you want to rent another land? (yes/no): ")
            # When 'no', loop ends and main menu is displayed again

        elif user_input == '2':
            operation.return_land()  # Return a land
            
        elif user_input == '3':
            main_loop = False
            print("Thank you for using TechnoPropertyNepal!")
            
        else:
            print("Invalid input. Please try again.")    

if __name__ == "__main__":
    main()
