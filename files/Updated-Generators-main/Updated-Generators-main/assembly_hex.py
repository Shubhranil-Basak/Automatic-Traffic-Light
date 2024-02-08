with open('assembly.txt', 'r') as file:
    assembly_code = file.read()

lines = assembly_code.split('\n')
hex_codes =[]
for line in lines[7:]:
    # Split the line into words
    words = line.split()

    # Check if there are at least 2 words in the line
    if len(words) >= 2:
        # Get the 2nd word as the hex code
        hex_code = words[1]
        hex_codes.append(hex_code)
with open('assembly_hex.txt', 'w') as hex_file:
    hex_file.write("00000000\n00000000\n")
    for hex_value in hex_codes:
        if (hex_value[0] != "<"):
            hex_file.write(hex_value + '\n')
    
    hex_file.write("ffffffff\nffffffff\n")


