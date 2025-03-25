# Open the input text file in read mode
with open('IHP.cif', 'r') as file:
    content = file.read()

# Replace each newline character with the string '\n'
modified_content = content.replace('\n', '\\n')

# Write the modified content to a new output file
with open('IHP-singleline.txt', 'w') as file:
    file.write(modified_content)