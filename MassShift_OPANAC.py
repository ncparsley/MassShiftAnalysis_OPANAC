import sys

# Constants
n_mass_shifts = 1
mass_shift = 161.30
total_mass_shift = mass_shift * n_mass_shifts
tolerance = 0.05 # Da
round_digits = 3 # Cut down on the duplicate masses

def print_usage():
    print("Usage: " + sys.argv[0] + " <input_file> [<output_file>]")

def main():
    # Check the command-line arguments, quit if they're not right
    # Input file is required, output is optional
    argc = len(sys.argv)
    if argc < 2:
        print_usage()
        exit(1)

    input_filename = sys.argv[1]
    if argc < 3:
        output_filename = input_filename + ".out"
    else :
        output_filename = sys.argv[2]

    # Make sure we can read and write to the appropriate files
    input_file = open(input_filename, "r")
    output_file = open(output_filename, "w")

    # Read in the data
    original_masses = set()
    reduced_masses = set()
    for line in input_file:
        masses = line.split(',')
        if len(masses) != 2:
            # Not a real line, keep going
            continue
                
        # There might (and probably will) be more reduced-alkylated masses than
        # original masses. Only add a mass if it's actually there.
        if len(masses[0]) > 0:
            # Depending on the file, there might be text like a column header or something.
            # There's probably a more clever way to check, but for now just try to convert
            # to a float and skip otherwise.
            try:            
                original_masses.add(round(float(masses[0]), round_digits))
            except:
                pass
        if len(masses[1]) > 0:
            try:        
                reduced_masses.add(round(float(masses[1]), round_digits))
            except:
                pass
    
    # Check for possible candidates
    original_masses = sorted(original_masses)
    reduced_masses = sorted(reduced_masses)
    output_file.write("# original, deriv\n")
    for m1 in original_masses:
        for m2 in reduced_masses:
            if abs(m1 + total_mass_shift - m2) < tolerance:
                output_file.write(str(m1) + ', ' + str(m2) +'\n')
    
    # Done with our files
    input_file.close()
    output_file.close()


if __name__ == "__main__":
     main()
