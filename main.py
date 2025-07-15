from read import read_data_from_file
import operation

def main():
    
    """ Main function to run the program."""
    
    main_loop = True
    land_data = read_data_from_file("land_data.txt")
    
    while main_loop:
        print("\n")
        print("\t  \t \t   Techno Property Nepal")
        print("\n")
        print("\t  \t  Kamalpokhari ,Kathmandu   |    Contact no:9841111111")
        print("-----------------------------------------------------------------------------------------------------------------------")
        print("\n  \t  \t        Welcome to TechnoPropertyNepal!")
        print("\n")
        print("Kitta \t City\t\tDirection \t     Anna  \t      Price  \tAvailability")
        print("--------------------------------------------------------------------------------------------------------------------")
            
        #Displaying land data
        for kitta, values in sorted(land_data.items()):
            if len(values) == 5:
                city, direction, anna, price, availability = values
                print(kitta + "\t" + city + "      \t" + direction + "  \t     " + anna + "     \t       " + price + "  \t  " + availability)
            else:
                print(f"Invalid data format for kitta number {kitta}")
        print("\n")
        print(" Select the option:")
        print("\n")
        print("1. Rent a land")
        print("2. Return a land")
        print("3. Exit")
        print("\n")
        
        user_input = input("Select an option: ")

        if user_input == '1':
            operation.rent_land()  # Calling function to rent a land

        elif user_input == '2':
            operation.return_land()  # Calling function to return a land
            
        elif user_input == '3':
            main_loop = False
            print("Thank you for using TechnoPropertyNepal!")
        else:
            print("Invalid input. Please try again.")    

if __name__ == "__main__":
    main() 
