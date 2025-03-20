# Open the input text file in read mode
with open('af3_momPI.mmcif', 'r') as file:
    content = file.read()

# Replace each newline character with the string '\n'
modified_content = content.replace('\n', '\\n')

# Write the modified content to a new output file
with open('af3_momPI-singleline.txt', 'w') as file:
    file.write(modified_content)