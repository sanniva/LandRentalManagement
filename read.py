def read_data_from_file(landdata):
    
    """Read land data from a file and return as a dictionary."""
    
    land_data = {}  # Initialize an empty dictionary to store land data
    with open("landdata.txt", "r") as f:
        for line in f:
            line_data = line.strip().split(", ")
            if len(line_data) >= 6:
                kitta_number = line_data[0]
                other_data = line_data[1:]
                land_data[kitta_number] = other_data
            else:
                print(f"Invalid data format in line: {line.strip()}")
    return land_data
