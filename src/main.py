import os
import PyPDF2
import re
import json  # Import the json module
from collections import defaultdict

# Specify the directory containing PDF files
pdf_directory = "pdfs/"

# Initialize an empty list to store all HD strings from all PDFs
all_hd_strings = []

# Iterate over each file in the specified directory
for filename in os.listdir(pdf_directory):
    if filename.endswith('.pdf'):  # Check if the file is a PDF
        file_path = os.path.join(pdf_directory, filename)
        
        # Extract year and sex from the filename
        parts = filename.split('_')
        if len(parts) >= 4:
            year = parts[2]
            sex = parts[3].removesuffix('.pdf')
        else:
            continue  # Skip files that do not have enough parts in the filename
        
        # Open the PDF file
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            number_of_pages = len(reader.pages)
            matches = []  # Initialize a list to store matches for this file

            # Iterate through each page and extract text
            for page in range(number_of_pages):
                text = reader.pages[page].extract_text()
 
                # Use regex to find all strings that start with "HD-"
                if text:  # Check if text is not None
                    found_matches = re.findall(r'\bHD-([A-Za-z][\w]*)', text)  # Capture the first letter after "HD-"
                    # Extract only the first letter and ignore everything else
                    cleaned_matches = [match[0] for match in found_matches]  # Take only the first character after "HD-"
                    matches.extend(cleaned_matches)  # Add cleaned matches to the list
            
            # Count occurrences of each unique value
            value_counts = defaultdict(int)
            for match in matches:
                value_counts[match] += 1  # Increment the count for each match
            
            # Add the dictionary for this file to the list after processing all pages
            all_hd_strings.append({
                "year": year,
                "sex": sex,
                "values": dict(value_counts)  # Convert defaultdict to a regular dict
            })

# Sort the list of dictionaries by the "year" key in ascending order
all_hd_strings.sort(key=lambda x: int(x["year"]))

# Create a JSON file from the results
json_file_path = "hd_strings.json"  # Specify the path for the JSON file
with open(json_file_path, 'w') as json_file:
    json.dump(all_hd_strings, json_file, indent=4)  # Write the list to the JSON file with indentation for readability
