from bs4 import BeautifulSoup
import os

# Define the source and destination directories
source_directory = './data/raw'
destination_directory = './data/clean'

# Ensure the destination directory exists
os.makedirs(destination_directory, exist_ok=True)

# Function to process a single file
def process_file(file_path):
    if file_path.find(".DS_Store") == -1:
      print(f"cleaning {file_path}")
      with open(file_path, 'r', encoding='utf-8') as file:
          content = file.read()
      
      # Apply BeautifulSoup to the content
      soup = BeautifulSoup(content, 'html.parser')
      
      # Get the modified content
      modified_content = soup.get_text()    

      # Get the relative path of the file within the source directory
      relative_path = os.path.relpath(file_path, source_directory)
      
      # Create the output file path in the destination directory
      output_file_path = os.path.join(destination_directory, relative_path)
      
      # Ensure the directory structure exists in the destination directory
      os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
      
      # Write the modified content to the destination file
      with open(output_file_path, 'w', encoding='utf-8') as output_file:
          output_file.write(modified_content)

# Iterate over files in the source directory
for root, _, files in os.walk(source_directory):
    for file in files:
        file_path = os.path.join(root, file)
        process_file(file_path)

print("Processing complete. Modified files are in the destination directory.")