import re

# Create a mapping of month names to numerical values
month_mapping = {
    'jan': '1',
    'feb': '2',
    'mar': '3',
    'apr': '4',
    'may': '5',
    'jun': '6',
    'jul': '7',
    'aug': '8',
    'sep': '9',
    'oct': '10',
    'nov': '11',
    'dec': '12',
    # Add more entries as needed to match your month names
    # 'your_month_name': 'numerical_value',
}

input_file = 'My Collection.bib'
output_file = 'your_output.bib'  # Change the output file name

# Open the input and output files
with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    entry = []
    abstract_started = False
    file_field_started = False
    author_field_started = False
    curly_brace_count = 0

    for line in infile:
        # Replace the (U+2009) character with a space
        line = line.replace('\u2009', ' ')
        # Replace the (U+0327) character with a space
        line = line.replace('\u0327', ' ')

        # Check if the line starts with "month = {" and contains a valid month name
        if line.strip().startswith('month = {') and '}' in line:
            # Extract the month value and replace it with the numerical value
            month_value = line.split('{', 1)[1].split('}', 1)[0].strip().lower()
            numerical_month = month_mapping.get(month_value, month_value)
            line = line.replace(month_value, numerical_month)

        if line.strip().startswith('abstract = {'):
            abstract_started = True
            curly_brace_count = 1
            entry.append(line)
            continue
        elif line.strip().startswith('file = {'):
            file_field_started = True
            continue
        elif re.match(r'^\s*author\s*=', line):
            author_field_started = True
            entry.append(line)
            continue
        elif abstract_started:
            entry.append(line)
            curly_brace_count += line.count('{') - line.count('}')
            if curly_brace_count == 0:
                abstract_started = False
                # Write the preserved abstract field lines to the output file
                outfile.writelines(entry)
                entry = []
            continue
        elif file_field_started and line.strip().endswith('},'):
            file_field_started = False
            continue
        elif author_field_started:
            entry.append(line)
            if line.strip().endswith('},'):
                author_field_started = False
                # Write the preserved author field lines to the output file
                outfile.writelines(entry)
                entry = []
            continue

        outfile.write(line)

print(f"Abstracts and file fields removed. (U+2009) and (U+0327) replaced with space. Output saved to '{output_file}'")
