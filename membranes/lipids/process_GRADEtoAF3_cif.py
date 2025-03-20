# function to prepare a CIF file from GRADE online for AF3
# takes an inpout file as an argument and writes the output to a new 
# file called <input_file>-singleline.mmcif for AF3 input
# the script also out[uts a file called <input_file>.mmcif with the
# output in a readable format
#
# version 0.1 05/02/2025
# written by Richard Birkinshaw

#import libraries
import argparse

#function to extract top and required tables from input content
def extract_top_and_tables(input_content):
    # Initialize variables
    top_data = []
    tables = []
    current_table = []
    table_count = 0
    in_table = False

    # Iterate through the content
    for line in input_content:
        if line.startswith('data_comp'):
            continue  # Skip lines that start with "data_comp"
        if line.startswith('#'):
            if in_table:
                # End of current table
                tables.append(current_table)
                current_table = []
                table_count += 1
                in_table = False
                if table_count == 3:
                    break
            top_data.append(line)
        elif line.startswith('loop_'):
            if in_table:
                tables.append(current_table)
                current_table = []
                table_count += 1
                if table_count == 3:
                    break
            in_table = True
            current_table.append(line)
        elif in_table:
            current_table.append(line)
        else:
            top_data.append(line)

    # Append the last table if it was not appended
    if in_table and current_table:
        tables.append(current_table)

    # Combine top data and the first three tables
    output_content = top_data
    for table in tables[:3]:
        output_content.append('#\n')
        output_content.extend(table)

    return output_content

#function to append SMILES string to the end of the input content. Hote this will not be needed with up to date version of AF3
def smilesappend_cif_file(input_content):
    # Extract the SMILES string from the line starting with '# GEN: from SMILES'
    smiles_line = None
    for line in input_content:
        if line.startswith('# GEN: from SMILES'):
            smiles_line = line.strip()
            break

    if smiles_line:
        # Extract the SMILES string
        smiles_string = smiles_line.split(' ')[-1]
        # Replace any '\' characters in the SMILES string with '\\'
        smiles_string = smiles_string.replace('\\', '\\\\')

        # Create the formatted SMILES string
        formatted_smiles = (
            "#\n"
            "_pdbx_chem_comp_descriptor.type SMILES\n"
            f"_pdbx_chem_comp_descriptor.descriptor '{smiles_string}'\n"
        )

        # Append the formatted SMILES string to the content
        input_content.append(formatted_smiles)

    # Return the reformatted output
    return input_content

#function to remove the first table from the input content and header
def remove_before_second_table(content):
    # Initialize variables
    table_count = 0
    output_content = []
    in_table = False

    # Iterate through the content
    for line in content:
        if line.startswith('loop_'):
            table_count += 1
            in_table = True
        if table_count >= 2:
            output_content.append(line)
        elif in_table and table_count == 1:
            continue  # Skip lines of the first table

    return output_content

#function to replace the strings in the input content
def replace_strings(content):
    replacements = {
        "_chem_comp_atom.pdbx_stereo_config": "_chem_comp_atom.pdbx_leaving_atom_flag",
        "_chem_comp_atom.x ": "_chem_comp_atom.pdbx_model_Cartn_x_ideal",
        "_chem_comp_atom.y ": "_chem_comp_atom.pdbx_model_Cartn_y_ideal",
        "_chem_comp_atom.z ": "_chem_comp_atom.pdbx_model_Cartn_z_ideal",
        "_chem_comp_bond.type": "_chem_comp_bond.value_order",
        "_chem_comp_bond.aromatic": "_chem_comp_bond.pdbx_aromatic_flag"
    }
    
    output_content = []
    for line in content:
        for old, new in replacements.items():
            line = line.replace(old, new)
        output_content.append(line)
    
    return output_content

#function to replace the strings in the input content for the second table
def ensure_seventh_column(content):
    output_content = []
    in_first_table = False
    table_count = 0

    for line in content:
        if line.startswith('loop_'):
            table_count += 1
            if table_count == 1:
                in_first_table = True
            else:
                in_first_table = False

        if in_first_table and not line.startswith('_'):
            columns = line.split()
            if len(columns) >= 7:
                # Find the start index of the 7th column
                start_index = line.find(columns[6])
                # Replace the 7th column with 'N' while keeping the padding
                line = line[:start_index] + 'N' + line[start_index + 1:]
        
        output_content.append(line)
    
    return output_content

#function to replace the strings in the input content for the third table
def process_second_table(content):
    output_content = []
    in_second_table = False
    table_count = 0

    replacements = {
        "single": "SING",
        "double": "DOUB",
        "aromatic": "AROM",
        "triple": "TRIP"
    }

    for line in content:
        if line.startswith('loop_'):
            table_count += 1
            if table_count == 2:
                in_second_table = True
            else:
                in_second_table = False

        if in_second_table and not line.startswith('_'):
            columns = line.split()
            if len(columns) >= 5:
                # Replace the fourth column strings
                if columns[3] in replacements:
                    start_index = line.find(columns[3])
                    line = line[:start_index] + replacements[columns[3]] + line[start_index + len(columns[3]):]
                # Capitalize the fifth column
                start_index = line.find(columns[4])
                line = line[:start_index] + columns[4].upper() + line[start_index + len(columns[4]):]
        
        output_content.append(line)
    
    return output_content

#function to input the first table in the correct format for AF3
#note returns two variables, the first is the content with the prepended text
def prepstart_text(content):
    # Extract comp_id from the first item in the first table after the lines starting with "_" and "loop_"
    comp_id = None
    for line in content:
        if not line.startswith('_') and not line.startswith('loop_') and line.strip():
            comp_id = line.split()[0]
            break

    if comp_id is None:
        raise ValueError("comp_id not found in the first table")

    # Derive comp_name from comp_id by removing "mom"
    comp_name = comp_id.replace("mom", "")

    prepend_content = (
        f"data_{comp_id}\n"
        "#\n"
        f"_chem_comp.id {comp_id}\n"
        f"_chem_comp.name {comp_name}\n"
        "_chem_comp.type non-polymer\n"
        "_chem_comp.formula ?\n"
        "_chem_comp.mon_nstd_parent_comp_id ?\n"
        "_chem_comp.pdbx_synonyms ?\n"
        "_chem_comp.formula_weight ?\n"
        "#\n"
    )
    return prepend_content.splitlines(keepends=True) + content, comp_id


#main function to call all the functions and write the output to a file
def main(input_file):
    output_filename = input_file.split('.')[0] + ".mmcif"
    output_SL_filename = input_file.split('.')[0] + "-singleline.mmcif"

    # Read the input file
    with open(input_file, 'r') as file:
        input_content = file.readlines()

    # Process the content with the required functions
    #extract the AF3 reuired tables
    tables_extracted = extract_top_and_tables(input_content)
    #append smiles to the end of the file (not needed with up to date version of AF3)
    smiles_appended = smilesappend_cif_file(tables_extracted)
    #remove all tables not needed from the start of the file
    remove_table1 = remove_before_second_table(smiles_appended)
    #replace table headers to the AF3 required headers
    strings_replaced = replace_strings(remove_table1)
    # Process the content with other functions as needed
    # Ensure the 7th column in the first table has an "N" character
    caps_table1 = ensure_seventh_column(strings_replaced)
    # Process the second table
    second_table_fixed = process_second_table(caps_table1)
    # Prepend the specified text to the start of the file and get comp_id
    final_content, comp_name = prepstart_text(second_table_fixed)
    # Join the list into a single line with no delimiter
    single_line = ''.join(final_content).replace('\n', '\\n')

    # Write the readable output file
    with open(output_filename, 'w') as file:
        file.writelines(final_content)

    # Write the single-line output file
    with open(output_SL_filename, 'w') as file:
        file.write(single_line)

    print(f"{input_file} processed and AF3 input written to {output_SL_filename}")
    print(f"a readable version is written to {output_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a CIF file.")
    parser.add_argument("input_file", help="Path to the input CIF file")
    args = parser.parse_args()
    main(args.input_file)
