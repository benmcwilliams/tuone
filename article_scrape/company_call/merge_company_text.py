# List of input text files
input_files = ["ACC.txt", "catl.txt", "volkswagen.txt",
               "SVOLT.txt", "tesla.txt", "varta.txt"] 

# Output concatenated text file
output_file = "concatenated.txt"  # Replace with the desired output file path

try:
    # Open the output file in write mode
    with open(output_file, 'w') as outfile:
        for input_file in input_files:
            # Open each input file in read mode
            with open(input_file, 'r') as infile:
                # Read the contents of the input file and write it to the output file
                outfile.write(infile.read())
                # Add a newline between the contents of different input files
                outfile.write("\n")
    print(f"Concatenated text saved to {output_file}")
except FileNotFoundError:
    print("One or more input files not found.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
